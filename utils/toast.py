"""
Toast notification utilities for the DeadDevelopers application.

This module provides functions for creating and managing toast notifications
with robust error handling to ensure session issues don't disrupt the user experience.
"""

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

def setup_toasts(app):
    """
    Set up toast notifications for the FastHTML app.
    
    This function adds middleware to the FastHTML app to handle toast notifications.
    
    Args:
        app: The FastHTML app to set up toasts for
    """
    try:
        # Import add_toast to make it available globally
        app.add_global('add_toast', add_toast)
        
        # Add middleware to handle toasts
        @app.middleware('response')
        def process_toasts(request, response):
            """Add toast notifications to the response if available"""
            try:
                # Skip if no session
                if not hasattr(request, 'session'):
                    return response
                
                # Get toasts from session
                toasts = get_toasts(request.session)
                
                # Skip if no toasts or response is not HTML
                if not toasts or not hasattr(response, 'html'):
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
                    }});
                </script>
                """
                
                # Add toast container to response body
                response.html = response.html.replace('</body>', f'{toast_container}</body>')
                
                return response
            except Exception as e:
                # Log the error but don't disrupt the response
                print(f"Error processing toast notifications: {str(e)}")
                return response
    except Exception as e:
        # Log the error during setup
        print(f"Error setting up toast notifications: {str(e)}")

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