import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..users.models import User
from ..users.forms import CustomUserCreationForm, CustomUserChangeForm


class UserModelTests(TestCase):
    """Test suite for the custom User model"""

    def setUp(self):
        self.User = get_user_model()
        
    def test_create_user(self):
        """Test creating a regular user"""
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.ai_percentage, 0)
        
    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = self.User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        
    def test_email_required(self):
        """Test that email is required"""
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                username='testuser',
                email='',
                password='testpass123'
            )
            
    def test_get_display_name(self):
        """Test the get_display_name method"""
        # User with first and last name
        user1 = self.User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user1.get_display_name(), 'Test User')
        
        # User without first and last name
        user2 = self.User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        self.assertEqual(user2.get_display_name(), 'testuser2')
        
    def test_ai_percentage_default(self):
        """Test that ai_percentage defaults to 0"""
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.ai_percentage, 0)
        
    def test_update_ai_percentage(self):
        """Test updating a user's AI percentage"""
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        user.ai_percentage = 85
        user.save()
        updated_user = self.User.objects.get(email='test@example.com')
        self.assertEqual(updated_user.ai_percentage, 85)


class AuthViewsTests(TestCase):
    """Test suite for authentication views"""
    
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.dashboard_url = reverse('dashboard')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_signup_view_get(self):
        """Test GET request to signup view"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)
        
    def test_signup_view_post_valid(self):
        """Test valid POST request to signup view"""
        response = self.client.post(self.signup_url, {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'name': 'New User',
            'password1': 'newpass123!',
            'password2': 'newpass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dashboard_url)
        
        # Check that user was created
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        
    def test_signup_view_post_invalid(self):
        """Test invalid POST request to signup view"""
        response = self.client.post(self.signup_url, {
            'email': 'invalid',
            'username': '',
            'name': 'New User',
            'password1': 'newpass123',
            'password2': 'different'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')
        self.assertFalse(User.objects.filter(email='invalid').exists())
        
    def test_login_view_get(self):
        """Test GET request to login view"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        
    def test_login_view_post_valid(self):
        """Test valid POST request to login view"""
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dashboard_url)
        
    def test_login_view_post_invalid(self):
        """Test invalid POST request to login view"""
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        
    def test_logout_view(self):
        """Test logout view"""
        # Login first
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class ProfileViewTests(TestCase):
    """Test suite for profile view"""
    
    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('profile')
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_profile_view_get_unauthenticated(self):
        """Test GET request to profile view when not logged in"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        
    def test_profile_view_get_authenticated(self):
        """Test GET request to profile view when logged in"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsInstance(response.context['form'], CustomUserChangeForm)
        
    def test_profile_view_post_valid(self):
        """Test valid POST request to profile view"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post(self.profile_url, {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'This is my bio'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)
        
        # Check that user was updated
        updated_user = User.objects.get(email='test@example.com')
        self.assertEqual(updated_user.bio, 'This is my bio')
        self.assertEqual(updated_user.first_name, 'Test')
        
    def test_update_ai_percentage_view(self):
        """Test the update_ai_percentage view"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post(reverse('update_ai_percentage'), {
            'ai_percentage': 75
        })
        self.assertEqual(response.status_code, 200)
        
        # Check that user was updated
        updated_user = User.objects.get(email='test@example.com')
        self.assertEqual(updated_user.ai_percentage, 75)
        
    def test_update_ai_percentage_invalid(self):
        """Test the update_ai_percentage view with invalid data"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post(reverse('update_ai_percentage'), {
            'ai_percentage': 'invalid'
        })
        self.assertEqual(response.status_code, 400)
        
        # User should not be updated
        updated_user = User.objects.get(email='test@example.com')
        self.assertEqual(updated_user.ai_percentage, 0)
        
    def test_update_ai_percentage_out_of_range(self):
        """Test the update_ai_percentage view with out of range data"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post(reverse('update_ai_percentage'), {
            'ai_percentage': 101
        })
        self.assertEqual(response.status_code, 400)
        
        # User should not be updated
        updated_user = User.objects.get(email='test@example.com')
        self.assertEqual(updated_user.ai_percentage, 0)
