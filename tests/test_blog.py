"""
Smoke tests for /blog. The pre-rewrite version of these tests asserted
on hardcoded "John Doe" mock content; the blog is now real CRUD against
the BlogPost model (see tests/test_blog_model.py for unit coverage), so
these tests verify only the structural contract of the public listing.
"""
import pytest
from starlette.testclient import TestClient
from bs4 import BeautifulSoup

import main
from app import app
from users.models import BlogPost, User


client = TestClient(app)


@pytest.fixture
def published_post(transactional_db):
    """Seed one published post so the listing renders with content.

    Uses `transactional_db` (real commits) instead of `db` (savepoints)
    because the FastHTML TestClient runs request handling in a separate
    thread, and sqlite blocks cross-connection reads inside an open
    transaction.
    """
    author = User.objects.create_user(
        email="seed@example.com", username="seed", password="x-not-real",
    )
    return BlogPost.objects.create(
        author=author,
        title="Seeded Post",
        content="# Heading\n\nBody.",
        excerpt="Seeded summary.",
        is_published=True,
    )


def test_blog_route_exists():
    """The /blog route returns 200 (no auth required)."""
    response = client.get("/blog")
    assert response.status_code == 200


def test_blog_route_accessible_without_auth():
    """The /blog route does not redirect anonymous visitors."""
    response = client.get("/blog", follow_redirects=False)
    assert response.status_code == 200


def test_blog_page_structure():
    """The blog page renders the layout chrome regardless of post count."""
    response = client.get("/blog")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Site chrome — note the SiteHeader component uses camelCase class names
    # (siteHeader, mainNav, navCenter, etc.). This is intentional in the
    # current codebase; test_blog used to assert on kebab-case but never
    # matched reality.
    assert soup.find('header', class_='siteHeader') is not None
    assert soup.find('nav', class_='mainNav') is not None

    # Blog layout container + section header (page title + write button)
    assert soup.find('div', class_='blog-container') is not None
    assert soup.find('div', class_='section-header') is not None
    assert soup.find('h1', string='Latest Posts') is not None


def test_blog_post_card_structure(published_post):
    """When a published post exists, /blog renders a real post card."""
    response = client.get("/blog")
    soup = BeautifulSoup(response.content, 'html.parser')

    posts_grid = soup.find('div', class_='posts-grid')
    assert posts_grid is not None, "posts-grid div should render when published posts exist"

    post_cards = posts_grid.find_all('article', class_='post-card')
    assert len(post_cards) >= 1, "expected at least one post card"

    first = post_cards[0]
    assert first.find('div', class_='post-header') is not None
    assert first.find('h2', class_='post-title') is not None
    assert first.find('p', class_='post-description') is not None


def test_write_post_button_exists():
    """The Write Post call-to-action links to /blog/write (or /login when anonymous)."""
    response = client.get("/blog")
    soup = BeautifulSoup(response.content, 'html.parser')

    write_btn = soup.find(class_='write-post-btn')
    assert write_btn is not None, "write-post-btn anchor should exist on /blog"

    href = write_btn.get('href', '')
    assert '/blog/write' in href or '/login' in href, (
        f"write button should link to /blog/write or /login, got: {href!r}"
    )


def test_write_post_route_redirects_unauthenticated():
    """Anonymous visitors hitting /blog/write are redirected to /login."""
    response = client.get("/blog/write", follow_redirects=False)
    assert response.status_code in [302, 303]
    assert "/login" in response.headers.get("location", "")
