import pytest
from starlette.testclient import TestClient
from bs4 import BeautifulSoup

# Import both app and main to ensure routes are registered
import app
import main
from app import app as app_instance

# Create test client
client = TestClient(app_instance)

def test_mobile_menu_exists():
    """Test that the mobile menu elements exist in the HTML."""
    response = client.get("/")
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Check mobile menu exists
    mobile_menu = soup.find(id="mobileMenu")
    assert mobile_menu is not None
    
    # Check backdrop exists
    backdrop = soup.find(id="mobileMenuBackdrop")
    assert backdrop is not None
    
    # Check menu toggle button exists
    menu_button = soup.find(id="menuToggleButton")
    assert menu_button is not None
    
    # Check it has the onclick handler
    assert menu_button.get('onclick') == "toggleMobileMenu()"

def test_mobile_menu_js_functions():
    """Test that the JavaScript functions for the mobile menu are included."""
    response = client.get("/")
    assert response.status_code == 200
    
    html_content = response.text
    
    # Check toggleMobileMenu function exists
    assert "function toggleMobileMenu()" in html_content
    
    # Check closeMobileMenu function exists
    assert "function closeMobileMenu()" in html_content
    
    # Check event listener setup
    assert "window.addEventListener" in html_content
    
    # Check the mobile menu classes are toggled
    assert "mobileMenu.classList.add('open')" in html_content
    assert "mobileMenu.classList.remove('open')" in html_content

def test_mobile_menu_contains_links():
    """Test that the mobile menu contains the navigation links."""
    response = client.get("/")
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.content, 'html.parser')
    mobile_menu = soup.find(id="mobileMenu")
    
    # Check for navigation links in mobile menu
    features_link = mobile_menu.find('a', href="/features")
    assert features_link is not None
    
    community_link = mobile_menu.find('a', href="/community")
    assert community_link is not None
    
    blog_link = mobile_menu.find('a', href="/blog")
    assert blog_link is not None
    
    about_link = mobile_menu.find('a', href="/about")
    assert about_link is not None

def test_mobile_menu_auth_links():
    """Test that the mobile menu contains authentication links."""
    response = client.get("/")
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.content, 'html.parser')
    mobile_menu = soup.find(id="mobileMenu")
    
    # Check for login and signup links
    login_link = mobile_menu.find('a', href="/login")
    assert login_link is not None
    assert "Log in" in login_link.text
    
    signup_link = mobile_menu.find('a', href="/signup")
    assert signup_link is not None
    assert "Sign up" in signup_link.text

@pytest.mark.skip(reason="Requires browser automation to test dynamic behavior")
def test_mobile_menu_toggle_behavior():
    """Test toggling the mobile menu open and closed (requires browser automation)."""
    # This test is skipped as it requires browser automation
    pass

@pytest.mark.skip(reason="Requires browser automation to test dynamic behavior")
def test_backdrop_closes_mobile_menu():
    """Test that clicking the backdrop closes the mobile menu (requires browser automation)."""
    # This test is skipped as it requires browser automation
    pass 