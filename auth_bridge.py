"""
Authentication Bridge for FastHTML and Django

This module provides a unified authentication layer that synchronizes
FastHTML sessions with Django's authentication system, solving the
dual-session management problem.
"""

from typing import Optional
from asgiref.sync import sync_to_async
from django.conf import settings as django_settings
from django.contrib.auth import get_user_model, authenticate, login as django_login, logout as django_logout
from django.contrib.sessions.backends.db import SessionStore
from django.middleware.csrf import get_token
from fasthtml.common import *
from starlette.requests import Request
from starlette.responses import Response

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

        The session is cached on the request object so a single request
        always sees the same SessionStore (same session_key). Without this
        cache, login_user() would create one session_key and the cookie
        helper would create a second different one — leaving the client
        with a cookie that points to an empty session.

        Args:
            request: The FastHTML/Starlette request object

        Returns:
            Django SessionStore instance
        """
        # `isinstance` guard: Mock-based test fixtures return a Mock for
        # any attribute, so a plain truthy check would loop back into a
        # bogus cache. Only honour real SessionStore instances.
        cached = getattr(request, '_dd_django_session', None)
        if isinstance(cached, SessionStore):
            return cached

        cookie_name = getattr(django_settings, 'SESSION_COOKIE_NAME', 'sessionid')
        session_key = request.cookies.get(cookie_name)
        session = SessionStore(session_key=session_key)

        if not session.exists(session.session_key):
            session.create()

        try:
            setattr(request, '_dd_django_session', session)
        except (AttributeError, TypeError):
            # Some request implementations are slot-based; just skip caching.
            pass
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

    @staticmethod
    def apply_session_cookie(response: Response, request: Request) -> Response:
        """Stamp the Django sessionid cookie onto a FastHTML response.

        FastHTML keeps its own session cookie ('session_'). DRF /api/* routes
        and any other Django-mounted view authenticate against Django's
        sessionid cookie. AuthBridge.login_user() saves the Django session
        server-side, but the cookie never reaches the client unless we set
        it on the response — Django's SessionMiddleware doesn't run for
        FastHTML routes.

        Call this on every response that comes after AuthBridge.login_user
        or .logout_user — it makes Django session-auth (and therefore DRF
        SessionAuthentication) work cross-origin between the FastHTML and
        Django sides of the app.
        """
        django_session = AuthBridge.get_django_session(request)
        cookie_name = getattr(django_settings, 'SESSION_COOKIE_NAME', 'sessionid')

        if django_session.session_key:
            response.set_cookie(
                cookie_name,
                django_session.session_key,
                max_age=getattr(django_settings, 'SESSION_COOKIE_AGE', 1209600),
                httponly=True,
                samesite=getattr(django_settings, 'SESSION_COOKIE_SAMESITE', 'Lax'),
                secure=getattr(django_settings, 'SESSION_COOKIE_SECURE', False),
                path=getattr(django_settings, 'SESSION_COOKIE_PATH', '/'),
                domain=getattr(django_settings, 'SESSION_COOKIE_DOMAIN', None),
            )
        else:
            # Logout path — clear the cookie so DRF/Django stop seeing the user.
            response.delete_cookie(cookie_name)
        return response


# Async variants of the sync class methods. Django 6 forbids calling sync
# ORM from an async context — these wrappers let `async def post` route
# handlers do `await AuthBridge.aget_current_user(req, session)` without
# tripping SynchronousOnlyOperation.
AuthBridge.aget_current_user = staticmethod(sync_to_async(AuthBridge.get_current_user))
AuthBridge.async_sessions     = staticmethod(sync_to_async(AuthBridge.sync_sessions))
AuthBridge.alogin_user        = staticmethod(sync_to_async(AuthBridge.login_user))
AuthBridge.alogout_user       = staticmethod(sync_to_async(AuthBridge.logout_user))


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
