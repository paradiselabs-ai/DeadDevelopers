from fasthtml.common import *
from app import app, rt, User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Q
import json

# Import chat models
from chat.models import ChatRoom, ChatMessage, UserPresence, ChatNotification

def chat_header():
    """Header component for the chat section"""
    return Div(
        H1("DeadDevelopers Chat", cls="chat-title"),
        P("Connect with other AI-powered developers in real-time", cls="chat-subtitle"),
        cls="chat-header terminal-header"
    )

def chat_room_card(room):
    """Card component for a chat room"""
    # Get online users count
    online_count = UserPresence.objects.filter(room=room, is_online=True).count()
    
    # Get unread messages count for current user
    unread_count = ChatNotification.objects.filter(
        room=room,
        user=get_current_user(),
        is_read=False
    ).count()
    
    # Format room type badge
    room_type_badge = ""
    if room.is_global:
        room_type_badge = Span("GLOBAL", cls="room-type global")
    elif room.is_public:
        room_type_badge = Span("PUBLIC", cls="room-type public")
    elif room.is_private:
        room_type_badge = Span("PRIVATE", cls="room-type private")
    
    # Format unread badge
    unread_badge = ""
    if unread_count > 0:
        unread_badge = Span(str(unread_count), cls="unread-badge")
    
    return Div(
        Div(
            H3(room.name, cls="room-name"),
            room_type_badge,
            cls="room-header"
        ),
        P(room.description, cls="room-description"),
        Div(
            Span(f"{online_count} online", cls="online-count"),
            unread_badge,
            cls="room-meta"
        ),
        A(
            "Join Chat",
            href=f"/chat/{room.slug}",
            cls="join-room-btn terminal-button"
        ),
        cls="room-card terminal-card",
        hx_get=f"/chat/{room.slug}",
        hx_target="#chat-container"
    )

def chat_sidebar(active_room=None):
    """Sidebar component for chat navigation"""
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
    public_rooms = ChatRoom.objects.filter(type='public', is_active=True)[:5]
    
    # Get private chat rooms for the current user
    user = get_current_user()
    private_rooms = ChatRoom.objects.filter(
        type='private',
        is_active=True,
        participants=user
    )[:5]
    
    # Create room list items
    room_items = []
    
    # Add global room
    active_class = "active" if active_room and active_room.id == global_room.id else ""
    room_items.append(
        Li(
            A(
                Span("# ", cls="room-prefix"),
                global_room.name,
                href=f"/chat/{global_room.slug}",
                cls=f"room-link {active_class}"
            ),
            cls="room-item"
        )
    )
    
    # Add public rooms
    if public_rooms:
        room_items.append(Li("Public Rooms", cls="room-category"))
        for room in public_rooms:
            active_class = "active" if active_room and active_room.id == room.id else ""
            room_items.append(
                Li(
                    A(
                        Span("# ", cls="room-prefix"),
                        room.name,
                        href=f"/chat/{room.slug}",
                        cls=f"room-link {active_class}"
                    ),
                    cls="room-item"
                )
            )
    
    # Add private rooms
    if private_rooms:
        room_items.append(Li("Private Chats", cls="room-category"))
        for room in private_rooms:
            active_class = "active" if active_room and active_room.id == room.id else ""
            # Get the other participant
            other_participant = room.participants.exclude(id=user.id).first()
            room_name = other_participant.username if other_participant else room.name
            room_items.append(
                Li(
                    A(
                        Span("@ ", cls="room-prefix"),
                        room_name,
                        href=f"/chat/{room.slug}",
                        cls=f"room-link {active_class}"
                    ),
                    cls="room-item"
                )
            )
    
    # Add create room button
    room_items.append(
        Li(
            A(
                "+ Create Room",
                href="/chat/create",
                cls="create-room-btn"
            ),
            cls="room-item create-room"
        )
    )
    
    return Div(
        H3("Chat Rooms", cls="sidebar-title"),
        Ul(*room_items, cls="room-list"),
        cls="chat-sidebar"
    )

def message_item(message):
    """Component for a single chat message"""
    user = message.user
    
    # Format timestamp
    timestamp = message.timestamp.strftime("%H:%M")
    
    # Format code block if message is code
    content = message.content
    if message.is_code:
        language_class = f"language-{message.code_language}" if message.code_language else ""
        content = Pre(
            Code(
                message.content,
                cls=language_class
            ),
            cls="message-code"
        )
    
    # Format edited indicator
    edited_indicator = ""
    if message.is_edited:
        edited_indicator = Span("(edited)", cls="edited-indicator")
    
    return Div(
        Div(
            Img(src=user.avatar.url if hasattr(user, 'avatar') and user.avatar else "/static/img/default-avatar.svg", 
                alt=f"{user.username}'s avatar", 
                cls="message-avatar"),
            cls="message-avatar-container"
        ),
        Div(
            Div(
                Span(user.username, cls="message-username"),
                Span(timestamp, cls="message-time"),
                edited_indicator,
                cls="message-header"
            ),
            Div(
                content,
                cls="message-content"
            ),
            cls="message-body"
        ),
        id=f"message-{message.id}",
        cls="message-item",
        data_message_id=str(message.id),
        data_user_id=str(user.id)
    )

def chat_message_list(room):
    """Component for the chat message list"""
    # Get recent messages
    messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')[:50]
    messages = reversed(list(messages))  # Reverse to show oldest first
    
    # Create message items
    message_items = [message_item(message) for message in messages]
    
    return Div(
        *message_items,
        id="message-list",
        cls="message-list"
    )

def chat_input_form(room):
    """Component for the chat input form"""
    return Form(
        Textarea(
            placeholder="Type your message here...",
            name="message",
            id="message-input",
            cls="chat-input terminal-input",
            rows=3
        ),
        Div(
            Button(
                "Send",
                type="submit",
                id="send-button",
                cls="send-btn terminal-button"
            ),
            Button(
                "Code",
                type="button",
                id="code-button",
                cls="code-btn terminal-button secondary"
            ),
            cls="chat-buttons"
        ),
        id="chat-form",
        cls="chat-form terminal-form",
        data_room_slug=room.slug
    )

def online_users_list(room):
    """Component for the online users list"""
    # Get online users
    online_users = UserPresence.objects.filter(
        room=room,
        is_online=True
    ).select_related('user')
    
    # Create user items
    user_items = []
    for presence in online_users:
        user = presence.user
        user_items.append(
            Li(
                Img(src=user.avatar.url if hasattr(user, 'avatar') and user.avatar else "/static/img/default-avatar.svg", 
                    alt=f"{user.username}'s avatar", 
                    cls="user-avatar"),
                Span(user.username, cls="user-name"),
                cls="user-item",
                data_user_id=str(user.id)
            )
        )
    
    return Div(
        H3(f"Online Users ({len(user_items)})", cls="users-title"),
        Ul(*user_items, cls="users-list", id="online-users"),
        cls="online-users-container"
    )

def chat_room_component(room):
    """Main component for a chat room"""
    return Div(
        Div(
            H2(room.name, cls="room-title"),
            P(room.description, cls="room-description"),
            cls="room-header terminal-header"
        ),
        Div(
            chat_message_list(room),
            chat_input_form(room),
            cls="chat-main"
        ),
        online_users_list(room),
        id="chat-room",
        cls="chat-room",
        data_room_slug=room.slug
    )

def chat_websocket_script(room):
    """JavaScript for WebSocket connection"""
    return Script(f"""
    // Chat WebSocket functionality
    document.addEventListener('DOMContentLoaded', function() {{
        const roomSlug = '{room.slug}';
        const messageList = document.getElementById('message-list');
        const chatForm = document.getElementById('chat-form');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        const codeButton = document.getElementById('code-button');
        const onlineUsers = document.getElementById('online-users');
        
        let socket = null;
        let isCode = false;
        let codeLanguage = '';
        
        // Connect to WebSocket
        function connectWebSocket() {{
            socket = new WebSocket(`ws://${{window.location.host}}/ws/chat/${{roomSlug}}/`);
            
            socket.onopen = function(e) {{
                console.log('WebSocket connection established');
                messageInput.disabled = false;
                sendButton.disabled = false;
            }};
            
            socket.onmessage = function(e) {{
                const data = JSON.parse(e.data);
                
                if (data.type === 'message') {{
                    // Add new message to the chat
                    addMessage(data);
                    
                    // Scroll to bottom
                    messageList.scrollTop = messageList.scrollHeight;
                }}
                else if (data.type === 'typing') {{
                    // Show typing indicator
                    updateTypingIndicator(data);
                }}
                else if (data.type === 'presence') {{
                    // Update online users
                    updateOnlineUsers(data);
                }}
                else if (data.type === 'history') {{
                    // Load chat history
                    loadChatHistory(data);
                    
                    // Scroll to bottom
                    messageList.scrollTop = messageList.scrollHeight;
                }}
            }};
            
            socket.onclose = function(e) {{
                console.log('WebSocket connection closed');
                messageInput.disabled = true;
                sendButton.disabled = true;
                
                // Try to reconnect after 5 seconds
                setTimeout(function() {{
                    connectWebSocket();
                }}, 5000);
            }};
            
            socket.onerror = function(e) {{
                console.error('WebSocket error:', e);
            }};
        }}
        
        // Add a new message to the chat
        function addMessage(data) {{
            const messageItem = document.createElement('div');
            messageItem.className = 'message-item';
            messageItem.id = `message-${{data.message_id}}`;
            messageItem.dataset.messageId = data.message_id;
            messageItem.dataset.userId = data.user_id;
            
            let content = data.content;
            if (data.is_code) {{
                const languageClass = data.code_language ? `language-${{data.code_language}}` : '';
                content = `<pre class="message-code"><code class="${{languageClass}}">${{escapeHtml(data.content)}}</code></pre>`;
            }}
            
            const timestamp = new Date(data.timestamp).toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
            
            messageItem.innerHTML = `
                <div class="message-avatar-container">
                    <img src="/static/img/default-avatar.svg" alt="${{data.username}}'s avatar" class="message-avatar">
                </div>
                <div class="message-body">
                    <div class="message-header">
                        <span class="message-username">${{data.username}}</span>
                        <span class="message-time">${{timestamp}}</span>
                    </div>
                    <div class="message-content">
                        ${{content}}
                    </div>
                </div>
            `;
            
            messageList.appendChild(messageItem);
            
            // Highlight code if needed
            if (data.is_code && window.Prism) {{
                Prism.highlightElement(messageItem.querySelector('code'));
            }}
        }}
        
        // Update typing indicator
        function updateTypingIndicator(data) {{
            const typingIndicator = document.getElementById('typing-indicator');
            
            if (data.is_typing) {{
                if (!typingIndicator) {{
                    const indicator = document.createElement('div');
                    indicator.id = 'typing-indicator';
                    indicator.className = 'typing-indicator';
                    indicator.innerHTML = `<span>${{data.username}} is typing...</span>`;
                    messageList.appendChild(indicator);
                }}
            }} else {{
                if (typingIndicator) {{
                    typingIndicator.remove();
                }}
            }}
        }}
        
        // Update online users
        function updateOnlineUsers(data) {{
            const userItem = document.querySelector(`.user-item[data-user-id="${{data.user_id}}"]`);
            
            if (data.is_online) {{
                if (!userItem) {{
                    const newUserItem = document.createElement('li');
                    newUserItem.className = 'user-item';
                    newUserItem.dataset.userId = data.user_id;
                    newUserItem.innerHTML = `
                        <img src="/static/img/default-avatar.svg" alt="${{data.username}}'s avatar" class="user-avatar">
                        <span class="user-name">${{data.username}}</span>
                    `;
                    onlineUsers.appendChild(newUserItem);
                    
                    // Update user count
                    const usersTitle = document.querySelector('.users-title');
                    const userCount = onlineUsers.querySelectorAll('.user-item').length;
                    usersTitle.textContent = `Online Users (${{userCount}})`;
                }}
            }} else {{
                if (userItem) {{
                    userItem.remove();
                    
                    // Update user count
                    const usersTitle = document.querySelector('.users-title');
                    const userCount = onlineUsers.querySelectorAll('.user-item').length;
                    usersTitle.textContent = `Online Users (${{userCount}})`;
                }}
            }}
        }}
        
        // Load chat history
        function loadChatHistory(data) {{
            // Clear existing messages
            messageList.innerHTML = '';
            
            // Add messages from history
            data.messages.forEach(message => {{
                addMessage(message);
            }});
            
            // Update online users
            onlineUsers.innerHTML = '';
            data.online_users.forEach(user => {{
                const userItem = document.createElement('li');
                userItem.className = 'user-item';
                userItem.dataset.userId = user.user_id;
                userItem.innerHTML = `
                    <img src="/static/img/default-avatar.svg" alt="${{user.username}}'s avatar" class="user-avatar">
                    <span class="user-name">${{user.username}}</span>
                `;
                onlineUsers.appendChild(userItem);
            }});
            
            // Update user count
            const usersTitle = document.querySelector('.users-title');
            const userCount = data.online_users.length;
            usersTitle.textContent = `Online Users (${{userCount}})`;
        }}
        
        // Send a message
        function sendMessage() {{
            if (!socket || socket.readyState !== WebSocket.OPEN) {{
                console.error('WebSocket not connected');
                return;
            }}
            
            const content = messageInput.value.trim();
            if (!content) {{
                return;
            }}
            
            const message = {{
                type: 'message',
                content: content,
                is_code: isCode,
                code_language: codeLanguage
            }};
            
            socket.send(JSON.stringify(message));
            
            // Clear input
            messageInput.value = '';
            
            // Reset code mode
            if (isCode) {{
                toggleCodeMode();
            }}
        }}
        
        // Toggle code mode
        function toggleCodeMode() {{
            isCode = !isCode;
            
            if (isCode) {{
                codeButton.classList.add('active');
                messageInput.classList.add('code-mode');
                
                // Prompt for language
                codeLanguage = prompt('Enter code language (e.g., javascript, python, html):', 'javascript');
                if (!codeLanguage) {{
                    codeLanguage = '';
                }}
                
                // Add language indicator
                const languageIndicator = document.createElement('div');
                languageIndicator.id = 'language-indicator';
                languageIndicator.className = 'language-indicator';
                languageIndicator.textContent = `Language: ${{codeLanguage || 'plain'}}`;
                chatForm.insertBefore(languageIndicator, messageInput);
            }} else {{
                codeButton.classList.remove('active');
                messageInput.classList.remove('code-mode');
                
                // Remove language indicator
                const languageIndicator = document.getElementById('language-indicator');
                if (languageIndicator) {{
                    languageIndicator.remove();
                }}
                
                codeLanguage = '';
            }}
        }}
        
        // Send typing indicator
        function sendTypingIndicator(isTyping) {{
            if (!socket || socket.readyState !== WebSocket.OPEN) {{
                return;
            }}
            
            const message = {{
                type: 'typing',
                is_typing: isTyping
            }};
            
            socket.send(JSON.stringify(message));
        }}
        
        // Helper function to escape HTML
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        // Event listeners
        chatForm.addEventListener('submit', function(e) {{
            e.preventDefault();
            sendMessage();
        }});
        
        codeButton.addEventListener('click', function(e) {{
            e.preventDefault();
            toggleCodeMode();
        }});
        
        let typingTimeout = null;
        messageInput.addEventListener('input', function() {{
            if (!typingTimeout) {{
                sendTypingIndicator(true);
            }}
            
            clearTimeout(typingTimeout);
            typingTimeout = setTimeout(function() {{
                sendTypingIndicator(false);
                typingTimeout = null;
            }}, 1000);
        }});
        
        // Connect to WebSocket
        connectWebSocket();
    }});
    """)

@rt('/chat')
def get(req):
    """Chat home page"""
    # Check if user is authenticated
    if not req.user.is_authenticated:
        return RedirectResponse('/login?next=/chat', status_code=303)
    
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
        participants=req.user
    )
    
    # Create room cards
    room_cards = []
    
    # Add global room card
    room_cards.append(chat_room_card(global_room))
    
    # Add public room cards
    for room in public_rooms:
        room_cards.append(chat_room_card(room))
    
    # Add private room cards
    for room in private_rooms:
        room_cards.append(chat_room_card(room))
    
    # Create chat home component
    chat_home = Div(
        chat_header(),
        Div(
            A(
                "+ Create New Chat Room",
                href="/chat/create",
                cls="create-room-btn terminal-button"
            ),
            cls="chat-actions"
        ),
        Div(
            *room_cards,
            cls="room-grid"
        ),
        id="chat-container",
        cls="chat-container"
    )
    
    return Titled(
        "Chat | DeadDevelopers",
        Div(
            Link(rel="stylesheet", href="/static/css/chat.css"),
            chat_home,
            cls="chat-page"
        )
    )

@rt('/chat/{room_slug}')
def get(req, room_slug):
    """Chat room page"""
    # Check if user is authenticated
    if not req.user.is_authenticated:
        return RedirectResponse(f'/login?next=/chat/{room_slug}', status_code=303)
    
    # Get the chat room
    try:
        room = ChatRoom.objects.get(slug=room_slug, is_active=True)
    except ChatRoom.DoesNotExist:
        return RedirectResponse('/chat', status_code=303)
    
    # Check if user has access to this room
    if not room.can_user_access(req.user):
        return RedirectResponse('/chat', status_code=303)
    
    # For private rooms, ensure both users are participants
    if room.is_private:
        room.add_participant(req.user)
    
    # Update or create user presence
    presence, created = UserPresence.objects.get_or_create(
        user=req.user,
        room=room,
        defaults={"is_online": True}
    )
    
    if not created:
        presence.update_presence(is_online=True)
    
    # Mark notifications as read
    ChatNotification.objects.filter(
        user=req.user,
        room=room,
        is_read=False
    ).update(is_read=True)
    
    # Create chat room page
    chat_room_page = Div(
        Link(rel="stylesheet", href="/static/css/chat.css"),
        Link(rel="stylesheet", href="/static/css/prism.css"),
        Div(
            chat_sidebar(active_room=room),
            Div(
                chat_room_component(room),
                cls="chat-content"
            ),
            cls="chat-layout"
        ),
        Script(src="/static/js/prism.js"),
        chat_websocket_script(room),
        cls="chat-page"
    )
    
    return Titled(
        f"{room.name} | Chat | DeadDevelopers",
        chat_room_page
    )

@rt('/chat/create')
def get(req):
    """Create chat room page"""
    # Check if user is authenticated
    if not req.user.is_authenticated:
        return RedirectResponse('/login?next=/chat/create', status_code=303)
    
    # Create form
    create_form = Form(
        H2("Create New Chat Room", cls="form-title terminal-header"),
        Div(
            Label("Room Name", htmlFor="name", cls="terminal-label"),
            Input(
                type="text",
                id="name",
                name="name",
                placeholder="Enter room name",
                required=True,
                cls="terminal-input"
            ),
            cls="form-group"
        ),
        Div(
            Label("Description", htmlFor="description", cls="terminal-label"),
            Textarea(
                id="description",
                name="description",
                placeholder="Enter room description",
                rows=3,
                cls="terminal-input"
            ),
            cls="form-group"
        ),
        Div(
            Label("Topics (comma-separated)", htmlFor="topics", cls="terminal-label"),
            Input(
                type="text",
                id="topics",
                name="topics",
                placeholder="ai, coding, projects",
                cls="terminal-input"
            ),
            cls="form-group"
        ),
        Div(
            Button(
                "Create Room",
                type="submit",
                cls="terminal-button"
            ),
            A(
                "Cancel",
                href="/chat",
                cls="terminal-button secondary"
            ),
            cls="form-buttons"
        ),
        method="post",
        action="/chat/create",
        cls="create-room-form terminal-form"
    )
    
    return Titled(
        "Create Chat Room | DeadDevelopers",
        Div(
            Link(rel="stylesheet", href="/static/css/chat.css"),
            Div(
                create_form,
                cls="create-room-container terminal-card"
            ),
            cls="chat-page centered"
        )
    )

@rt('/chat/create')
def post(req, name: str, description: str = "", topics: str = ""):
    """Handle chat room creation"""
    # Check if user is authenticated
    if not req.user.is_authenticated:
        return RedirectResponse('/login?next=/chat/create', status_code=303)
    
    # Validate input
    if not name:
        # Return form with error
        return get(req)
    
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
    room.moderators.add(req.user)
    
    # Add success message
    add_toast(req.session, f"Chat room '{name}' created successfully!", "success")
    
    # Redirect to the new room
    return RedirectResponse(f'/chat/{room.slug}', status_code=303)