import sys
from pathlib import Path
import pytest
import os

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

def test_dashboard_authenticated(authenticated_client):
    """Test /dashboard displays correctly for authenticated users"""
    response = authenticated_client.get("/dashboard")
    assert response.status_code == 200, f"Dashboard should render, got {response.status_code}"
    assert "Dashboard - Dashboard User" in response.text, "Should include user's name"
    assert "50%" in response.text, "Should show AI usage percentage"
    assert "Your Projects" in response.text, "Should display projects section"
    assert "AI Assistant" in response.text, "Should display AI assistant section"

def test_new_project_unauthenticated(client):
    """Test /dashboard/new-project redirects to login for unauthenticated users"""
    response = client.get("/dashboard/new-project")
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    assert response.headers["location"] == "/login", "Should redirect to login"

def test_new_project_authenticated(authenticated_client):
    """Test /dashboard/new-project displays form for authenticated users"""
    response = authenticated_client.get("/dashboard/new-project")
    assert response.status_code == 200, f"New project form should render, got {response.status_code}"
    assert "Create New Project" in response.text, "Should display project form"
    assert 'name="name"' in response.text, "Should include project name field"
    assert 'name="description"' in response.text, "Should include project description field"

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
    """Test /dashboard/create-project creates a project for authenticated users"""
    data = {
        "name": "Test Project",
        "description": "A project created in tests"
    }
    response = authenticated_client.post("/dashboard/create-project", data=data)
    assert response.status_code == 200, f"Expected 200 with project card, got {response.status_code}"
    assert "Test Project" in response.text, "Should include project name"
    assert "A project created in tests" in response.text, "Should include project description"

def test_ask_ai_unauthenticated(client):
    """Test /dashboard/ask redirects to login for unauthenticated users"""
    data = {"query": "How do I optimize my code?"}
    response = client.post("/dashboard/ask", data=data)
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    assert response.headers["location"] == "/login", "Should redirect to login"

def test_ask_ai_authenticated(authenticated_client):
    """Test /dashboard/ask returns AI response for authenticated users"""
    data = {"query": "How do I optimize my code?"}
    response = authenticated_client.post("/dashboard/ask", data=data)
    assert response.status_code == 200, f"Expected 200 with AI response, got {response.status_code}"
    assert "AI Assistant Response" in response.text, "Should include response header"
    assert "performance" in response.text, "Should include performance-related content"
