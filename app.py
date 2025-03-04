from fasthtml.common import *
from pathlib import Path
from starlette.responses import RedirectResponse

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
        Link(rel='stylesheet', href='/css/style.css'),  # Our custom styles
        Link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap'),  # Monospace font
        Script(src='https://cdnjs.cloudflare.com/ajax/libs/prismjs/1.24.1/prism.min.js'),  # Syntax highlighting
        Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/prismjs/1.24.1/themes/prism-tomorrow.min.css'),
    )
)

# Set up toast notifications
setup_toasts(app)
