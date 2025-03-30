from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for our custom User model.
    Extends the standard Django UserAdmin with our custom fields.
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'bio', 'avatar')}),
        (_('Social links'), {'fields': ('github_username', 'twitter_username', 'website')}),
        (_('DeadDevelopers metrics'), {'fields': ('ai_percentage', 'challenge_count', 'completed_projects')}),
        (_('Preferences'), {'fields': ('theme_preference',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    list_display = ('email', 'username', 'first_name', 'last_name', 'ai_percentage', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
