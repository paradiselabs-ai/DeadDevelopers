"""
Test suite for AuthBridge functionality
Tests the unified authentication layer between FastHTML and Django
"""

import pytest
from django.contrib.auth import get_user_model
from auth_bridge import AuthBridge
from unittest.mock import Mock, MagicMock

User = get_user_model()


@pytest.fixture
def test_user(db):
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        ai_percentage=75
    )


@pytest.fixture
def mock_request():
    """Create a mock FastHTML request"""
    request = Mock()
    request.client = Mock()
    request.client.host = '127.0.0.1'
    request.cookies = {}
    return request


@pytest.fixture
def fasthtml_session():
    """Create a mock FastHTML session"""
    return {}


class TestAuthBridge:
    """Test cases for AuthBridge class"""
    
    def test_login_user_sets_both_sessions(self, test_user, mock_request, fasthtml_session):
        """Test that login_user sets both FastHTML and Django sessions"""
        AuthBridge.login_user(mock_request, fasthtml_session, test_user)
        
        # Check FastHTML session
        assert fasthtml_session['auth'] == 'testuser'
        assert fasthtml_session['user']['name'] == 'Test User'
        assert fasthtml_session['user']['email'] == 'test@example.com'
        assert fasthtml_session['user']['ai_percentage'] == 75
        assert fasthtml_session['user']['id'] == test_user.id
    
    def test_logout_user_clears_both_sessions(self, test_user, mock_request, fasthtml_session):
        """Test that logout_user clears both sessions"""
        # Set up logged in state
        fasthtml_session['auth'] = 'testuser'
        fasthtml_session['user'] = {
            'name': 'Test User',
            'email': 'test@example.com',
            'ai_percentage': 75
        }
        
        AuthBridge.logout_user(mock_request, fasthtml_session)
        
        # Check FastHTML session is cleared
        assert 'auth' not in fasthtml_session
        assert 'user' not in fasthtml_session
    
    def test_get_current_user_returns_user_when_authenticated(self, test_user, mock_request, fasthtml_session):
        """Test that get_current_user returns the user when authenticated"""
        fasthtml_session['auth'] = 'testuser'
        
        user = AuthBridge.get_current_user(mock_request, fasthtml_session)
        
        assert user is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
    
    def test_get_current_user_returns_none_when_not_authenticated(self, mock_request, fasthtml_session):
        """Test that get_current_user returns None when not authenticated"""
        user = AuthBridge.get_current_user(mock_request, fasthtml_session)
        assert user is None
    
    def test_get_current_user_clears_session_when_user_deleted(self, mock_request, fasthtml_session):
        """Test that get_current_user clears session when user no longer exists"""
        fasthtml_session['auth'] = 'nonexistentuser'
        
        user = AuthBridge.get_current_user(mock_request, fasthtml_session)
        
        assert user is None
        assert 'auth' not in fasthtml_session
        assert 'user' not in fasthtml_session


@pytest.mark.django_db
class TestAuthBridgeIntegration:
    """Integration tests for AuthBridge with real database"""
    
    def test_full_login_logout_cycle(self, test_user, mock_request, fasthtml_session):
        """Test a complete login and logout cycle"""
        # Login
        AuthBridge.login_user(mock_request, fasthtml_session, test_user)
        assert fasthtml_session['auth'] == 'testuser'
        
        # Verify user can be retrieved
        user = AuthBridge.get_current_user(mock_request, fasthtml_session)
        assert user.username == 'testuser'
        
        # Logout
        AuthBridge.logout_user(mock_request, fasthtml_session)
        assert 'auth' not in fasthtml_session
        
        # Verify user is no longer authenticated
        user = AuthBridge.get_current_user(mock_request, fasthtml_session)
        assert user is None
