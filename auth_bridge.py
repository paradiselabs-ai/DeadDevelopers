"""
Authentication Bridge for FastHTML and Django

This module provides a unified authentication layer that synchronizes
FastHTML sessions with Django's authentication system, solving the
dual-session management problem.
"""

from typing import Optional
from django.contrib.auth import get_user_model, authenticate, login as django_login, logout as django_logout
from django.contrib.sessions.backends.db import SessionStore
from django.middleware.csrf import get_token
from fasthtml.common import *
from starlette.requests import Request

User = get_user_model()


class AuthBridge:
    """
    Bridge between FastHTML and Django authentication systems.
    
    This class ensures that both FastHTML sessions and Django sessions
    stay synchronized, preventing authentication conflicts.
    """
    
    @staticmethod
    def get_django_session(request: Request) -> SessionStore:
        """
        Get or create a Django session from the FastHTML request.
        
        Args:
            request: The FastHTML/Starlette request object
            
        Returns:
            Django SessionStore instance
        """
        session_key = request.cookies.get('sessionid')
        session = SessionStore(session_key=session_key)
        
        if not session.exists(session.session_key):
            session.create()
            
        return session
    
    @staticmethod
    def login_user(request: Request, fasthtml_session: dict, user: User) -> None:
        """
        Log in a user in both FastHTML and Django sessions.
        
        Args:
            request: The FastHTML/Starlette request object
            fasthtml_session: The FastHTML session dictionary
            user: The Django User instance to log in
        """
        # Update FastHTML session
        fasthtml_session['auth'] = user.username
        fasthtml_session['user'] = {
            'name': user.get_display_name(),
            'email': user.email,
            'ai_percentage': user.ai_percentage,
            'id': user.id
        }
        
        # Get Django session and update it
        django_session = AuthBridge.get_django_session(request)
        django_session['_auth_user_id'] = str(user.id)
        django_session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
        django_session['_auth_user_hash'] = user.get_session_auth_hash()
        django_session.save()
    
    @staticmethod
    def logout_user(request: Request, fasthtml_session: dict) -> None:
        """
        Log out a user from both FastHTML and Django sessions.
        
        Args:
            request: The FastHTML/Starlette request object
            fasthtml_session: The FastHTML session dictionary
        """
        # Clear FastHTML session
        fasthtml_session.pop('auth', None)
        fasthtml_session.pop('user', None)
        
        # Clear Django session
        django_session = AuthBridge.get_django_session(request)
        django_session.flush()
    
    @staticmethod
    def get_current_user(request: Request, fasthtml_session: dict) -> Optional[User]:
        """
        Get the currently authenticated user from the session.
        
        Args:
            request: The FastHTML/Starlette request object
            fasthtml_session: The FastHTML session dictionary
            
        Returns:
            User instance if authenticated, None otherwise
        """
        auth_username = fasthtml_session.get('auth')
        
        if not auth_username:
            return None
        
        try:
            user = User.objects.get(username=auth_username)
            return user
        except User.DoesNotExist:
            # User was deleted, clear session
            AuthBridge.logout_user(request, fasthtml_session)
            return None
    
    @staticmethod
    def sync_sessions(request: Request, fasthtml_session: dict) -> None:
        """
        Synchronize FastHTML and Django sessions.
        
        This ensures both sessions are in sync. If one has auth and the other
        doesn't, this method will reconcile them.
        
        Args:
            request: The FastHTML/Starlette request object
            fasthtml_session: The FastHTML session dictionary
        """
        django_session = AuthBridge.get_django_session(request)
        
        # Check if user is authenticated in Django
        django_user_id = django_session.get('_auth_user_id')
        fasthtml_auth = fasthtml_session.get('auth')
        
        # If Django has auth but FastHTML doesn't, sync to FastHTML
        if django_user_id and not fasthtml_auth:
            try:
                user = User.objects.get(id=django_user_id)
                fasthtml_session['auth'] = user.username
                fasthtml_session['user'] = {
                    'name': user.get_display_name(),
                    'email': user.email,
                    'ai_percentage': user.ai_percentage,
                    'id': user.id
                }
            except User.DoesNotExist:
                # User doesn't exist, clear Django session
                django_session.flush()
        
        # If FastHTML has auth but Django doesn't, sync to Django
        elif fasthtml_auth and not django_user_id:
            try:
                user = User.objects.get(username=fasthtml_auth)
                django_session['_auth_user_id'] = str(user.id)
                django_session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
                django_session['_auth_user_hash'] = user.get_session_auth_hash()
                django_session.save()
            except User.DoesNotExist:
                # User doesn't exist, clear FastHTML session
                fasthtml_session.pop('auth', None)
                fasthtml_session.pop('user', None)


def csrf_input(request: Request) -> Input:
    """
    Generate a CSRF token input field for forms.
    
    Args:
        request: The FastHTML/Starlette request object
        
    Returns:
        Hidden input field with CSRF token
    """
    django_session = AuthBridge.get_django_session(request)
    
    # Mock request object for Django's get_token function
    class MockRequest:
        def __init__(self, session):
            self.session = session
            self.META = {}
    
    mock_request = MockRequest(django_session)
    token = get_token(mock_request)
    
    return Input(type="hidden", name="csrfmiddlewaretoken", value=token)
