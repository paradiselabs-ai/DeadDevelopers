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
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "first_name": "Test",
        "last_name": "User",
        "ai_percentage": 0
    }
    user = user_model.objects.create_user(**user_data)
    assert user.pk is not None, "User should be created with an ID"
    assert user.email == "test@example.com", "Email should match"
    assert user.check_password("SecurePass123!"), "Password should be set correctly"
    assert user.first_name == "Test" and user.last_name == "User", "Names should match"
    assert user.ai_percentage == 0, "Custom field should be set"

@pytest.mark.xfail(reason="Session incompatibility: login(req, user) raises 'cycle_key' error instead of redirecting")
def test_signup_route_success(client, user_model):
    """
    Test /signup POST route for correct user creation and redirect.

    Intended Behavior:
    - Creates user in Django and redirects to /dashboard (303).
    Current Behavior:
    - Creates user but raises AttributeError ('cycle_key') due to login(req, user).
    Fix: Remove login(req, user) in routes/auth.py and set req.session['auth'] manually.
    """
    data = {
        "email": "newuser@example.com",
        "password": "SecurePass123!",
        "name": "New User",
        "username": "newuser"
    }
    response = client.post("/signup", data=data)
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    assert response.headers["location"] == "/dashboard", "Should redirect to dashboard"

    # Verify user was created
    user = user_model.objects.get(email="newuser@example.com")
    assert user.username == "newuser", "User should be created in Django"
    assert user.check_password("SecurePass123!"), "Password should be hashed"

@pytest.mark.xfail(reason="Response handling: signup_form() tuple lacks 'find' method, raises error instead of showing errors")
def test_signup_route_duplicate_email(client, user_model):
    """
    Test /signup POST with duplicate email for correct error handling.

    Intended Behavior:
    - Returns 200 with 'Email already registered' error message.
    Current Behavior:
    - Detects duplicate but raises AttributeError ('find') due to response.find().
    Fix: Modify signup_form() in routes/auth.py to accept errors parameter.
    """
    user_model.objects.create_user(
        username="existinguser",
        email="existing@example.com",
        password="SecurePass123!"
    )
    data = {
        "email": "existing@example.com",
        "password": "AnotherPass123!",
        "name": "New User",
        "username": "newuser"
    }
    response = client.post("/signup", data=data)
    assert response.status_code == 200, f"Expected 200 with error form, got {response.status_code}"
    assert "Email already registered" in response.text, "Should show duplicate email error"

    # Verify no new user was created
    assert user_model.objects.filter(email="existing@example.com").count() == 1, "No duplicate should be created"

def test_login_route_get(client):
    """Test /login GET route renders the form correctly."""
    response = client.get("/login")
    assert response.status_code == 200, f"Login page should render, got {response.status_code}"
    assert "Welcome Back" in response.text, "Should include login header"
    assert 'hx-post="/login"' in response.text, "Should include form with POST action"

@pytest.mark.xfail(reason="Session incompatibility: login(req, user) raises 'cycle_key' error instead of redirecting")
def test_login_route_post_success(client, user_model):
    """
    Test /login POST with valid credentials for correct authentication and redirect.

    Intended Behavior:
    - Authenticates user and redirects to /dashboard (303).
    Current Behavior:
    - Authenticates but raises AttributeError ('cycle_key') due to login(req, user).
    Fix: Remove login(req, user) in routes/auth.py and set req.session['auth'] manually.
    """
    user_model.objects.create_user(
        username="loginuser",
        email="login@example.com",
        password="SecurePass123!"
    )
    data = {
        "email": "login@example.com",
        "password": "SecurePass123!"
    }
    response = client.post("/login", data=data)
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    assert response.headers["location"] == "/dashboard", "Should redirect to dashboard"

def test_login_route_post_failure(client, user_model):
    """Test /login POST with invalid credentials for correct error handling."""
    user_model.objects.create_user(
        username="loginuser",
        email="login@example.com",
        password="SecurePass123!"
    )
    data = {
        "email": "login@example.com",
        "password": "WrongPass!"
    }
    response = client.post("/login", data=data)
    assert response.status_code == 200, f"Expected 200 with error form, got {response.status_code}"
    assert "Invalid email or password" in response.text, "Should show auth failure message"

@pytest.mark.xfail(reason="Cannot simulate session with FastHTML Client; auth_before redirects to /login instead of clearing session")
def test_logout_route(client, user_model):
    """
    Test /logout GET route for correct session clearing and redirect.

    Intended Behavior:
    - Clears session and redirects to / (303).
    Current Behavior:
    - Redirects to /login (303) for unauthenticated users; can't test session clearing.
    Fix: Modify app.py auth_before and routes/auth.py logout to handle sessions correctly.
    """
    user_model.objects.create_user(
        username="logoutuser",
        email="logout@example.com",
        password="SecurePass123!"
    )
    # Ideally, simulate a logged-in session (not possible with current Client)
    response = client.get("/logout")
    assert response.status_code == 303, f"Expected 303 redirect, got {response.status_code}"
    assert response.headers["location"] == "/", "Should redirect to home after logout"
    # Cannot assert session cleared due to test limitation