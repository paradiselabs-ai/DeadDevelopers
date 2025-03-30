import pytest
from starlette.testclient import TestClient

# Import the application directly from main.py
from main import app

# Create a test client using the main app
client = TestClient(app)

def test_logout_endpoint_exists():
    """
    Test that the logout endpoint exists and returns a successful response.
    """
    # First verify we can access the logout endpoint
    response = client.get("/logout")
    assert response.status_code == 200, f"Expected 200 OK status, got {response.status_code}"
    
    # The response should contain HTML content
    assert "text/html" in response.headers["content-type"], "Response should be HTML content"

if __name__ == "__main__":
    pytest.main([__file__])
