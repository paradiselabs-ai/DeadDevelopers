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

from fasthtml.core import Client, App
from starlette.responses import RedirectResponse

# Create a simple app with a logout route
app = App()

@app.route('/test-logout')
def get(req):
    """Simple test logout route"""
    print("Test logout route called")
    return RedirectResponse('/', status_code=303)

def test_redirect():
    """Test the redirect behavior of the client"""
    client = Client(app)
    
    response = client.get("/test-logout")
    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Location header: {response.headers.get('location')}")
    
    # Assert the response
    assert response.status_code == 303, f"Expected 303, got {response.status_code}"
    assert response.headers["location"] == "/", f"Expected /, got {response.headers.get('location')}"
    
    print("✅ Test passed!")

if __name__ == "__main__":
    test_redirect()
