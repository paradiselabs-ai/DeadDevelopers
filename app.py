from fasthtml.common import *
from pathlib import Path
from starlette.responses import RedirectResponse
import os
import django

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')
django.setup()

# Import Django authentication models and forms after Django setup
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from users.models import User
from users.forms import CustomUserCreationForm

# Status code 303 is a redirect that can change POST to GET
login_redir = RedirectResponse('/login', status_code=303)

def auth_before(req, sess):
    """Beforeware to handle authentication"""
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir

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
        skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', r'.*\.js', r'.*\.png', '/login', '/signup', '/']
    ),
    hdrs=(
        Link(rel='stylesheet', href='/static/css/style.css'),  # Our custom styles
        Link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap'),  # Monospace font
        Script(src='https://cdnjs.cloudflare.com/ajax/libs/prismjs/1.24.1/prism.min.js'),  # Syntax highlighting
        Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/prismjs/1.24.1/themes/prism-tomorrow.min.css'),
        # Add FastHTML-specific components for modern UI
        Style("""
            :root {
                --acid: #00ff66;
                --voltage: #7df9ff;
                --terminal: #1a1a1a;
                --steel: #2b2b2b;
            }
            body {
                font-family: 'JetBrains Mono', monospace;
                background-color: var(--steel);
                color: #fff;
                margin: 0;
                padding: 0;
            }
            .ai-meter {
                width: 100%;
                height: 20px;
                background-color: var(--steel);
                border-radius: 10px;
                overflow: hidden;
                margin-top: 10px;
            }
            .ai-fill {
                height: 100%;
                background-color: var(--acid);
                transition: width 0.5s ease-in-out;
            }
            .htmx-indicator {
                opacity: 0;
                transition: opacity 200ms ease-in;
            }
            .htmx-request .htmx-indicator {
                opacity: 1;
            }
            .htmx-request.htmx-indicator {
                opacity: 1;
            }
        """)
    )
)

# Set up toast notifications
setup_toasts(app)

# Django-FastHTML Authentication Bridge Functions

def django_authenticate(email, password, session):
    """Bridge function to authenticate with Django backend"""
    user = authenticate(email=email, password=password)
    if user is not None:
        # Store user ID in session for Django integration
        session['user_id'] = user.id
        session['auth'] = user.email  # For FastHTML auth system
        
        # Basic user info for the session
        session['user'] = {
            'name': user.get_display_name(),
            'email': user.email,
            'ai_percentage': user.ai_percentage
        }
        return True, user
    return False, None

def django_logout(session):
    """Bridge function to logout from Django backend"""
    if 'user_id' in session:
        del session['user_id']
    if 'auth' in session:
        del session['auth']
    if 'user' in session:
        del session['user']

def django_create_user(form_data, session):
    """Bridge function to create a user with Django backend"""
    form = CustomUserCreationForm(form_data)
    if form.is_valid():
        user = form.save()
        
        # Authenticate the new user
        return django_authenticate(form_data.get('email'), form_data.get('password'), session)
    return False, form

# Import routes
import routes.auth
