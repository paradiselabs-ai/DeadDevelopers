from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
import json

from .models import ChatRoom, ChatMessage, ChatNotification, UserPresence

@login_required
def chat_home(request):
    """
    Chat home page showing available chat rooms and recent activity.
    """
    # Get global chat room
    try:
        global_room = ChatRoom.objects.get(type='global')
    except ChatRoom.DoesNotExist:
        # Create global chat room if it doesn't exist
        global_room = ChatRoom.objects.create(
            name='Global Chat',
            slug='global',
            description='Chat room for all DeadDevelopers users',
            type='global',
            is_active=True
        )
    
    # Get public chat rooms
    public_rooms = ChatRoom.objects.filter(type='public', is_active=True)
    
    # Get private chat rooms for the current user
    private_rooms = ChatRoom.objects.filter(
        type='private',
        is_active=True,
        participants=request.user
    )
    
    # Get unread notifications count
    unread_count = ChatNotification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    context = {
        'global_room': global_room,
        'public_rooms': public_rooms,
        'private_rooms': private_rooms,
        'unread_count': unread_count,
    }
    
    return render(request, 'chat/home.html', context)

@login_required
def chat_rooms(request):
    """
    List all available chat rooms.
    """
    # Get all public chat rooms
    public_rooms = ChatRoom.objects.filter(type='public', is_active=True)
    
    # Get private chat rooms for the current user
    private_rooms = ChatRoom.objects.filter(
        type='private',
        is_active=True,
        participants=request.user
    )
    
    # Search functionality
    query = request.GET.get('q', '')
    if query:
        public_rooms = public_rooms.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(topics__icontains=query)
        )
        private_rooms = private_rooms.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Pagination for public rooms
    paginator = Paginator(public_rooms, 10)
    page_number = request.GET.get('page', 1)
    public_rooms_page = paginator.get_page(page_number)
    
    context = {
        'public_rooms': public_rooms_page,
        'private_rooms': private_rooms,
        'query': query,
    }
    
    return render(request, 'chat/rooms.html', context)

@login_required
def create_room(request):
    """
    Create a new chat room.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        topics = request.POST.get('topics', '')
        
        if name:
            # Generate slug from name
            slug = slugify(name)
            
            # Check if slug already exists
            if ChatRoom.objects.filter(slug=slug).exists():
                # Append timestamp to make slug unique
                slug = f"{slug}-{int(timezone.now().timestamp())}"
            
            # Create the room
            room = ChatRoom.objects.create(
                name=name,
                slug=slug,
                description=description,
                type='public',
                topics=topics,
                is_active=True
            )
            
            # Add creator as moderator
            room.moderators.add(request.user)
            
            # Redirect to the new room
            return redirect('chat:room', room_slug=room.slug)
    
    return render(request, 'chat/create_room.html')

@login_required
def chat_room(request, room_slug):
    """
    Display a specific chat room.
    """
    # Get the chat room
    room = get_object_or_404(ChatRoom, slug=room_slug, is_active=True)
    
    # Check if user has access to this room
    if not room.can_user_access(request.user):
        return redirect('chat:home')
    
    # For private rooms, ensure both users are participants
    if room.is_private:
        room.add_participant(request.user)
    
    # Update or create user presence
    presence, created = UserPresence.objects.get_or_create(
        user=request.user,
        room=room,
        defaults={"is_online": True}
    )
    
    if not created:
        presence.update_presence(is_online=True)
    
    # Mark notifications as read
    ChatNotification.objects.filter(
        user=request.user,
        room=room,
        is_read=False
    ).update(is_read=True)
    
    # Get recent messages
    messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')[:50]
    messages = reversed(list(messages))  # Reverse to show oldest first
    
    # Get online users
    online_users = UserPresence.objects.filter(
        room=room,
        is_online=True
    ).select_related('user')
    
    context = {
        'room': room,
        'messages': messages,
        'online_users': online_users,
        'is_moderator': request.user in room.moderators.all(),
    }
    
    return render(request, 'chat/room.html', context)

@login_required
def room_messages(request, room_slug):
    """
    Get messages for a specific chat room (for AJAX loading).
    """
    # Get the chat room
    room = get_object_or_404(ChatRoom, slug=room_slug, is_active=True)
    
    # Check if user has access to this room
    if not room.can_user_access(request.user):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Get messages with pagination
    page = request.GET.get('page', 1)
    before_id = request.GET.get('before_id')
    limit = int(request.GET.get('limit', 20))
    
    messages_query = ChatMessage.objects.filter(room=room)
    
    if before_id:
        try:
            before_message = ChatMessage.objects.get(id=before_id)
            messages_query = messages_query.filter(timestamp__lt=before_message.timestamp)
        except ChatMessage.DoesNotExist:
            pass
    
    messages = messages_query.order_by('-timestamp')[:limit]
    
    # Format messages for JSON response
    messages_data = []
    for message in reversed(list(messages)):
        messages_data.append({
            'id': message.id,
            'user_id': message.user.id,
            'username': message.user.username,
            'content': message.content,
            'is_code': message.is_code,
            'code_language': message.code_language,
            'timestamp': message.timestamp.isoformat(),
            'is_edited': message.is_edited,
            'edited_at': message.edited_at.isoformat() if message.edited_at else None,
        })
    
    return JsonResponse({
        'messages': messages_data,
        'has_more': len(messages) == limit,
    })

@login_required
def room_participants(request, room_slug):
    """
    Get participants for a specific chat room.
    """
    # Get the chat room
    room = get_object_or_404(ChatRoom, slug=room_slug, is_active=True)
    
    # Check if user has access to this room
    if not room.can_user_access(request.user):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Get online users
    online_users = UserPresence.objects.filter(
        room=room,
        is_online=True
    ).select_related('user')
    
    # Format users for JSON response
    users_data = []
    for presence in online_users:
        users_data.append({
            'id': presence.user.id,
            'username': presence.user.username,
            'last_seen': presence.last_seen.isoformat(),
        })
    
    return JsonResponse({
        'online_users': users_data,
    })

@login_required
def api_rooms(request):
    """
    API endpoint for getting chat rooms.
    """
    # Get global chat room
    try:
        global_room = ChatRoom.objects.get(type='global')
        global_room_data = {
            'id': global_room.id,
            'name': global_room.name,
            'slug': global_room.slug,
            'description': global_room.description,
            'type': global_room.type,
        }
    except ChatRoom.DoesNotExist:
        global_room_data = None
    
    # Get public chat rooms
    public_rooms = ChatRoom.objects.filter(type='public', is_active=True)
    public_rooms_data = []
    for room in public_rooms:
        public_rooms_data.append({
            'id': room.id,
            'name': room.name,
            'slug': room.slug,
            'description': room.description,
            'type': room.type,
            'topics': room.topics,
        })
    
    # Get private chat rooms for the current user
    private_rooms = ChatRoom.objects.filter(
        type='private',
        is_active=True,
        participants=request.user
    )
    private_rooms_data = []
    for room in private_rooms:
        # Get the other participant
        other_participant = room.participants.exclude(id=request.user.id).first()
        private_rooms_data.append({
            'id': room.id,
            'name': room.name,
            'slug': room.slug,
            'description': room.description,
            'type': room.type,
            'other_participant': {
                'id': other_participant.id,
                'username': other_participant.username,
            } if other_participant else None,
        })
    
    return JsonResponse({
        'global_room': global_room_data,
        'public_rooms': public_rooms_data,
        'private_rooms': private_rooms_data,
    })

@login_required
def api_messages(request, room_slug):
    """
    API endpoint for getting messages for a specific chat room.
    """
    # Get the chat room
    room = get_object_or_404(ChatRoom, slug=room_slug, is_active=True)
    
    # Check if user has access to this room
    if not room.can_user_access(request.user):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Get messages with pagination
    before_id = request.GET.get('before_id')
    limit = int(request.GET.get('limit', 20))
    
    messages_query = ChatMessage.objects.filter(room=room)
    
    if before_id:
        try:
            before_message = ChatMessage.objects.get(id=before_id)
            messages_query = messages_query.filter(timestamp__lt=before_message.timestamp)
        except ChatMessage.DoesNotExist:
            pass
    
    messages = messages_query.order_by('-timestamp')[:limit]
    
    # Format messages for JSON response
    messages_data = []
    for message in reversed(list(messages)):
        messages_data.append({
            'id': message.id,
            'user_id': message.user.id,
            'username': message.user.username,
            'content': message.content,
            'is_code': message.is_code,
            'code_language': message.code_language,
            'timestamp': message.timestamp.isoformat(),
            'is_edited': message.is_edited,
            'edited_at': message.edited_at.isoformat() if message.edited_at else None,
        })
    
    return JsonResponse({
        'messages': messages_data,
        'has_more': len(messages) == limit,
    })

@login_required
def api_notifications(request):
    """
    API endpoint for getting chat notifications.
    """
    # Get unread notifications
    notifications = ChatNotification.objects.filter(
        user=request.user,
        is_read=False
    ).select_related('room', 'message', 'message__user')
    
    # Format notifications for JSON response
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'id': notification.id,
            'room': {
                'id': notification.room.id,
                'name': notification.room.name,
                'slug': notification.room.slug,
                'type': notification.room.type,
            },
            'message': {
                'id': notification.message.id,
                'content': notification.message.content[:50] + '...' if len(notification.message.content) > 50 else notification.message.content,
                'username': notification.message.user.username,
            },
            'timestamp': notification.timestamp.isoformat(),
        })
    
    return JsonResponse({
        'notifications': notifications_data,
        'count': len(notifications_data),
    })

@require_POST
@login_required
def mark_notifications_read(request):
    """
    Mark notifications as read.
    """
    # Get notification IDs from request
    data = json.loads(request.body)
    notification_ids = data.get('notification_ids', [])
    
    if notification_ids:
        # Mark specific notifications as read
        ChatNotification.objects.filter(
            id__in=notification_ids,
            user=request.user
        ).update(is_read=True)
    else:
        # Mark all notifications as read
        ChatNotification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
    
    return JsonResponse({'success': True})