import os
import django
import pytest
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings
from unittest.mock import patch, MagicMock

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')
django.setup()

# Import models and utilities after Django setup
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.socialaccount.models import SocialApp, SocialAccount
from users.models import User
from users.adapters import CustomAccountAdapter, CustomSocialAccountAdapter
from allauth.account.utils import user_email
from allauth.account.adapter import get_adapter

class EmailVerificationTests(TestCase):
    """Test suite for email verification functionality"""
    
    def setUp(self):
        self.signup_url = '/signup'
        self.login_url = '/login'
        self.email_verification_sent_url = '/accounts/confirm-email/'
        self.factory = RequestFactory()
        
        # Create a test user but don't verify email
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Create EmailAddress record for the user (unverified)
        self.email_address = EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            primary=True,
            verified=False
        )
        
        # Create a site for testing
        self.site = Site.objects.get_or_create(domain='example.com', name='example.com')[0]
        settings.SITE_ID = self.site.id
    
    def test_signup_sends_verification_email(self):
        """Test that signup sends a verification email"""
        with patch('allauth.account.utils.send_email_confirmation') as mock_send:
            response = self.client.post(self.signup_url, {
                'name': 'New Test User',
                'username': 'newtestuser',
                'email': 'newtest@example.com',
                'password': 'testpass123'
            })
            
            # Check that send_email_confirmation was called
            self.assertTrue(mock_send.called)
            
            # Check that we get redirected to the verification sent page
            self.assertRedirects(response, self.email_verification_sent_url, 
                                fetch_redirect_response=False)
            
            # Check that the user was created
            self.assertTrue(User.objects.filter(email='newtest@example.com').exists())
            
            # Check that an EmailAddress record was created
            email_address = EmailAddress.objects.get(email='newtest@example.com')
            self.assertFalse(email_address.verified)
    
    def test_login_with_unverified_email(self):
        """Test that login with unverified email shows error"""
        with patch('allauth.account.utils.send_email_confirmation') as mock_send:
            response = self.client.post(self.login_url, {
                'email': 'test@example.com',
                'password': 'testpass123'
            })
            
            # Check that send_email_confirmation was called to resend verification
            self.assertTrue(mock_send.called)
            
            # Check that we stay on the login page with an error
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Email not verified', response.content)
    
    def test_login_with_verified_email(self):
        """Test that login with verified email works"""
        # Verify the email
        self.email_address.verified = True
        self.email_address.save()
        
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        
        # Check that we get redirected to the dashboard
        self.assertRedirects(response, '/dashboard', 
                            fetch_redirect_response=False)
    
    def test_email_confirmation_process(self):
        """Test the email confirmation process"""
        # Create a confirmation
        confirmation = EmailConfirmation.create(self.email_address)
        confirmation.sent = django.utils.timezone.now()
        confirmation.save()
        
        # Get the confirmation URL
        confirm_url = reverse('account_confirm_email', args=[confirmation.key])
        
        # Visit the confirmation page
        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 200)
        
        # Confirm the email
        response = self.client.post(confirm_url)
        
        # Check that the email is now verified
        self.email_address.refresh_from_db()
        self.assertTrue(self.email_address.verified)
        
        # Check that we get redirected to the login page (since we're not logged in)
        self.assertRedirects(response, settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL, 
                            fetch_redirect_response=False)


class GitHubOAuthTests(TestCase):
    """Test suite for GitHub OAuth functionality"""
    
    def setUp(self):
        self.factory = RequestFactory()
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Create a site for testing
        self.site = Site.objects.get_or_create(domain='example.com', name='example.com')[0]
        settings.SITE_ID = self.site.id
        
        # Create a GitHub SocialApp
        self.github_app = SocialApp.objects.create(
            provider='github',
            name='GitHub',
            client_id='github-client-id',
            secret='github-secret',
            key='',
            sites=[self.site]
        )
    
    def test_github_login_button_exists(self):
        """Test that GitHub login button exists on login page"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Continue with GitHub', response.content)
        self.assertIn(b'/accounts/github/login/', response.content)
    
    def test_github_signup_button_exists(self):
        """Test that GitHub signup button exists on signup page"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign up with GitHub', response.content)
        self.assertIn(b'/accounts/github/login/', response.content)
    
    @patch('allauth.socialaccount.providers.github.views.GitHubOAuth2Adapter.complete_login')
    def test_github_login_flow(self, mock_complete_login):
        """Test the GitHub login flow"""
        # Mock the GitHub login response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': '12345',
            'login': 'githubuser',
            'name': 'GitHub User',
            'email': 'github@example.com'
        }
        mock_complete_login.return_value = mock_response
        
        # Start the GitHub login flow
        response = self.client.get('/accounts/github/login/')
        self.assertEqual(response.status_code, 302)  # Redirects to GitHub
        
        # Mock the callback from GitHub
        response = self.client.get('/accounts/github/login/callback/?code=test-code&state=test-state')
        
        # Should redirect to signup page to complete profile
        self.assertRedirects(response, '/accounts/social/signup/', 
                            fetch_redirect_response=False)
        
        # Complete the signup
        response = self.client.post('/accounts/social/signup/', {
            'email': 'github@example.com',
            'username': 'githubuser',
            'name': 'GitHub User'
        })
        
        # Check that the user was created
        self.assertTrue(User.objects.filter(email='github@example.com').exists())
        
        # Check that a SocialAccount was created
        social_account = SocialAccount.objects.get(user__email='github@example.com')
        self.assertEqual(social_account.provider, 'github')
    
    def test_custom_social_account_adapter(self):
        """Test the CustomSocialAccountAdapter"""
        adapter = CustomSocialAccountAdapter()
        
        # Create a mock sociallogin
        sociallogin = MagicMock()
        sociallogin.account.provider = 'github'
        sociallogin.account.extra_data = {
            'login': 'githubuser',
            'name': 'GitHub User',
            'email': 'github@example.com'
        }
        
        # Create a mock user
        user = MagicMock()
        user.username = None
        user.first_name = None
        user.last_name = None
        
        # Test populate_user
        populated_user = adapter.populate_user(None, sociallogin, {})
        
        # Check that the user was populated with GitHub data
        self.assertEqual(populated_user.username, 'githubuser')
        self.assertEqual(populated_user.github_username, 'githubuser')
        self.assertEqual(populated_user.ai_percentage, 0)


class AuthIntegrationTests(TestCase):
    """Integration tests for the authentication system"""
    
    def setUp(self):
        self.client = Client()
        
        # Create a verified user
        self.verified_user = User.objects.create_user(
            username='verifieduser',
            email='verified@example.com',
            password='testpass123',
            first_name='Verified',
            last_name='User'
        )
        
        # Create EmailAddress record for the verified user
        self.verified_email = EmailAddress.objects.create(
            user=self.verified_user,
            email=self.verified_user.email,
            primary=True,
            verified=True
        )
        
        # Create an unverified user
        self.unverified_user = User.objects.create_user(
            username='unverifieduser',
            email='unverified@example.com',
            password='testpass123',
            first_name='Unverified',
            last_name='User'
        )
        
        # Create EmailAddress record for the unverified user
        self.unverified_email = EmailAddress.objects.create(
            user=self.unverified_user,
            email=self.unverified_user.email,
            primary=True,
            verified=False
        )
    
    def test_full_login_flow_verified_user(self):
        """Test the full login flow for a verified user"""
        # Login
        response = self.client.post('/login', {
            'email': 'verified@example.com',
            'password': 'testpass123'
        })
        
        # Should redirect to dashboard
        self.assertRedirects(response, '/dashboard', 
                            fetch_redirect_response=False)
        
        # Check session data
        session = self.client.session
        self.assertEqual(session['auth'], 'verifieduser')
        self.assertEqual(session['user']['name'], 'Verified User')
        self.assertEqual(session['user']['email'], 'verified@example.com')
        
        # Logout
        response = self.client.get('/logout')
        
        # Should redirect to home
        self.assertRedirects(response, '/', 
                            fetch_redirect_response=False)
        
        # Check session data is cleared
        session = self.client.session
        self.assertNotIn('auth', session)
        self.assertNotIn('user', session)
    
    def test_full_login_flow_unverified_user(self):
        """Test the full login flow for an unverified user"""
        with patch('allauth.account.utils.send_email_confirmation') as mock_send:
            # Login
            response = self.client.post('/login', {
                'email': 'unverified@example.com',
                'password': 'testpass123'
            })
            
            # Should stay on login page with error
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Email not verified', response.content)
            
            # Check that send_email_confirmation was called
            self.assertTrue(mock_send.called)
    
    def test_full_signup_flow(self):
        """Test the full signup flow"""
        with patch('allauth.account.utils.send_email_confirmation') as mock_send:
            # Signup
            response = self.client.post('/signup', {
                'name': 'New Test User',
                'username': 'newtestuser',
                'email': 'newtest@example.com',
                'password': 'testpass123'
            })
            
            # Should redirect to verification sent page
            self.assertRedirects(response, '/accounts/confirm-email/', 
                                fetch_redirect_response=False)
            
            # Check that send_email_confirmation was called
            self.assertTrue(mock_send.called)
            
            # Check that the user was created
            user = User.objects.get(email='newtest@example.com')
            self.assertEqual(user.username, 'newtestuser')
            
            # Check that an EmailAddress record was created
            email_address = EmailAddress.objects.get(email='newtest@example.com')
            self.assertFalse(email_address.verified)
            
            # Create a confirmation
            confirmation = EmailConfirmation.create(email_address)
            confirmation.sent = django.utils.timezone.now()
            confirmation.save()
            
            # Get the confirmation URL
            confirm_url = reverse('account_confirm_email', args=[confirmation.key])
            
            # Confirm the email
            response = self.client.post(confirm_url)
            
            # Check that the email is now verified
            email_address.refresh_from_db()
            self.assertTrue(email_address.verified)
            
            # Now try to login
            response = self.client.post('/login', {
                'email': 'newtest@example.com',
                'password': 'testpass123'
            })
            
            # Should redirect to dashboard
            self.assertRedirects(response, '/dashboard', 
                                fetch_redirect_response=False)