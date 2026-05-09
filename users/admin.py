from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Project, Tag, BlogPost


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


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'ai_percentage', 'updated_at')
    list_filter = ('status',)
    search_fields = ('name', 'description', 'owner__username', 'owner__email')
    ordering = ('-updated_at',)
    raw_id_fields = ('owner',)
    readonly_fields = ('created_at', 'updated_at', 'slug')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    readonly_fields = ('slug',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'published_at', 'view_count')
    list_filter = ('is_published',)
    search_fields = ('title', 'content', 'author__username', 'author__email')
    ordering = ('-published_at', '-created_at')
    raw_id_fields = ('author',)
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at', 'slug', 'view_count')
