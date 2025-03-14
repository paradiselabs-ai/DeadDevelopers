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

# Initialize FastHTML app with WebSocket support
app, rt = fast_app(
    exts='ws',  # Enable WebSocket support
    debug=True,  # Enable debug mode during development
    pico=True,  # Use Pico CSS for styling
    surreal=True,  # Enable Surreal.js for enhanced interactivity
    htmx=True,  # Enable HTMX for dynamic updates
    static_path=Path('static'),  # Set static files directory
    before=Beforeware(
        auth_before,
        skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', r'.*\.js', r'.*\.png', '/login', '/signup', '/', '/features', '/community', '/blog']
    ),
    hdrs=(
        Link(rel='stylesheet', href='/css/style.css'),  # Our custom styles
        Link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap'),  # Monospace font
        Script(src='https://cdnjs.cloudflare.com/ajax/libs/prismjs/1.24.1/prism.min.js'),  # Syntax highlighting
        Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/prismjs/1.24.1/themes/prism-tomorrow.min.css'),
        Script(src='/js/nav.js'),  # Custom navigation JavaScript
    )
)

# Set up toast notifications
setup_toasts(app)
