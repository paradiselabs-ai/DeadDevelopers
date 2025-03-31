"""
Custom session middleware for FastHTML.

This middleware ensures that sessions are properly handled in the FastHTML application.
"""
from starlette.middleware.sessions import SessionMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send

class CustomSessionMiddleware:
    """
    Custom session middleware that ensures sessions are properly initialized.
    
    This middleware wraps the Starlette SessionMiddleware and adds additional
    error handling and debugging.
    """
    
    def __init__(self, app: ASGIApp, secret_key: str, session_cookie: str = "session", 
                 max_age: int = 14 * 24 * 60 * 60, # 14 days in seconds
                 same_site: str = "lax", https_only: bool = False):
        """
        Initialize the custom session middleware.
        
        Args:
            app: The ASGI application
            secret_key: Secret key for signing the session cookie
            session_cookie: Name of the session cookie
            max_age: Maximum age of the session cookie in seconds
            same_site: SameSite attribute for the cookie
            https_only: Whether the cookie should only be sent over HTTPS
        """
        self.app = app
        # Create the standard Starlette SessionMiddleware
        self.session_middleware = SessionMiddleware(
            app=app,
            secret_key=secret_key,
            session_cookie=session_cookie,
            max_age=max_age,
            same_site=same_site,
            https_only=https_only
        )
        
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """
        Process an ASGI request with session handling.
        
        Args:
            scope: The ASGI scope
            receive: The ASGI receive function
            send: The ASGI send function
        """
        # Skip non-HTTP requests
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
            
        # Add a session dictionary to the scope if it doesn't exist
        if "session" not in scope:
            scope["session"] = {}
            
        try:
            # Use the standard SessionMiddleware to handle the session
            await self.session_middleware(scope, receive, send)
        except Exception as e:
            # Log the error but don't crash the application
            print(f"Session middleware error: {str(e)}")
            # Fall back to the application without session handling
            await self.app(scope, receive, send)