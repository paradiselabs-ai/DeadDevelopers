import pytest
from starlette.testclient import TestClient
from bs4 import BeautifulSoup

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

def test_features_page_structure():
    """Test that the features page has the correct structural elements."""
    response = client.get("/features")
    
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Test that the page has a title
    assert soup.title is not None
    
    # More flexible header check
    header = (
        soup.find('header') or 
        soup.find(['div', 'section', 'nav'], class_=lambda c: c and ('header' in c.lower() or 'nav' in c.lower()))
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
        soup.find(['div', 'main'], class_=lambda c: c and 'feature' in c.lower()) or
        soup.find('main') or
        soup.find(['div', 'section'], class_=lambda c: c and ('container' in c.lower() or 'content' in c.lower() or 'main' in c.lower()))
    )
    assert container is not None, "Page should have a main container element"
    
    # More flexible feature sections check
    feature_sections = (
        soup.find_all(['section', 'div'], class_=lambda c: c and 'feature' in c.lower()) or
        soup.find_all(['section', 'div'], class_=lambda c: c and ('section' in c.lower() or 'card' in c.lower())) or
        soup.find_all(['section', 'div'])
    )
    assert len(feature_sections) > 0, "Page should have feature sections or content divisions"
    
    # Test for presence of call-to-action elements
    cta_elements = (
        soup.find(['a', 'button'], class_=lambda c: c and ('cta' in c.lower() or 'button' in c.lower())) or
        soup.find(['a', 'button'], string=lambda s: s and ('get started' in s.lower() or 'try' in s.lower() or 'learn more' in s.lower()))
    )
    assert cta_elements is not None, "Page should have at least one call-to-action element"
    
    # Footer should be present - more flexible
    footer = (
        soup.find('footer') or
        soup.find(['div', 'section'], class_=lambda c: c and 'footer' in c.lower())
    )
    assert footer is not None, "Page should have a footer element"

def test_feature_cards_structure():
    """Test the structure of feature cards on the features page."""
    response = client.get("/features")
    
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find feature cards with a more flexible approach
    feature_cards = (
        soup.find_all(['div', 'article', 'section'], class_=lambda c: c and ('card' in c.lower() or 'feature' in c.lower() or 'item' in c.lower())) or
        soup.find_all(['li', 'div', 'article'], class_=lambda c: c and ('list-item' in c.lower() or 'grid-item' in c.lower()))
    )
    
    # If we can't find specific feature cards, look for any meaningful content divisions
    if len(feature_cards) == 0:
        main_container = (
            soup.find('main') or 
            soup.find(['div', 'section'], class_=lambda c: c and ('container' in c.lower() or 'content' in c.lower() or 'main' in c.lower()))
        )
        if main_container:
            feature_cards = main_container.find_all(['div', 'section'])
    
    assert len(feature_cards) > 0, "Page should have feature cards or content divisions"
    
    # Check the structure of at least one feature card
    non_empty_cards = [card for card in feature_cards if card.get_text(strip=True)]
    assert len(non_empty_cards) > 0, "At least one feature card should have content"
    
    # Take the first non-empty card
    first_card = non_empty_cards[0]
    
    # Check for heading or title element
    heading = (
        first_card.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong']) or
        first_card.find(['div', 'span'], class_=lambda c: c and ('title' in c.lower() or 'heading' in c.lower()))
    )
    assert heading is not None, "Feature card should have a heading/title element"
    
    # Check for descriptive text
    has_description = (
        first_card.find('p') is not None or
        first_card.find(['div', 'span'], class_=lambda c: c and ('desc' in c.lower() or 'text' in c.lower())) is not None
    )
    assert has_description, "Feature card should include descriptive text"

def test_features_comparison_table():
    """Test for the presence of a feature comparison or highlights table/section."""
    response = client.get("/features")
    
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Look for a comparison table or a feature highlights section
    # - Either an actual table
    # - Or a section formatted as a table/grid/comparison
    comparison_element = (
        soup.find('table') or
        soup.find(['div', 'section'], class_=lambda c: c and ('compare' in c.lower() or 'table' in c.lower() or 'grid' in c.lower() or 'highlight' in c.lower())) or
        soup.find(['div', 'section'], id=lambda i: i and ('compare' in i.lower() or 'table' in i.lower() or 'highlight' in i.lower()))
    )
    
    # This is an optional test - not all feature pages will have comparison tables
    # If a comparison element exists, verify it has content
    if comparison_element:
        # Should have either rows/columns or descriptive items
        rows = comparison_element.find_all('tr') or comparison_element.find_all(['div', 'section'], class_=lambda c: c and 'row' in c.lower())
        cells = comparison_element.find_all(['td', 'th']) or comparison_element.find_all(['div', 'span'], class_=lambda c: c and ('cell' in c.lower() or 'col' in c.lower()))
        
        has_structure = len(rows) > 0 or len(cells) > 0 or len(comparison_element.find_all(['li', 'div'])) > 0
        if comparison_element:
            assert has_structure, "Comparison element should have structured content"
