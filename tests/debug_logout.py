import sys
from pathlib import Path
import os

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')

# Import Django and FastHTML after setting environment
import django
django.setup()

from fasthtml.core import Client
from main import app

# Import auth routes to ensure they're registered
try:
    from routes.auth import *
except ImportError as e:
    print(f"Warning: Could not import routes.auth: {e}")

def debug_logout_route():
    """Debug the logout route separately"""
    client = Client(app)
    
    # Check the route registration
    print("Available routes:", [route.path for route in app.router.routes])
    
    # Test the logout route
    response = client.get("/logout")
    print(f"Logout response status: {response.status_code}")
    print(f"Logout response headers: {response.headers}")
    
    # Check redirect location
    location = response.headers.get('location')
    print(f"Redirect location: {location}")
    
    # Validate the response
    if response.status_code == 303 and location == '/':
        print("✅ PASS: Logout route correctly redirects to home (/) with status 303")
    else:
        print(f"❌ FAIL: Logout route should redirect to / with status 303, but got status={response.status_code}, location={location}")

if __name__ == "__main__":
    debug_logout_route()
