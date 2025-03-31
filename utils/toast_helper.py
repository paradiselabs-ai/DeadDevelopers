"""
Simplified toast notification utilities for the DeadDevelopers application.

This module provides functions for creating and managing toast notifications
that work directly with FastHTML's components rather than using middleware.
"""

from django.contrib import messages

class RequestWrapper:
    """
    Wrapper for FastHTML request objects to provide Django-compatible methods.

    This wrapper adds the build_absolute_uri method that Django expects but
    FastHTML requests don't have, and handles Django messages.
    """
    def __init__(self, original_request):
        self.original_request = original_request
        # Django's message framework expects this
        self._messages = messages.storage.default_storage(self)

    def build_absolute_uri(self, path):
        """Build an absolute URI from the given path."""
        # Get the host from the original request
        host = self.original_request.headers.get('host', 'localhost:8000')
        scheme = 'https' if self.original_request.headers.get('x-forwarded-proto') == 'https' else 'http'
        return f"{scheme}://{host}{path}"

    # Django message framework compatibility
    def is_secure(self):
        """Check if the request is secure (HTTPS)."""
        return self.original_request.headers.get('x-forwarded-proto') == 'https'

    def get_host(self):
        """Get the host from the request."""
        return self.original_request.headers.get('host', 'localhost:8000')

    @property
    def session(self):
        """Get the session from the original request."""
        return self.original_request.session

    @property
    def META(self):
        """Provide META dict that Django expects."""
        meta = {}
        for key, value in self.original_request.headers.items():
            meta[f'HTTP_{key.upper().replace("-", "_")}'] = value
        return meta

    def __getattr__(self, name):
        """Pass through any other attributes to the original request."""
        return getattr(self.original_request, name)

def add_toast(session, message, toast_type="info"):
    """
    Add a toast notification to the session with robust error handling.
    
    Args:
        session: The session object to store the toast in
        message: The message to display in the toast
        toast_type: The type of toast (info, success, warning, error)
        
    Returns:
        bool: True if toast was added successfully, False otherwise
    """
    # Check if session is None or not a valid session object
    if session is None:
        print("Cannot add toast: Session is None")
        return False
        
    try:
        # Initialize toasts list if it doesn't exist
        if 'toasts' not in session:
            session['toasts'] = []
            
        # Validate toast_type
        valid_types = ["info", "success", "warning", "error"]
        if toast_type not in valid_types:
            toast_type = "info"  # Default to info if invalid type
            
        # Add toast to session
        session['toasts'].append({
            'message': str(message),
            'type': toast_type
        })
        
        return True
    except Exception as e:
        # Log the error but don't crash the application
        print(f"Error adding toast notification: {str(e)}")
        return False

def get_toasts(session, clear=True):
    """
    Get all toast notifications from the session with error handling.
    
    Args:
        session: The session object containing the toasts
        clear: Whether to clear the toasts after retrieving them
        
    Returns:
        list: List of toast notifications or empty list if none or error
    """
    # Check if session is None or not a valid session object
    if session is None:
        print("Cannot get toasts: Session is None")
        return []
        
    try:
        # Get toasts from session
        toasts = session.get('toasts', [])
        
        # Clear toasts if requested
        if clear and 'toasts' in session:
            session['toasts'] = []
            
        return toasts
    except Exception as e:
        # Log the error but don't crash the application
        print(f"Error retrieving toast notifications: {str(e)}")
        return []

def render_toasts(session):
    """
    Render toast notifications as a FastHTML component.

    Args:
        session: The session object containing the toasts

    Returns:
        str or None: FastHTML component for toast notifications or None if none
    """
    from fasthtml.common import Div, P, Script

    try:
        # Get toasts from session
        toasts = get_toasts(session)

        # Skip if no toasts
        if not toasts:
            return None

        # Create toast elements
        toast_elements = []
        for toast in toasts:
            # Handle different formats of toast data
            if isinstance(toast, dict) and 'message' in toast and 'type' in toast:
                # Standard format with message and type keys
                message = toast['message']
                toast_type = toast['type']
            elif isinstance(toast, dict) and len(toast) > 0:
                # Dictionary but with different keys
                message = next(iter(toast.values()))
                toast_type = "info"
            elif isinstance(toast, (str, int, float)):
                # Simple string or number
                message = str(toast)
                toast_type = "info"
            else:
                # Unknown format, use a default message
                message = "Notification"
                toast_type = "info"

            # Use a button element directly instead of Raw
            toast_elements.append(
                Div(
                    Div(
                        P(message),
                        cls="toast-content"
                    ),
                    Div(
                        "×",
                        cls="toast-close",
                        onclick="this.parentElement.remove()"
                    ),
                    cls=f"toast toast-{toast_type}"
                )
            )

        # Create auto-hide script
        auto_hide_script = """
        // Auto-hide toasts after 5 seconds
        document.addEventListener('DOMContentLoaded', function() {
            const toasts = document.querySelectorAll('.toast');
            toasts.forEach(toast => {
                setTimeout(() => {
                    toast.classList.add('toast-hide');
                    setTimeout(() => {
                        toast.remove();
                    }, 300);
                }, 5000);
            });

            // Also auto-hide error messages after 5 seconds
            const errorMessages = document.querySelectorAll('.error-message');
            errorMessages.forEach(errorMsg => {
                setTimeout(() => {
                    errorMsg.classList.add('fade-out');
                    setTimeout(() => {
                        errorMsg.style.display = 'none';
                    }, 300);
                }, 5000);
            });
        });
        """

        # Return toast container with all toasts and script
        return Div(
            *toast_elements,
            Script(auto_hide_script),
            cls="toast-container"
        )
    except Exception as e:
        # Log the error but don't crash the application
        print(f"Error rendering toast notifications: {str(e)}")
        return None

def handle_session_safely(session, action_func, default_value=None, log_prefix="Session operation"):
    """
    Safely handle session operations with proper error handling.

    Args:
        session: The session object to operate on
        action_func: A function that performs the session operation
        default_value: Value to return if operation fails
        log_prefix: Prefix for error logging

    Returns:
        The result of action_func or default_value if an error occurs
    """
    try:
        return action_func(session)
    except Exception as e:
        print(f"{log_prefix} error: {str(e)}")
        return default_value