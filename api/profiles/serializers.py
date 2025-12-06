from rest_framework import serializers
from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data.
    Includes all public profile information.
    """
    display_name = serializers.CharField(source='get_display_name', read_only=True)
    avatar_url = serializers.CharField(source='get_avatar_url', read_only=True)
    profile_url = serializers.CharField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'display_name',
            'first_name',
            'last_name',
            'bio',
            'tagline',
            'location',
            'avatar_url',
            'profile_url',
            'github_username',
            'twitter_username',
            'linkedin_username',
            'website',
            'portfolio_url',
            'portfolio_content',
            'ai_percentage',
            'challenge_count',
            'completed_projects',
            'theme_preference',
            'is_public',
            'show_email',
            'date_joined',
        ]
        read_only_fields = [
            'id',
            'username',
            'date_joined',
            'display_name',
            'avatar_url',
            'profile_url',
        ]
    
    def to_representation(self, instance):
        """
        Customize the representation based on privacy settings.
        """
        data = super().to_representation(instance)
        
        # Hide email if user doesn't want it shown
        if not instance.show_email:
            data.pop('email', None)
        
        # Hide profile if not public (unless it's the owner viewing)
        request = self.context.get('request')
        if not instance.is_public and (not request or request.user != instance):
            # Return minimal data for private profiles
            return {
                'username': data['username'],
                'display_name': data['display_name'],
                'is_public': False,
            }
        
        return data


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    Only allows updating specific fields.
    """
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'bio',
            'tagline',
            'location',
            'github_username',
            'twitter_username',
            'linkedin_username',
            'website',
            'portfolio_url',
            'portfolio_content',
            'theme_preference',
            'is_public',
            'show_email',
        ]
