import os
import sys
from pathlib import Path

# Initialize Django settings first - before any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')

# Add the current directory to the Python path if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialize Django
import django
django.setup()

# Now that Django is properly configured, we can import the rest
from fasthtml.common import *
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
import time

# Import our custom session middleware
from middleware import CustomSessionMiddleware

# Import Django models and functionality
from django.contrib.auth import get_user_model
User = get_user_model()

# Status code 303 is a redirect that can change POST to GET
login_redir = RedirectResponse('/login', status_code=303)

def auth_before(req, sess):
    """Beforeware to handle authentication"""
    # Set auth in request scope from session
    auth = req.scope['auth'] = sess.get('auth', None)
    
    # If auth is present in session, ensure user data is also available
    if auth:
        # Ensure user data is in session
        if 'user' not in sess:
            try:
                # Try to get user from Django
                user = User.objects.get(username=auth)
                sess['user'] = {
                    'name': user.get_display_name(),
                    'email': user.email,
                    'ai_percentage': user.ai_percentage
                }
            except User.DoesNotExist:
                # If user doesn't exist, clear auth
                del sess['auth']
                return login_redir
        return None
    
    # No auth in session, redirect to login
    return login_redir

# Define middleware with our custom session middleware
middleware = [
    Middleware(
        CustomSessionMiddleware,
        secret_key="deaddevs-secret-key-change-in-production",
        session_cookie="deaddevs_session",
        max_age=14 * 24 * 60 * 60,  # 14 days in seconds
        same_site="lax",
        https_only=False
    )
]

# Initialize FastHTML app with WebSocket support
app, rt = fast_app(
    exts='ws',  # Enable WebSocket support
    debug=True,  # Enable debug mode during development
    pico=True,  # Use Pico CSS for styling
    surreal=True,  # Enable Surreal.js for enhanced interactivity
    htmx=True,  # Enable HTMX for dynamic updates
    static_path=Path('static'),  # Set static files directory
    middleware=middleware,  # Use our custom middleware
    before=Beforeware(
        auth_before,
        skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', r'.*\.js', r'.*\.png', '/login', '/signup', '/', '/features', '/community', '/blog', '/about', r'/accounts/confirm-email.*', '/chat_send']
    ),
    hdrs=(
        # Add timestamp query parameter to bust cache
        Link(rel='stylesheet', href=f'/css/style.css?v={int(time.time())}'),  # Our custom styles with cache busting
        Link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap'),  # Monospace font
        # Prism.js for syntax highlighting
        Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-tomorrow.min.css'),
        Script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/prism.min.js'),
        Script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-markup.min.js'),
        Script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-css.min.js'),
        Script(src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-javascript.min.js'),
        Script(src='/js/header.js'),  # Custom navigation JavaScript
    )
)

# Import our simplified toast implementation
from utils.toast_helper import add_toast

# Make add_toast available globally
globals()['add_toast'] = add_toast
