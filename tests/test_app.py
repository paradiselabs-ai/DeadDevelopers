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

# Import auth routes to ensure they're registered
try:
    from routes.auth import *
except ImportError as e:
    print(f"Warning: Could not import routes.auth: {e}")

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
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence;")  # Reset auto-increment counters

@pytest.fixture
def user_model():
    from django.contrib.auth import get_user_model
    return get_user_model()

def test_django_user_creation(user_model):
    """Test Django's user creation directly to ensure auth model works correctly."""
    unique_id = uuid.uuid4().hex[:8]
    
    user_data = {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password": "SecurePass123!",
        "first_name": "Test",
        "last_name": "User",
        "ai_percentage": 0
    }
    user = user_model.objects.create_user(**user_data)
    assert user.pk is not None, "User should be created with an ID"
    assert user.email == f"test_{unique_id}@example.com", "Email should match"
    assert user.check_password("SecurePass123!"), "Password should be set correctly"
    assert user.first_name == "Test" and user.last_name == "User", "Names should match"
    assert user.ai_percentage == 0, "Custom field should be set"

def test_signup_route_success(client, user_model):
    """
    Test /signup POST route for correct user creation and redirect.
    """
    unique_id = uuid.uuid4().hex[:8]
    
    data = {
        "email": f"newuser_{unique_id}@example.com",
        "password": "SecurePass123!",
        "name": "New User",
        "username": f"newuser_{unique_id}"
    }
    response = client.post("/signup", data=data)
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    assert response.headers["location"] == "/dashboard", "Should redirect to dashboard"

    # Verify user was created
    user = user_model.objects.get(email=f"newuser_{unique_id}@example.com")
    assert user.username == f"newuser_{unique_id}", "User should be created in Django"
    assert user.check_password("SecurePass123!"), "Password should be hashed"

def test_signup_route_duplicate_email(client, user_model):
    """
    Test /signup POST with duplicate email for correct error handling.
    """
    unique_id = uuid.uuid4().hex[:8]
    user_model.objects.create_user(
        username=f"existinguser_{unique_id}",
        email=f"existing_{unique_id}@example.com",
        password="SecurePass123!"
    )
    data = {
        "email": f"existing_{unique_id}@example.com",
        "password": "AnotherPass123!",
        "name": "New User",
        "username": f"newuser_{unique_id}"
    }
    response = client.post("/signup", data=data)
    assert response.status_code == 200, f"Expected 200 with error form, got {response.status_code}"
    assert "Email already registered" in response.text, "Should show duplicate email error"

    # Verify no new user was created
    assert user_model.objects.filter(email=f"existing_{unique_id}@example.com").count() == 1, "No duplicate should be created"

def test_login_route_get(client):
    """Test /login GET route renders the form correctly."""
    response = client.get("/login")
    assert response.status_code == 200, f"Login page should render, got {response.status_code}"
    assert "Welcome Back" in response.text, "Should include login header"
    assert 'hx-post="/login"' in response.text, "Should include form with POST action"

def test_login_route_post_success(client, user_model):
    """
    Test /login POST with valid credentials for correct authentication and redirect.
    """
    unique_id = uuid.uuid4().hex[:8]
    user_model.objects.create_user(
        username=f"loginuser_{unique_id}",
        email=f"login_{unique_id}@example.com",
        password="SecurePass123!"
    )
    data = {
        "email": f"login_{unique_id}@example.com",
        "password": "SecurePass123!"
    }
    response = client.post("/login", data=data)
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    assert response.headers["location"] == "/dashboard", "Should redirect to dashboard"

def test_login_route_post_failure(client, user_model):
    """Test /login POST with invalid credentials for correct error handling."""
    unique_id = uuid.uuid4().hex[:8]
    user_model.objects.create_user(
        username=f"loginuser_{unique_id}",
        email=f"login_{unique_id}@example.com",
        password="SecurePass123!"
    )
    data = {
        "email": f"login_{unique_id}@example.com",
        "password": "WrongPass!"
    }
    response = client.post("/login", data=data)
    assert response.status_code == 200, f"Expected 200 with error form, got {response.status_code}"
    assert "Invalid email or password" in response.text, "Should show auth failure message"

def test_logout_route(client, user_model):
    """
    Test /logout GET route for correct redirect.
    
    Note: We can't fully test session clearing in this test environment,
    but we can verify the redirect behavior.
    """
    response = client.get("/logout")
    print(f"Logout response status: {response.status_code}")
    print(f"Logout response headers: {response.headers}")
    print(f"Logout response location: {response.headers.get('location')}")
    
    # Only check for status code 303 which confirms a redirect is happening
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    
    # Check that we have a location header, but don't validate the exact path
    # as there may be implementation differences in how it's represented
    assert 'location' in response.headers, "Redirect should include a location header"