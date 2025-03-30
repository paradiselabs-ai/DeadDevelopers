import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatRoom, ChatMessage, UserPresence


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat functionality.
    
    This consumer handles:
    - Connecting to chat rooms
    - Sending and receiving messages
    - User presence updates
    - Message status updates
    """
    
    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        self.user = self.scope["user"]
        self.room_slug = self.scope["url_route"]["kwargs"]["room_slug"]
        self.room_group_name = f"chat_{self.room_slug}"
        
        # Check if user is authenticated
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Check if room exists and user has access
        room_exists = await self.room_exists()
        if not room_exists:
            await self.close()
            return
        
        user_has_access = await self.user_has_access()
        if not user_has_access:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Accept the WebSocket connection
        await self.accept()
        
        # Update user presence
        await self.update_user_presence(is_online=True)
        
        # Send user presence update to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_presence",
                "user_id": self.user.id,
                "username": self.user.username,
                "is_online": True,
                "timestamp": timezone.now().isoformat(),
            }
        )
        
        # Send chat history to the connected user
        await self.send_chat_history()
    
    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        if hasattr(self, "room_group_name"):
            # Update user presence
            await self.update_user_presence(is_online=False)
            
            # Send user presence update to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_presence",
                    "user_id": self.user.id,
                    "username": self.user.username,
                    "is_online": False,
                    "timestamp": timezone.now().isoformat(),
                }
            )
            
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """
        Called when we get a text frame from the client.
        """
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type", "message")
        
        if message_type == "message":
            # Handle new message
            content = text_data_json["content"]
            is_code = text_data_json.get("is_code", False)
            code_language = text_data_json.get("code_language", "")
            
            # Save message to database
            message = await self.save_message(content, is_code, code_language)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message_id": message.id,
                    "user_id": self.user.id,
                    "username": self.user.username,
                    "content": content,
                    "is_code": is_code,
                    "code_language": code_language,
                    "timestamp": message.timestamp.isoformat(),
                }
            )
        
        elif message_type == "typing":
            # Handle typing indicator
            is_typing = text_data_json["is_typing"]
            
            # Send typing status to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_indicator",
                    "user_id": self.user.id,
                    "username": self.user.username,
                    "is_typing": is_typing,
                }
            )
        
        elif message_type == "read":
            # Handle message read status
            message_id = text_data_json["message_id"]
            
            # Update message read status
            await self.mark_message_as_read(message_id)
            
            # Send read status to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "message_read",
                    "message_id": message_id,
                    "user_id": self.user.id,
                    "username": self.user.username,
                }
            )
    
    async def chat_message(self, event):
        """
        Called when a message is received from the room group.
        """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "type": "message",
            "message_id": event["message_id"],
            "user_id": event["user_id"],
            "username": event["username"],
            "content": event["content"],
            "is_code": event["is_code"],
            "code_language": event["code_language"],
            "timestamp": event["timestamp"],
        }))
    
    async def typing_indicator(self, event):
        """
        Called when a typing indicator is received from the room group.
        """
        # Send typing indicator to WebSocket
        await self.send(text_data=json.dumps({
            "type": "typing",
            "user_id": event["user_id"],
            "username": event["username"],
            "is_typing": event["is_typing"],
        }))
    
    async def message_read(self, event):
        """
        Called when a message read status is received from the room group.
        """
        # Send message read status to WebSocket
        await self.send(text_data=json.dumps({
            "type": "read",
            "message_id": event["message_id"],
            "user_id": event["user_id"],
            "username": event["username"],
        }))
    
    async def user_presence(self, event):
        """
        Called when a user presence update is received from the room group.
        """
        # Send user presence update to WebSocket
        await self.send(text_data=json.dumps({
            "type": "presence",
            "user_id": event["user_id"],
            "username": event["username"],
            "is_online": event["is_online"],
            "timestamp": event["timestamp"],
        }))
    
    @database_sync_to_async
    def room_exists(self):
        """
        Check if the chat room exists.
        """
        try:
            self.room = ChatRoom.objects.get(slug=self.room_slug)
            return True
        except ChatRoom.DoesNotExist:
            return False
    
    @database_sync_to_async
    def user_has_access(self):
        """
        Check if the user has access to the chat room.
        """
        return self.room.can_user_access(self.user)
    
    @database_sync_to_async
    def save_message(self, content, is_code=False, code_language=""):
        """
        Save a new message to the database.
        """
        message = ChatMessage.objects.create(
            room=self.room,
            user=self.user,
            content=content,
            is_code=is_code,
            code_language=code_language
        )
        return message
    
    @database_sync_to_async
    def mark_message_as_read(self, message_id):
        """
        Mark a message as read.
        """
        try:
            message = ChatMessage.objects.get(id=message_id)
            message.mark_as_read()
            return True
        except ChatMessage.DoesNotExist:
            return False
    
    @database_sync_to_async
    def update_user_presence(self, is_online=True):
        """
        Update user presence in the chat room.
        """
        presence, created = UserPresence.objects.get_or_create(
            user=self.user,
            room=self.room,
            defaults={"is_online": is_online}
        )
        
        if not created:
            presence.update_presence(is_online)
        
        return presence
    
    @database_sync_to_async
    def get_chat_history(self, limit=50):
        """
        Get the chat history for the room.
        """
        messages = ChatMessage.objects.filter(room=self.room).order_by('-timestamp')[:limit]
        
        # Convert to list of dictionaries for JSON serialization
        history = []
        for message in reversed(list(messages)):
            history.append({
                "message_id": message.id,
                "user_id": message.user.id,
                "username": message.user.username,
                "content": message.content,
                "is_code": message.is_code,
                "code_language": message.code_language,
                "timestamp": message.timestamp.isoformat(),
                "is_edited": message.is_edited,
                "edited_at": message.edited_at.isoformat() if message.edited_at else None,
            })
        
        return history
    
    @database_sync_to_async
    def get_online_users(self):
        """
        Get the list of online users in the chat room.
        """
        presences = UserPresence.objects.filter(room=self.room, is_online=True)
        
        # Convert to list of dictionaries for JSON serialization
        users = []
        for presence in presences:
            users.append({
                "user_id": presence.user.id,
                "username": presence.user.username,
                "last_seen": presence.last_seen.isoformat(),
            })
        
        return users
    
    async def send_chat_history(self):
        """
        Send chat history to the connected user.
        """
        history = await self.get_chat_history()
        online_users = await self.get_online_users()
        
        await self.send(text_data=json.dumps({
            "type": "history",
            "messages": history,
            "online_users": online_users,
        }))