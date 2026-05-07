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
import time

# Import Django models and functionality
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import connection
from auth_bridge import AuthBridge

User = get_user_model()

# Check database migrations on startup
def check_migrations():
    """Verify that all database migrations have been applied"""
    try:
        connection.ensure_connection()
        # This will raise an exception if migrations are not up to date
        call_command('migrate', '--check', verbosity=0)
        print("✓ Database migrations are up to date")
    except Exception as e:
        print(f"⚠️  Database migrations need to run: {e}")
        print("Run: python manage.py migrate")
        sys.exit(1)

# Only check migrations in production or when explicitly enabled
if not os.getenv('SKIP_MIGRATION_CHECK'):
    check_migrations()

# Status code 303 is a redirect that can change POST to GET
login_redir = RedirectResponse('/login', status_code=303)

def auth_before(req, sess):
    """Beforeware to handle authentication with AuthBridge synchronization"""
    # Synchronize FastHTML and Django sessions
    AuthBridge.sync_sessions(req, sess)
    
    # Get current user from unified auth system
    user = AuthBridge.get_current_user(req, sess)
    
    # Set auth in request scope
    req.scope['auth'] = sess.get('auth', None)
    
    # If user is authenticated, allow access
    if user:
        return None
    
    # No auth, redirect to login
    return login_redir

# Import Django API for mounting
from api_mount import django_app

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
        skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', r'.*\.js', r'.*\.png', '/login', '/signup', '/', '/features', '/community', '/blog', '/about', r'/accounts/confirm-email.*', r'/profile/[^/]+$']
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

# Set up toast notifications
setup_toasts(app)

# ASGI dispatcher: /api/* and /admin/* go to Django with the full path
# preserved so django_config/urls.py and Django's URL reversing both work.
# (Starlette's Mount strips its prefix, which breaks the urlconf.)
_fastapp = app

async def app(scope, receive, send):
    if scope['type'] in ('http', 'websocket'):
        path = scope.get('path', '')
        if path.startswith('/api/') or path.startswith('/admin/'):
            await django_app(scope, receive, send)
            return
    await _fastapp(scope, receive, send)
