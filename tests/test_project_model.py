"""
Unit tests for the Project model added in Day 8 (users/models.py).

Covers: auto-slug generation, ai_percentage clamping, ordering, and the
unique_together constraint that prevents the same owner from having two
projects with the same slug.
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

from users.models import Project, User


@pytest.fixture
def owner(db):
    return User.objects.create_user(
        email="owner@example.com",
        username="owner",
        password="testpass-not-real",
    )


@pytest.mark.django_db
def test_auto_slug_on_save(owner):
    p = Project.objects.create(owner=owner, name="My Cool App")
    assert p.slug == "my-cool-app"


@pytest.mark.django_db
def test_explicit_slug_preserved(owner):
    p = Project.objects.create(owner=owner, name="Whatever", slug="custom")
    assert p.slug == "custom"


@pytest.mark.django_db
def test_ai_percentage_clamped_high(owner):
    p = Project.objects.create(owner=owner, name="A", ai_percentage=999)
    p.refresh_from_db()
    assert p.ai_percentage == 100


@pytest.mark.django_db
def test_unique_together_blocks_duplicate_slug(owner):
    Project.objects.create(owner=owner, name="Same Name")
    with pytest.raises(IntegrityError):
        Project.objects.create(owner=owner, name="Same Name")


@pytest.mark.django_db
def test_ordering_is_recent_first(owner):
    a = Project.objects.create(owner=owner, name="First")
    b = Project.objects.create(owner=owner, name="Second")
    # Touch `a` so it's now the most-recently-updated
    a.description = "edited"
    a.save()
    qs = list(Project.objects.filter(owner=owner))
    assert qs[0] == a
    assert qs[1] == b


@pytest.mark.django_db
def test_get_absolute_url(owner):
    p = Project.objects.create(owner=owner, name="Foo Bar")
    assert p.get_absolute_url() == "/dashboard/project/foo-bar"


@pytest.mark.django_db
def test_str_repr(owner):
    p = Project.objects.create(owner=owner, name="X")
    assert "owner" in str(p) and "X" in str(p)
