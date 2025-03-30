from django.contrib import admin
from .models import ChatRoom, ChatMessage, ChatNotification, UserPresence

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'type', 'is_active', 'created_at', 'updated_at')
    list_filter = ('type', 'is_active', 'created_at')
    search_fields = ('name', 'slug', 'description', 'topics')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('participants', 'moderators')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'type')
        }),
        ('Participants', {
            'fields': ('participants', 'moderators')
        }),
        ('Settings', {
            'fields': ('is_active', 'max_participants', 'topics')
        }),
    )

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'short_content', 'is_code', 'timestamp', 'is_read', 'is_edited')
    list_filter = ('room', 'is_code', 'is_read', 'is_edited', 'timestamp')
    search_fields = ('content', 'user__username', 'room__name')
    readonly_fields = ('timestamp', 'edited_at')
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'

@admin.register(ChatNotification)
class ChatNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'message', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('user__username', 'room__name')
    readonly_fields = ('timestamp',)

@admin.register(UserPresence)
class UserPresenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'is_online', 'last_seen')
    list_filter = ('is_online', 'last_seen')
    search_fields = ('user__username', 'room__name')
    readonly_fields = ('last_seen',)