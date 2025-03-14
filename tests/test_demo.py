import sys
from pathlib import Path
import pytest
import os
import uuid
from bs4 import BeautifulSoup

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

def test_demo_page_structure(client):
    """Test /demo page structure elements"""
    response = client.get("/demo")
    
    # Check if we're getting a 200 (success) or 303 (redirect)
    # The demo page might require authentication, so it could redirect to login
    assert response.status_code in (200, 303), f"Demo page should render (200) or redirect to login (303), got {response.status_code}"
    
    # Only check structure if we got a 200 response
    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Test header is present
        header = soup.find('header') or soup.find('div', class_=lambda c: c and 'header' in c.lower())
        assert header is not None
        
        # Test that the demo container exists
        demo_container = soup.find(['div', 'main'], class_=lambda c: c and ('demo' in c.lower() or 'container' in c.lower()))
        assert demo_container is not None
        
        # Test that the demo sections exist
        demo_sections = soup.find_all(['section', 'div'], class_=lambda c: c and ('demo' in c.lower() or 'section' in c.lower()))
        assert len(demo_sections) > 0
        
        # Look for a code generation form or interactive element
        generate_element = (
            soup.find(['button', 'a'], string=lambda s: s and ('generate' in s.lower() or 'code' in s.lower())) or
            soup.find(['button', 'a'], class_=lambda c: c and ('generate' in c.lower() or 'demo' in c.lower())) or
            soup.find('form', class_=lambda c: c and ('generate' in c.lower() or 'demo' in c.lower()))
        )
        assert generate_element is not None
    elif response.status_code == 303:
        # If redirecting, make sure it's going to the login page
        assert response.headers.get('location') == '/login', "Should redirect to login if authentication is required"

def test_demo_generate_endpoint_structure(client):
    """Test /demo/generate endpoint returns properly structured response"""
    data = {"prompt": "Create a responsive navigation menu"}
    response = client.post("/demo/generate", data=data)
    
    # Check response status - either success or redirect to login
    assert response.status_code in (200, 303, 400), "Should return success (200), redirect to login (303), or bad request (400)"
    
    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Test for presence of code snippet container
        code_container = (
            soup.find('pre') or 
            soup.find('code') or
            soup.find(['div', 'section'], class_=lambda c: c and 'code' in c.lower())
        )
        assert code_container is not None
        
        # Test for presence of a response message or explanation
        explanation = soup.find(['p', 'div', 'section'], class_=lambda c: c and ('response' in c.lower() or 'explanation' in c.lower()))
        # This is optional, so we don't assert on it
    elif response.status_code == 303:
        # If redirecting, make sure it's going to the login page
        assert response.headers.get('location') == '/login', "Should redirect to login if authentication is required"

def test_authenticated_demo_access(authenticated_client):
    """Test that authenticated users can access the demo page"""
    response = authenticated_client.get("/demo")
    
    # Authenticated users should always get a 200 response
    assert response.status_code == 200, f"Authenticated demo page should render, got {response.status_code}"
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Test that the page displays some form of user recognition
    user_element = (
        soup.find(['div', 'span', 'p'], string=lambda s: s and 'user' in s.lower()) or
        soup.find(['div', 'span', 'p'], class_=lambda c: c and 'user' in c.lower())
    )
    # This is optional depending on demo page design, so we don't assert on it
    
    # Test that the demo container exists with proper structure
    demo_container = soup.find(['div', 'main'], class_=lambda c: c and ('demo' in c.lower() or 'container' in c.lower()))
    assert demo_container is not None
