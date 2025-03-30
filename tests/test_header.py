import pytest
from starlette.testclient import TestClient
from bs4 import BeautifulSoup

# Import both app and main to ensure routes are registered
import app
import main
from app import app as app_instance

# Create test client AFTER importing main to ensure routes are registered
client = TestClient(app_instance)

def test_header_renders():
    """Test that the header component renders without errors."""
    response = client.get("/")
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.content, 'html.parser')
    header = soup.find('header', class_='siteHeader')
    
    assert header is not None
    assert "DEADDEVELOPERS" in header.text
    
def test_navigation_links():
    """Test that navigation links are rendered correctly."""
    response = client.get("/features")
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.content, 'html.parser')
    nav_center = soup.find('div', class_='navCenter')
    
    # Test that all nav links are present
    assert nav_center.find('a', href="/features") is not None
    assert nav_center.find('a', href="/community") is not None 
    assert nav_center.find('a', href="/blog") is not None
    assert nav_center.find('a', href="/about") is not None
    
    # Test that the active link has the active class
    assert "active" in nav_center.find('a', href="/features").get('class', [])
    
    # Test other links don't have active class
    assert "active" not in nav_center.find('a', href="/community").get('class', [])

def test_mobile_menu_elements():
    """Test that mobile menu elements are present."""
    response = client.get("/")
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Test mobile menu elements
    assert soup.find(id="mobileMenu") is not None
    assert soup.find(id="mobileMenuBackdrop") is not None
    assert soup.find(id="menuToggleButton") is not None
    
    # Test hamburger and close icons
    hamburger_icon = soup.find(attrs={"d": "M4 8H20M4 16H20"})
    close_icon = soup.find(attrs={"d": "M18 6L6 18M6 6L18 18"})
    
    assert hamburger_icon is not None
    assert close_icon is not None

def test_mobile_menu_javascript():
    """Test that JavaScript for mobile menu is included."""
    response = client.get("/")
    assert response.status_code == 200
    
    html_content = response.text
    
    # Test for the toggleMobileMenu function
    assert "function toggleMobileMenu()" in html_content
    assert "getElementById('mobileMenu')" in html_content or 'getElementById("mobileMenu")' in html_content
    
    # Test for the click handler
    assert 'onclick="toggleMobileMenu()"' in html_content
    
    # Test for event listeners
    assert "window.addEventListener" in html_content

def test_different_paths():
    """Test that the header handles different paths correctly."""
    # Test with about path
    response_about = client.get("/about")
    assert response_about.status_code == 200
    
    soup_about = BeautifulSoup(response_about.content, 'html.parser')
    nav_about = soup_about.find('div', class_='navCenter')
    
    # Test that about link is active
    assert "active" in nav_about.find('a', href="/about").get('class', [])
    
    # Test with blog path
    response_blog = client.get("/blog")
    assert response_blog.status_code == 200
    
    soup_blog = BeautifulSoup(response_blog.content, 'html.parser')
    nav_blog = soup_blog.find('div', class_='navCenter')
    
    # Test that blog link is active
    assert "active" in nav_blog.find('a', href="/blog").get('class', [])

def test_svg_logo_rendering():
    """Test that the SVG logo renders correctly."""
    response = client.get("/")
    assert response.status_code == 200
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the SVG in the header
    svg = soup.find('svg')
    assert svg is not None
    
    # Test SVG attributes - note that attributes may be lowercase in HTML
    assert svg.get('viewbox') == "0 0 2000 2965" or svg.get('viewBox') == "0 0 2000 2965"
    assert svg.get('xmlns') == "http://www.w3.org/2000/svg"
    
    # Verify paths are included with correct colors
    paths = svg.find_all('path')
    fill_colors = [path.get('fill') for path in paths if path.get('fill')]
    
    assert "#FEFDFD" in fill_colors or "#FDFDFD" in fill_colors 