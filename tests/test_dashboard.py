import sys
from pathlib import Path
import pytest
import os
from bs4 import BeautifulSoup

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')

# Import Django and FastHTML after setting environment
import django
from fasthtml.core import Client
from main import app

# Import dashboard routes to ensure they're registered
try:
    from routes.dashboard import *
except ImportError as e:
    print(f"Warning: Could not import routes.dashboard: {e}")

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
        username=f"dashboarduser_{unique_id}",
        email=f"dashboard_{unique_id}@example.com",
        password="SecurePass123!",
        first_name="Dashboard",
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

def test_dashboard_unauthenticated(client):
    """Test /dashboard redirects to login for unauthenticated users"""
    response = client.get("/dashboard")
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    assert response.headers["location"] == "/login", "Should redirect to login"

def test_dashboard_authenticated_structure(authenticated_client):
    """Test that the dashboard page has the correct structural elements for authenticated users."""
    response = authenticated_client.get("/dashboard")
    assert response.status_code == 200, f"Dashboard should render, got {response.status_code}"
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # More flexible header check
    header = (
        soup.find('header') or 
        soup.find(['div', 'nav', 'section'], class_=lambda c: c and ('header' in c.lower() or 'nav' in c.lower()))
    )
    assert header is not None, "Dashboard should have a header or navigation element"
    
    # More flexible container check
    main_container = (
        soup.find('main') or 
        soup.find(['div', 'section'], id=lambda i: i and 'dashboard' in i.lower()) or
        soup.find(['div', 'section'], class_=lambda c: c and ('dashboard' in c.lower() or 'container' in c.lower() or 'content' in c.lower()))
    )
    assert main_container is not None, "Dashboard should have a main container element"
    
    # More flexible project section check - using contains for text content search
    has_project_section = False
    for tag in soup.find_all(['div', 'section', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        if tag.string and 'project' in tag.string.lower():
            has_project_section = True
            break
    
    assert has_project_section, "Dashboard should mention projects somewhere"
    
    # Look for user-related information
    has_user_info = False
    user_element = soup.find(['div', 'span', 'p', 'h1', 'h2', 'h3', 'h4'], string=lambda s: s and ('dashboard' in s.lower() or 'user' in s.lower() or 'welcome' in s.lower()))
    if user_element:
        has_user_info = True
    
    assert has_user_info, "Dashboard should display some form of user information"

def test_new_project_unauthenticated(client):
    """Test /dashboard/new-project redirects to login for unauthenticated users"""
    response = client.get("/dashboard/new-project")
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    assert response.headers["location"] == "/login", "Should redirect to login"

def test_new_project_form_structure(authenticated_client):
    """Test that the new project form has the correct structural elements."""
    response = authenticated_client.get("/dashboard/new-project")
    assert response.status_code == 200, f"New project form should render, got {response.status_code}"
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Test that the form exists
    form = soup.find('form')
    assert form is not None, "Page should have a form for creating a new project"
    
    # Test for required form fields - more flexibly
    name_field = (
        soup.find('input', attrs={'name': 'name'}) or 
        soup.find('input', attrs={'id': 'name'}) or
        soup.find('textarea', attrs={'name': 'name'})
    )
    assert name_field is not None, "Form should have a name field"
    
    description_field = (
        soup.find('input', attrs={'name': 'description'}) or 
        soup.find('input', attrs={'id': 'description'}) or
        soup.find('textarea', attrs={'name': 'description'})
    )
    assert description_field is not None, "Form should have a description field"
    
    # Test for submit button - more flexibly
    submit_button = (
        soup.find('button', attrs={'type': 'submit'}) or 
        soup.find('input', attrs={'type': 'submit'}) or
        soup.find('button', string=lambda s: s and ('create' in s.lower() or 'submit' in s.lower() or 'save' in s.lower())) or
        soup.find('button', attrs={'id': lambda i: i and ('submit' in i.lower() or 'save' in i.lower())})
    )
    assert submit_button is not None, "Form should have a submit button"

def test_create_project_unauthenticated(client):
    """Test /dashboard/create-project redirects to login for unauthenticated users"""
    data = {
        "name": "Test Project",
        "description": "A project created in tests"
    }
    response = client.post("/dashboard/create-project", data=data)
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    assert response.headers["location"] == "/login", "Should redirect to login"

def test_create_project_authenticated(authenticated_client):
    """Test /dashboard/create-project creates a project and redirects to dashboard."""
    data = {
        "name": "Test Project",
        "description": "A project created in tests"
    }
    response = authenticated_client.post("/dashboard/create-project", data=data)
    
    # The app might either redirect or return a 200 with updated content - accept both
    assert response.status_code in [200, 302, 303], f"Expected success or redirect, got {response.status_code}"
    
    # If it's a redirect, it should go to the dashboard
    if response.status_code in [302, 303]:
        assert "/dashboard" in response.headers.get("location", ""), "Should redirect to dashboard"
        # Make a follow-up request to get the dashboard content
        dashboard_response = authenticated_client.get("/dashboard")
        assert "Test Project" in dashboard_response.text, "Dashboard should show the created project"
    else:
        # If it's a 200, the project should be shown in the response
        assert "Test Project" in response.text, "Response should include the created project"
