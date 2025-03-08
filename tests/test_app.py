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

@pytest.fixture(scope="function")
def client():
    """Fixture to set up Django database and provide a test client."""
    from django.conf import settings
    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            TIME_ZONE='UTC',
            USE_TZ=True,
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'users',  # Adjust if your User model is elsewhere
            ],
            SECRET_KEY='test-secret-key',
            AUTH_USER_MODEL='users.User' if 'users' in os.listdir() else 'auth.User',
        )

    django.setup()
    from django.core.management import call_command
    call_command('migrate', '--noinput')
    return Client(app)

def test_landing_page(client):
    """Verify the landing page renders with the correct title and hero content."""
    response = client.get("/")
    assert response.status_code == 200
    assert "DeadDevelopers" in response.text
    assert "Humans (mostly) Not Required" in response.text

def test_signup_form_submission(client):
    """Test that submitting the signup form redirects to the dashboard."""
    data = {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "name": "Test User",
        "username": "testuser"
    }
    response = client.post("/signup", data=data)
    assert response.status_code == 303
    assert response.headers["Location"] == "/dashboard"

def test_nav_menu_toggle(client):
    """Ensure the navigation menu toggle button works with HTMX."""
    response = client.get("/")
    assert response.status_code == 200
    assert "hx-get" in response.text
    toggle_response = client.get("/nav-toggle")
    assert toggle_response.status_code == 200
    assert "main-nav active" in toggle_response.text