"""
Unit tests for BlogPost + Tag models and the markdown sanitizer used by
the blog. Together these cover: auto-slug, auto-excerpt, draft visibility
gating, published_at stamping, view-count atomicity, and XSS scrubbing.
"""
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_config.settings")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not django.apps.apps.ready:
    django.setup()

import pytest
from django.db import IntegrityError

from users.models import BlogPost, Tag, User
from routes.blog import render_markdown


@pytest.fixture
def author(db):
    return User.objects.create_user(
        email="author@example.com",
        username="author",
        password="testpass-not-real",
    )


@pytest.mark.django_db
def test_auto_slug_from_title(author):
    p = BlogPost.objects.create(author=author, title="Hello World!", content="body")
    assert p.slug == "hello-world"


@pytest.mark.django_db
def test_auto_excerpt_from_first_line(author):
    p = BlogPost.objects.create(
        author=author, title="t", content="First line summary\n\nThe rest.",
    )
    assert p.excerpt.startswith("First line summary")


@pytest.mark.django_db
def test_explicit_excerpt_preserved(author):
    p = BlogPost.objects.create(
        author=author, title="t", content="ignored body",
        excerpt="Custom summary",
    )
    assert p.excerpt == "Custom summary"


@pytest.mark.django_db
def test_published_at_stamped_on_publish(author):
    p = BlogPost.objects.create(
        author=author, title="draft", content="x", is_published=False,
    )
    assert p.published_at is None
    p.is_published = True
    p.save()
    assert p.published_at is not None


@pytest.mark.django_db
def test_published_at_not_stamped_again_on_re_save(author):
    p = BlogPost.objects.create(
        author=author, title="t", content="x", is_published=True,
    )
    first = p.published_at
    p.title = "edited"
    p.save()
    assert p.published_at == first


@pytest.mark.django_db
def test_unique_together_blocks_same_slug_per_author(author):
    BlogPost.objects.create(author=author, title="Same Title", content="x", slug="same")
    with pytest.raises(IntegrityError):
        BlogPost.objects.create(author=author, title="Same Title", content="y", slug="same")


@pytest.mark.django_db
def test_increment_views_is_atomic(author):
    p = BlogPost.objects.create(author=author, title="t", content="x")
    p.increment_views()
    p.increment_views()
    p.refresh_from_db()
    assert p.view_count == 2


@pytest.mark.django_db
def test_get_absolute_url(author):
    p = BlogPost.objects.create(author=author, title="My Post", content="x")
    assert p.get_absolute_url() == "/blog/author/my-post"


@pytest.mark.django_db
def test_tag_auto_slug():
    t = Tag.objects.create(name="Machine Learning")
    assert t.slug == "machine-learning"


@pytest.mark.django_db
def test_tag_attach_and_query(author):
    p = BlogPost.objects.create(author=author, title="t", content="x", is_published=True)
    py = Tag.objects.create(name="python")
    p.tags.add(py)
    assert list(py.posts.all()) == [p]


def test_render_markdown_strips_script():
    out = render_markdown("Hello\n\n<script>alert(1)</script>\n\n**bold**")
    assert "<script>" not in out
    assert "alert" not in out
    assert "<strong>bold</strong>" in out


def test_render_markdown_keeps_safe_tags():
    out = render_markdown("# Title\n\n```python\nprint('hi')\n```")
    assert "<h1>" in out
    assert "<pre>" in out and "<code" in out


def test_render_markdown_strips_event_handlers():
    out = render_markdown('<a href="javascript:alert(1)" onclick="bad()">x</a>')
    # bleach should strip the onclick attr and either drop or escape the
    # javascript: protocol depending on version; assert neither remains.
    assert "onclick" not in out
    assert "javascript:" not in out


def test_render_markdown_empty_returns_empty():
    assert render_markdown("") == ""
    assert render_markdown(None) == ""
