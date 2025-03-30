import pytest
from starlette.testclient import TestClient
from bs4 import BeautifulSoup
from app import app

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
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Test header is present
    header = soup.find('header', class_='site-header')
    assert header is not None
    
    # Test navigation elements
    nav = header.find('nav', class_='main-nav')
    assert nav is not None
    
    # Test that the blog container exists
    blog_container = soup.find('div', class_='blog-container')
    assert blog_container is not None
    
    # Test that there's a posts grid
    posts_grid = soup.find('div', class_='posts-grid')
    assert posts_grid is not None
    
    # Test that there are blog post cards
    post_cards = posts_grid.find_all('article', class_='post-card')
    assert len(post_cards) > 0

def test_blog_post_card_structure():
    """Test that the blog post cards have the expected structure."""
    response = client.get("/blog")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the first post card
    posts_grid = soup.find('div', class_='posts-grid')
    post_cards = posts_grid.find_all('article', class_='post-card')
    
    # Ensure we have at least one post card
    assert len(post_cards) > 0
    
    # Test the structure of the first post card
    first_card = post_cards[0]
    
    # Card should have a post header
    post_header = first_card.find('div', class_='post-header')
    assert post_header is not None
    
    # Card should have a post title
    post_title = first_card.find('h2', class_='post-title')
    assert post_title is not None
    
    # Card should have a post description
    post_description = first_card.find('p', class_='post-description')
    assert post_description is not None
    
    # Card should have tags
    tags = first_card.find('div', class_='tags')
    assert tags is not None

def test_write_post_button_exists():
    """Test that the Write Post button exists."""
    response = client.get("/blog")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the header section
    header_section = soup.find('div', class_='header')
    assert header_section is not None
    
    # Find the Write Post button
    write_post_btn = soup.find('button', class_='write-post-btn')
    assert write_post_btn is not None
    
    # Verify it has an onclick attribute (without checking the specific URL)
    assert 'onclick' in write_post_btn.attrs

@pytest.mark.xfail(reason="Write post page not implemented yet")
def test_write_post_route():
    """Test that the write post route exists and requires authentication."""
    # This test is expected to fail until the write-post route is implemented
    response = client.get("/write-post", follow_redirects=False)
    # Should redirect to login without being authenticated
    assert response.status_code in [302, 303]  # Accept either redirect code
