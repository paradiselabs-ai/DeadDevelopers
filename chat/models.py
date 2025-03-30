from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class ChatRoom(models.Model):
    """
    Model representing a chat room.
    
    Types:
    - global: Single global chat room for all users
    - public: Topic-based public chat rooms
    - private: User-to-user private chat rooms
    """
    ROOM_TYPES = (
        ('global', _('Global')),
        ('public', _('Public')),
        ('private', _('Private')),
    )
    
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    type = models.CharField(_('type'), max_length=10, choices=ROOM_TYPES, default='public')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # For private chats, we need to track participants
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chat_rooms',
        verbose_name=_('participants'),
        blank=True
    )
    
    # For public chats, we can have moderators
    moderators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='moderated_chat_rooms',
        verbose_name=_('moderators'),
        blank=True
    )
    
    # For public chats, we can have topics/tags
    topics = models.CharField(_('topics'), max_length=255, blank=True, help_text=_('Comma-separated topics'))
    
    # Additional settings
    is_active = models.BooleanField(_('is active'), default=True)
    max_participants = models.PositiveIntegerField(_('max participants'), default=0, help_text=_('0 for unlimited'))
    
    class Meta:
        verbose_name = _('chat room')
        verbose_name_plural = _('chat rooms')
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_private(self):
        return self.type == 'private'
    
    @property
    def is_public(self):
        return self.type == 'public'
    
    @property
    def is_global(self):
        return self.type == 'global'
    
    def get_absolute_url(self):
        return f"/chat/{self.slug}/"
    
    def add_participant(self, user):
        """Add a user to the chat room participants"""
        if not self.participants.filter(id=user.id).exists():
            self.participants.add(user)
            self.save()
    
    def remove_participant(self, user):
        """Remove a user from the chat room participants"""
        if self.participants.filter(id=user.id).exists():
            self.participants.remove(user)
            self.save()
    
    def can_user_access(self, user):
        """Check if a user can access this chat room"""
        if not user.is_authenticated:
            return False
        
        if self.is_global or self.is_public:
            return True
        
        if self.is_private:
            return self.participants.filter(id=user.id).exists()
        
        return False


class ChatMessage(models.Model):
    """Model representing a chat message"""
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('room')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages',
        verbose_name=_('user')
    )
    content = models.TextField(_('content'))
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    
    # For code snippets
    is_code = models.BooleanField(_('is code'), default=False)
    code_language = models.CharField(_('code language'), max_length=50, blank=True)
    
    # Message status
    is_read = models.BooleanField(_('is read'), default=False)
    is_edited = models.BooleanField(_('is edited'), default=False)
    edited_at = models.DateTimeField(_('edited at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('chat message')
        verbose_name_plural = _('chat messages')
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
    
    def mark_as_read(self):
        """Mark the message as read"""
        self.is_read = True
        self.save()
    
    def edit_message(self, new_content):
        """Edit the message content"""
        self.content = new_content
        self.is_edited = True
        self.edited_at = timezone.now()
        self.save()


class ChatNotification(models.Model):
    """Model for tracking unread messages and notifications"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_notifications',
        verbose_name=_('user')
    )
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('room')
    )
    message = models.ForeignKey(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('message')
    )
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    is_read = models.BooleanField(_('is read'), default=False)
    
    class Meta:
        verbose_name = _('chat notification')
        verbose_name_plural = _('chat notifications')
        ordering = ['-timestamp']
        unique_together = ('user', 'message')
    
    def __str__(self):
        return f"Notification for {self.user.username} in {self.room.name}"
    
    def mark_as_read(self):
        """Mark the notification as read"""
        self.is_read = True
        self.save()


class UserPresence(models.Model):
    """Model for tracking user presence in chat rooms"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='presence',
        verbose_name=_('user')
    )
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='presence',
        verbose_name=_('room')
    )
    last_seen = models.DateTimeField(_('last seen'), auto_now=True)
    is_online = models.BooleanField(_('is online'), default=False)
    
    class Meta:
        verbose_name = _('user presence')
        verbose_name_plural = _('user presences')
        unique_together = ('user', 'room')
    
    def __str__(self):
        status = "online" if self.is_online else "offline"
        return f"{self.user.username} is {status} in {self.room.name}"
    
    def update_presence(self, is_online=True):
        """Update user presence status"""
        self.is_online = is_online
        self.save()