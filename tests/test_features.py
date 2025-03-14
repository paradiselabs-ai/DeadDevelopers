import pytest
from fasthtml.common import *
from starlette.testclient import TestClient

# Import both app and main to ensure routes are registered
import app
import main
from app import app as app_instance

# Create test client AFTER importing main to ensure routes are registered
client = TestClient(app_instance)

def test_features_route_exists():
    """Test that the features route exists and returns a 200 OK status."""
    response = client.get("/features")
    assert response.status_code == 200

def test_features_page_content():
    """Test that the features page contains expected content."""
    response = client.get("/features")
    content = response.text
    
    # Print content for debugging
    print("Response content:", content[:500])  # Print first 500 chars for debugging
    
    # Check page title - should be in a <title> tag
    assert "<title>Platform Features</title>" in content
    
    # Check that main feature categories are present
    # Using more lenient checks that will work with different HTML structures
    assert "Real-Time Chat" in content
    assert "Code Challenges" in content
    
    # Check for at least one "Learn More" link
    assert "Learn More" in content
    
    # Check for call to action section - look for general terms
    assert "Get Started" in content
