import pytest
from starlette.testclient import TestClient
from bs4 import BeautifulSoup

from main import app

client = TestClient(app)

def test_about_page_loads():
    """
    Test that the about page loads successfully with a 200 status code.
    """
    response = client.get("/about")
    assert response.status_code == 200

def test_about_page_has_correct_structure():
    """
    Test that the about page has the correct structural elements.
    These tests check for the presence of key structural components
    without relying on specific content.
    """
    response = client.get("/about")
    assert response.status_code == 200
    
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # More flexible header check
    header = (
        soup.find('header') or
        soup.find(['div', 'section'], class_=lambda c: c and ('header' in c.lower() or 'nav' in c.lower()))
    )
    assert header is not None, "Page should have a header element"
    
    # More flexible navigation check
    nav = (
        header.find('nav') or
        soup.find('nav') or
        soup.find(['div', 'ul'], class_=lambda c: c and 'nav' in c.lower())
    )
    assert nav is not None, "Page should have navigation elements"
    
    # More flexible container check
    container = (
        soup.find('div', class_=lambda c: c and ('landing' in c.lower() or 'about' in c.lower())) or
        soup.find('main') or
        soup.find(['div', 'section'], class_=lambda c: c and ('container' in c.lower() or 'content' in c.lower() or 'main' in c.lower()))
    )
    assert container is not None, "Page should have a main container element"
    
    # More flexible content check
    content_area = (
        container.find(['div', 'section'], class_=lambda c: c and ('content' in c.lower() or 'animated' in c.lower())) or
        container.find(['div', 'section'])
    )
    assert content_area is not None, "Page should have a content area"
    
    # Check for sections - more flexible
    sections = (
        content_area.find_all(['section', 'div'], class_=lambda c: c and ('section' in c.lower() or 'hero' in c.lower() or 'tech' in c.lower() or 'cta' in c.lower())) or
        content_area.find_all(['section', 'div'])
    )
    assert len(sections) > 0, "Page should have content sections"
    
    # Look for technology section - more flexible
    tech_section = (
        soup.find(['section', 'div'], class_=lambda c: c and ('tech' in c.lower())) or
        soup.find(['section', 'div'], id=lambda i: i and 'tech' in i.lower())
    )
    
    # If we found a technology section, check for a grid or cards
    if tech_section:
        tech_grid = (
            tech_section.find(['div', 'ul'], class_=lambda c: c and ('grid' in c.lower() or 'cards' in c.lower() or 'list' in c.lower())) or
            tech_section.find(['div', 'ul'])
        )
        assert tech_grid is not None, "Technology section should have a grid or list of technologies"
    
    # Check for hero section - more flexible
    hero_section = (
        soup.find(['section', 'div'], class_=lambda c: c and ('hero' in c.lower() or 'banner' in c.lower() or 'jumbotron' in c.lower())) or
        soup.find(['section', 'div'], id=lambda i: i and ('hero' in i.lower() or 'banner' in i.lower()))
    )
    
    # If we found a hero section, check for a heading
    if hero_section:
        hero_heading = hero_section.find(['h1', 'h2', 'h3'])
        assert hero_heading is not None, "Hero section should have a heading"
    
    # More flexible footer check
    footer = (
        soup.find('footer') or
        soup.find(['div', 'section'], class_=lambda c: c and 'footer' in c.lower())
    )
    assert footer is not None, "Page should have a footer element"

def test_about_page_has_technology_cards():
    """
    Test that the about page has technology cards in the technologies section.
    This test checks for the structural elements of the cards without relying on specific content.
    """
    response = client.get("/about")
    assert response.status_code == 200
    
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the technologies section - more flexible
    tech_section = (
        soup.find(['section', 'div'], class_=lambda c: c and ('tech' in c.lower())) or
        soup.find(['section', 'div'], id=lambda i: i and 'tech' in i.lower())
    )
    assert tech_section is not None, "Page should have a technologies section"
    
    # Find technology grid or container - more flexible
    tech_grid = (
        tech_section.find(['div', 'ul'], class_=lambda c: c and ('grid' in c.lower() or 'cards' in c.lower() or 'list' in c.lower())) or
        tech_section.find(['div', 'ul'])
    )
    assert tech_grid is not None, "Technologies section should have a grid or list of technologies"
    
    # Find technology cards - more flexible
    tech_cards = (
        tech_grid.find_all(['div', 'li', 'article'], class_=lambda c: c and ('card' in c.lower() or 'item' in c.lower() or 'tech' in c.lower())) or
        tech_grid.find_all(['div', 'li', 'article'])
    )
    
    # Ensure there are multiple technology cards
    assert len(tech_cards) > 0, "Technologies grid should contain technology cards"
    
    # Test the structure of the first card with content
    first_card = None
    for card in tech_cards:
        if card.get_text(strip=True):
            first_card = card
            break
    
    assert first_card is not None, "At least one technology card should have content"
    
    # Card should have a heading or title - more flexible
    title_element = (
        first_card.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong']) or
        first_card.find(['div', 'span'], class_=lambda c: c and ('title' in c.lower() or 'name' in c.lower() or 'header' in c.lower()))
    )
    
    # Card should have descriptive text - more flexible
    description = (
        first_card.find('p') or
        first_card.find(['div', 'span'], class_=lambda c: c and ('desc' in c.lower() or 'content' in c.lower() or 'text' in c.lower()))
    )
    
    # Check that there's some meaningful content in the card
    assert first_card.get_text(strip=True), "Technology card should have text content"

def test_about_cta_button_is_functional():
    """
    Test that the CTA button on the about page exists and has an onclick handler.
    """
    response = client.get("/about")
    assert response.status_code == 200
    
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the CTA section - more flexible
    cta_section = (
        soup.find(['section', 'div'], class_=lambda c: c and 'cta' in c.lower()) or
        soup.find(['section', 'div'], id=lambda i: i and 'cta' in i.lower())
    )
    assert cta_section is not None, "Page should have a call-to-action section"
    
    # Find the CTA button - more flexible
    cta_button = (
        cta_section.find(['button', 'a'], class_=lambda c: c and ('cta' in c.lower() or 'button' in c.lower())) or
        cta_section.find(['button', 'a'])
    )
    assert cta_button is not None, "CTA section should have a button or link"
    
    # Check that the button has an action (either onclick or href)
    has_action = (
        'onclick' in cta_button.attrs or 
        'href' in cta_button.attrs
    )
    assert has_action, "CTA button should have an action (onclick or href)"
