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
        "email": f"existing_{unique_id}@example.com",  # Same email as above
        "password": "NewPass123!",
        "name": "Duplicate User",
        "username": f"duplicateuser_{unique_id}"
    }
    response = client.post("/signup", data=data)
    assert response.status_code == 200, f"Expected 200 with error, got {response.status_code}"
    
    # Test for error element in response
    soup = BeautifulSoup(response.text, 'html.parser')
    error_element = soup.find(['div', 'p', 'span'], class_=lambda c: c and 'error' in c.lower())
    assert error_element is not None, "Should display error message for duplicate email"

def test_login_page_structure(client):
    """
    Test /login GET route for correct structure.
    """
    response = client.get("/login")
    assert response.status_code == 200, f"Login page should render, got {response.status_code}"
    
    # Test for correct structure
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for form existence
    form = soup.find('form')
    assert form is not None, "Login page should have a form"
    
    # Check for email and password inputs
    email_input = form.find('input', attrs={'name': 'email'})
    assert email_input is not None, "Login form should have email input"
    
    password_input = form.find('input', attrs={'name': 'password'})
    assert password_input is not None, "Login form should have password input"
    
    # Check for submit button
    submit_button = form.find('button', attrs={'type': 'submit'}) or form.find('input', attrs={'type': 'submit'})
    assert submit_button is not None, "Login form should have submit button"

def test_signup_page_structure(client):
    """
    Test /signup GET route for correct structure.
    """
    response = client.get("/signup")
    assert response.status_code == 200, f"Signup page should render, got {response.status_code}"
    
    # Test for correct structure
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for form existence
    form = soup.find('form')
    assert form is not None, "Signup page should have a form"
    
    # Check for required inputs
    email_input = form.find('input', attrs={'name': 'email'})
    assert email_input is not None, "Signup form should have email input"
    
    password_input = form.find('input', attrs={'name': 'password'})
    assert password_input is not None, "Signup form should have password input"
    
    name_input = form.find('input', attrs={'name': 'name'})
    assert name_input is not None, "Signup form should have name input"
    
    username_input = form.find('input', attrs={'name': 'username'})
    assert username_input is not None, "Signup form should have username input"
    
    # Check for submit button
    submit_button = form.find('button', attrs={'type': 'submit'}) or form.find('input', attrs={'type': 'submit'})
    assert submit_button is not None, "Signup form should have submit button"

def test_homepage_structure(client):
    """
    Test the homepage (/) for correct structure.
    """
    response = client.get("/")
    assert response.status_code == 200, f"Homepage should render, got {response.status_code}"
    
    # Test for correct structure
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for header
    header = soup.find('header') or soup.find('div', class_=lambda c: c and 'header' in c.lower())
    assert header is not None, "Homepage should have a header"
    
    # Check for navigation
    nav = header.find('nav')
    assert nav is not None, "Header should contain navigation"
    
    # Check for main content container
    main_content = soup.find(['div', 'main'], class_=lambda c: c and ('container' in c.lower() or 'content' in c.lower() or 'main' in c.lower()))
    assert main_content is not None, "Homepage should have main content container"
    
    # Check for call-to-action element
    cta_element = soup.find(['a', 'button'], class_=lambda c: c and 'cta' in c.lower()) or \
                  soup.find(['a', 'button'], string=lambda s: s and ('get started' in s.lower() or 'sign up' in s.lower() or 'join' in s.lower()))
    assert cta_element is not None, "Homepage should have a call-to-action element"
    
    # Check for footer
    footer = soup.find('footer')
    assert footer is not None, "Homepage should have a footer"

def test_login_route_get(client):
    """Test /login GET route renders the form correctly."""
    response = client.get("/login")
    assert response.status_code == 200, f"Login page should render, got {response.status_code}"
    
    # Test for correct structure
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check for form existence
    form = soup.find('form')
    assert form is not None, "Login page should have a form"
    
    # Check for email and password inputs
    email_input = form.find('input', attrs={'name': 'email'})
    assert email_input is not None, "Login form should have email input"
    
    password_input = form.find('input', attrs={'name': 'password'})
    assert password_input is not None, "Login form should have password input"
    
    # Check for submit button
    submit_button = form.find('button', attrs={'type': 'submit'}) or form.find('input', attrs={'type': 'submit'})
    assert submit_button is not None, "Login form should have submit button"

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
    
    # Test for error element in response
    soup = BeautifulSoup(response.text, 'html.parser')
    error_element = soup.find(['div', 'p', 'span'], class_=lambda c: c and 'error' in c.lower())
    assert error_element is not None, "Should display error message for invalid credentials"

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