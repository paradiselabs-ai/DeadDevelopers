import pytest
from fasthtml.common import *
from starlette.testclient import TestClient
from app import app
import sys

# Make sure the routes are properly imported before testing
import main

client = TestClient(app)

def test_blog_route_exists():
    """Test that the blog route exists and returns a 200 OK status."""
    response = client.get("/blog")
    assert response.status_code == 200

def test_blog_route_accessible_without_auth():
    """Test that the blog route is accessible without authentication."""
    # This test checks that the route doesn't redirect to login
    response = client.get("/blog", follow_redirects=False)
    assert response.status_code == 200

def test_blog_page_structure():
    """Test that the blog page has the core structural elements."""
    response = client.get("/blog")
    content = response.text
    
    # Check that the page contains a div element (very basic test)
    assert "<div" in content
    
    # Check for basic structural indicators
    assert "<article" in content  # Should have at least one article
    assert "<button" in content   # Should have at least one button

@pytest.mark.xfail(reason="Write post page not implemented yet")
def test_write_post_route():
    """Test that the write post route exists and requires authentication."""
    # This test is expected to fail until the write-post route is implemented
    response = client.get("/write-post", follow_redirects=False)
    # Should redirect to login without being authenticated
    assert response.status_code in [302, 303]  # Accept either redirect code
