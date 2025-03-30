from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom account adapter for DeadDevelopers"""
    
    def get_login_redirect_url(self, request):
        """Redirect to dashboard after login"""
        return settings.LOGIN_REDIRECT_URL
    
    def get_logout_redirect_url(self, request):
        """Redirect to home after logout"""
        return settings.ACCOUNT_LOGOUT_REDIRECT_URL
    
    def get_email_verification_redirect_url(email_address):
        """Redirect to dashboard after email verification"""
        return settings.LOGIN_REDIRECT_URL

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom social account adapter for GitHub integration"""
    
    def pre_social_login(self, request, sociallogin):
        """Handle pre-social login actions"""
        # If the user is already logged in and trying to connect a social account
        if request.user.is_authenticated and not sociallogin.is_existing:
            # Connect the social account to the current user
            sociallogin.connect(request, request.user)
    
    def populate_user(self, request, sociallogin, data):
        """Populate user fields from social account data"""
        user = super().populate_user(request, sociallogin, data)
        
        # Get data from GitHub
        if sociallogin.account.provider == 'github':
            github_data = sociallogin.account.extra_data
            
            # Set username if not already set
            if not user.username:
                user.username = github_data.get('login', '')
            
            # Set name if available
            if github_data.get('name'):
                name_parts = github_data.get('name', '').split(' ', 1)
                user.first_name = name_parts[0]
                user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            # Set GitHub username
            user.github_username = github_data.get('login', '')
            
            # Set AI percentage to default value
            user.ai_percentage = 0
        
        return user
    
    def save_user(self, request, sociallogin, form=None):
        """Save the user and update session data for FastHTML"""
        user = super().save_user(request, sociallogin, form)
        
        # Update FastHTML session data
        request.session['auth'] = user.username
        request.session['user'] = {
            'name': user.get_display_name(),
            'email': user.email,
            'ai_percentage': user.ai_percentage
        }
        
        return user