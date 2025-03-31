"""
Toast notification utilities for the DeadDevelopers application.

This module provides functions for creating and managing toast notifications
with robust error handling to ensure session issues don't disrupt the user experience.
"""

from django.contrib import messages

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

    # Check if session is a dictionary-like object
    if not hasattr(session, '__setitem__') or not hasattr(session, '__getitem__'):
        print(f"Cannot add toast: Session is not a dictionary-like object: {type(session)}")
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

        # Try to save the session if it has a save method
        if hasattr(session, 'save'):
            try:
                session.save()
            except Exception as save_error:
                print(f"Warning: Could not save session after adding toast: {str(save_error)}")
                # Continue anyway, as the toast might still work

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

    # Check if session is a dictionary-like object
    if not hasattr(session, '__getitem__'):
        print(f"Cannot get toasts: Session is not a dictionary-like object: {type(session)}")
        return []

    try:
        # Get toasts from session
        toasts = session.get('toasts', []) if hasattr(session, 'get') else []

        # Clear toasts if requested
        if clear and hasattr(session, '__setitem__') and 'toasts' in session:
            try:
                session['toasts'] = []

                # Try to save the session if it has a save method
                if hasattr(session, 'save'):
                    try:
                        session.save()
                    except Exception as save_error:
                        print(f"Warning: Could not save session after clearing toasts: {str(save_error)}")
                        # Continue anyway, as we've already retrieved the toasts
            except Exception as clear_error:
                print(f"Warning: Could not clear toasts: {str(clear_error)}")
                # Continue anyway, as we've already retrieved the toasts

        return toasts
    except Exception as e:
        # Log the error but don't crash the application
        print(f"Error retrieving toast notifications: {str(e)}")
        return []

def setup_toasts(app):
    """
    Set up toast notifications for the FastHTML app.

    This function adds middleware to the FastHTML app to handle toast notifications.

    Args:
        app: The FastHTML app to set up toasts for
    """
    try:
        # Add middleware to handle toasts - make it the last middleware to run
        # so that session middleware has a chance to initialize first
        @app.middleware('http')  # Use default priority
        def process_toasts(request, call_next):
            """Add toast notifications to the response if available"""
            # Process the request first - do this outside the try block
            # to ensure the request is always processed
            response = call_next(request)

            try:
                # Skip if no session attribute or if session middleware hasn't been initialized
                if not hasattr(request, 'session'):
                    # This is normal for static files and some other routes
                    return response

                # Try to access session safely
                try:
                    # Get toasts from session
                    toasts = get_toasts(request.session)
                except Exception as session_error:
                    # Log the error but continue with the response
                    print(f"Error accessing session for toasts: {str(session_error)}")
                    return response

                # Skip if no toasts or response is not HTML
                if not toasts or not hasattr(response, 'body'):
                    return response

                # Only process HTML responses
                content_type = response.headers.get('content-type', '')
                if 'text/html' not in content_type:
                    return response

                # Get response body as string
                body = response.body.decode('utf-8')

                # Skip if no closing body tag
                if '</body>' not in body:
                    return response

                # Create toast HTML
                toast_html = ""
                for toast in toasts:
                    toast_html += f"""
                    <div class="toast toast-{toast['type']}">
                        <div class="toast-content">
                            <p>{toast['message']}</p>
                        </div>
                        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
                    </div>
                    """

                # Create toast container and script
                toast_container = f"""
                <div class="toast-container">
                    {toast_html}
                </div>
                <script>
                    // Auto-hide toasts after 5 seconds
                    document.addEventListener('DOMContentLoaded', function() {{
                        const toasts = document.querySelectorAll('.toast');
                        toasts.forEach(toast => {{
                            setTimeout(() => {{
                                toast.classList.add('toast-hide');
                                setTimeout(() => {{
                                    toast.remove();
                                }}, 300);
                            }}, 5000);
                        }});

                        // Also auto-hide error messages after 5 seconds
                        const errorMessages = document.querySelectorAll('.error-message');
                        errorMessages.forEach(errorMsg => {{
                            setTimeout(() => {{
                                errorMsg.classList.add('fade-out');
                                setTimeout(() => {{
                                    errorMsg.style.display = 'none';
                                }}, 300);
                            }}, 5000);
                        }});
                    }});
                </script>
                """

                # Add toast container to response body
                modified_body = body.replace('</body>', f'{toast_container}</body>')

                # Create new response with modified body
                from starlette.responses import HTMLResponse
                new_response = HTMLResponse(
                    content=modified_body,
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )

                return new_response
            except Exception as e:
                # Log the error but don't disrupt the response
                print(f"Error processing toast notifications: {str(e)}")
                return response
    except Exception as e:
        # Log the error during setup
        print(f"Error setting up toast notifications: {str(e)}")

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