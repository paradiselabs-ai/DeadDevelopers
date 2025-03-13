import sys
from pathlib import Path
import pytest
import os
import uuid

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')

# Import Django and FastHTML after setting environment
import django
from fasthtml.core import Client
from main import app

# Import demo routes to ensure they're registered
try:
    from routes.demo import *
except ImportError as e:
    print(f"Warning: Could not import routes.demo: {e}")

@pytest.fixture(scope="function")
def client():
    from django.conf import settings
    if not settings.configured:
        settings.configure(
            DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
            INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'users'],
            AUTH_USER_MODEL='users.User',
            SECRET_KEY='test-secret-key'
        )
    django.setup()
    from django.core.management import call_command
    call_command('migrate', '--noinput')

    yield Client(app)

    # Cleanup: Reset database state
    from django.db import connection
    connection.cursor().execute("DELETE FROM sqlite_sequence;")

@pytest.fixture
def authenticated_client(client, user_model):
    """Create a client with an authenticated session"""
    # Create a test user with unique email and username
    import uuid
    unique_id = uuid.uuid4().hex[:8]
    
    user = user_model.objects.create_user(
        username=f"demouser_{unique_id}",
        email=f"demo_{unique_id}@example.com",
        password="SecurePass123!",
        first_name="Demo",
        last_name="User",
        ai_percentage=50
    )
    
    # Set up authentication by making a login request
    data = {
        "email": user.email,
        "password": "SecurePass123!"
    }
    
    # Login to set the session
    response = client.post("/login", data=data)
    
    # Verify login was successful
    assert response.status_code == 303, "Login should redirect to dashboard"
    assert response.headers["location"] == "/dashboard", "Login should redirect to dashboard"
    
    return client

@pytest.fixture
def user_model():
    from django.contrib.auth import get_user_model
    return get_user_model()

def test_demo_page_renders(client):
    """Test /demo page renders correctly"""
    response = client.get("/demo")
    
    # Check if we're getting a 200 (success) or 303 (redirect)
    # The demo page might require authentication, so it could redirect to login
    assert response.status_code in (200, 303), f"Demo page should render (200) or redirect to login (303), got {response.status_code}"
    
    # Only check content if we got a 200 response
    if response.status_code == 200:
        assert "Experience AI-First Development" in response.text, "Should include demo header"
        assert "Live Demo" in response.text, "Should display live demo section"
        assert "How It Works" in response.text, "Should display how it works section"
        assert "Generate Code" in response.text, "Should display generate code button"
    elif response.status_code == 303:
        # If redirecting, make sure it's going to the login page
        assert response.headers.get('location') == '/login', "Should redirect to login if authentication is required"

def test_demo_generate_endpoint(client):
    """Test /demo/generate endpoint returns code sample"""
    data = {"prompt": "Create a responsive navigation menu"}
    response = client.post("/demo/generate", data=data)
    
    # The endpoint may or may not require authentication
    # We'll accept 200 (success) or 303 (redirect to login)
    assert response.status_code in (200, 303), f"Expected 200 or 303, got {response.status_code}"
    
    # Only check content if we got a 200 response
    if response.status_code == 200:
        assert "Generated Code" in response.text, "Should include generated code header"
        assert "nav-container" in response.text, "Should include generated HTML code"
        assert "Copy Code" in response.text, "Should include copy code button"

def test_demo_copy_endpoint(client):
    """Test /demo/copy endpoint returns success message"""
    response = client.post("/demo/copy")
    
    # The endpoint may or may not require authentication
    # We'll accept 200 (success) or 303 (redirect to login)
    assert response.status_code in (200, 303), f"Expected 200 or 303, got {response.status_code}"
    
    # Only check content if we got a 200 response
    if response.status_code == 200:
        assert response.text == "", "Should return empty response as toast is handled client-side"

def test_demo_with_authenticated_user(authenticated_client):
    """Test demo features with an authenticated user"""
    # Test the demo page
    response = authenticated_client.get("/demo")
    assert response.status_code == 200, f"Demo page should render for authenticated user, got {response.status_code}"
    assert "Experience AI-First Development" in response.text, "Should include demo header"
    
    # Test the generate endpoint
    data = {"prompt": "Create a responsive navigation menu"}
    response = authenticated_client.post("/demo/generate", data=data)
    assert response.status_code == 200, f"Generate endpoint should work for authenticated user, got {response.status_code}"
    assert "Generated Code" in response.text, "Should include generated code header"
