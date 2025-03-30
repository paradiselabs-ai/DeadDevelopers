from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import ChatMessage, ChatNotification, ChatRoom

User = get_user_model()

@receiver(post_save, sender=ChatMessage)
def create_chat_notifications(sender, instance, created, **kwargs):
    """
    Create notifications for all participants in a chat room when a new message is created.
    """
    if created:
        room = instance.room
        sender_user = instance.user
        
        # For private chats, notify all participants except the sender
        if room.is_private:
            for user in room.participants.all():
                if user != sender_user:
                    ChatNotification.objects.create(
                        user=user,
                        room=room,
                        message=instance
                    )
        
        # For public and global chats, notify users who have explicitly joined the room
        else:
            # Get all users who have presence in this room
            from .models import UserPresence
            user_presences = UserPresence.objects.filter(room=room).exclude(user=sender_user)
            
            for presence in user_presences:
                ChatNotification.objects.create(
                    user=presence.user,
                    room=room,
                    message=instance
                )