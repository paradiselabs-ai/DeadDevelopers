import pytest
from fasthtml.common import *
from starlette.testclient import TestClient
from app import app
import sys

# Make sure the routes are properly imported before testing
import main

client = TestClient(app)

def test_community_route_exists():
    """Test that the community route exists and returns a 200 OK status."""
    response = client.get("/community")
    assert response.status_code == 200

def test_community_route_accessible_without_auth():
    """Test that the community route is accessible without authentication."""
    # This test checks that the route doesn't redirect to login
    response = client.get("/community", follow_redirects=False)
    assert response.status_code == 200
    # If it redirected, it would be 302 or 303 to /login or /signup

def test_community_page_title():
    """Test that the community page has the correct title."""
    response = client.get("/community")
    content = response.text
    
    # Check page title
    assert "Join the DeadDevelopers Community" in content

def test_community_hero_section():
    """Test that the hero section contains expected content."""
    response = client.get("/community")
    content = response.text
    
    # Check hero section text
    assert "Join the DeadDevelopers Community" in content
    assert "Connect, collaborate, and code with" in content
    assert "fellow developers" in content
    assert "thriving" in content
    assert "community" in content

def test_community_feature_cards():
    """Test that the feature cards section contains expected content."""
    response = client.get("/community")
    content = response.text
    
    # Check Forum card
    assert "Forum" in content
    assert "Engage in discussions" in content
    assert "Join Discussion" in content
    
    # Check Live Chat card
    assert "Live Chat" in content
    assert "Have live conversations" in content
    assert "Start Chatting" in content

def test_community_member_spotlight():
    """Test that the member spotlight section contains expected content."""
    response = client.get("/community")
    content = response.text
    
    # Check member spotlight section
    assert "Member Spotlight" in content
    
    # Check for member information
    assert "Contributions" in content

def test_community_cta_section():
    """Test that the call to action section contains expected content."""
    response = client.get("/community")
    content = response.text
    
    # Check for call to action content
    assert "Ready to Join?" in content
    assert "Join Now" in content

def test_community_page_footer():
    """Test that the footer contains expected content."""
    response = client.get("/community")
    content = response.text
    
    # Check footer content
    assert "Product" in content
    assert "Company" in content
    assert "Resources" in content
    assert "ParadiseLabs" in content
    assert "Twitter" in content
    assert "GitHub" in content
    assert "Discord" in content

def test_community_page_navigation():
    """Test that the navigation menu contains expected links."""
    response = client.get("/community")
    content = response.text
    
    # Check navigation links
    assert "/Features" in content
    assert "/Community" in content
    assert "/Blog" in content
    assert "/About" in content
    assert "Log in" in content
    assert "Sign up" in content

def test_community_page_css_classes():
    """Test that the page contains expected CSS class names."""
    response = client.get("/community")
    content = response.text
    
    # Check CSS classes
    assert "cards-container" in content
    assert "member-card" in content
    assert "hero" in content

# HTMX integration test
def test_community_page_htmx_attributes():
    """Test that the page contains HTMX attributes for dynamic behavior."""
    response = client.get("/community")
    content = response.text
    
    # Check for HTMX attributes
    assert "hx-get" in content
