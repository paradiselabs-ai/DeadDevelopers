"""
Unit tests for routes/ai.py — the OpenRouter-backed AI assistant.

These tests exercise the rate-limit, prompt-cap, missing-config, and
exception-swallowing paths without ever calling OpenRouter. The provider
client is lazy-built per-call, so we just patch _get_client to return a
mock or None as needed.
"""
import asyncio
import os
import sys
import django
from unittest.mock import AsyncMock, MagicMock, patch
import pytest


# Bootstrap Django before importing the route module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_config.settings")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not django.apps.apps.ready:
    django.setup()


from django.core.cache import cache  # noqa: E402

from routes import ai as ai_module  # noqa: E402


def _run(coro):
    # asyncio.get_event_loop() raises in Python 3.12+ when there's no
    # current loop. asyncio.run() creates and tears down a fresh loop
    # per call, which is what we want for unit tests.
    return asyncio.run(coro)


@pytest.fixture(autouse=True)
def _reset_state():
    """Each test starts with a clean cache + no cached client."""
    cache.clear()
    ai_module._client = None
    yield
    cache.clear()
    ai_module._client = None


def test_returns_friendly_message_when_no_api_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    out = _run(ai_module.get_ai_response("hi", user_id=1))
    assert "not configured" in out.lower()


def test_rejects_empty_prompt(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    with patch.object(ai_module, "_get_client", return_value=MagicMock()):
        out = _run(ai_module.get_ai_response("   ", user_id=1))
    assert "type a question" in out.lower()


def test_rejects_oversize_prompt(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    with patch.object(ai_module, "_get_client", return_value=MagicMock()):
        out = _run(ai_module.get_ai_response(
            "x" * (ai_module.MAX_PROMPT_CHARS + 1), user_id=1
        ))
    assert "too long" in out.lower()


def test_rate_limit_blocks_after_quota():
    # Pre-fill the cache so the first call is already over quota.
    cache.set(f"ai_ratelimit_42", ai_module.RATE_LIMIT_PER_HOUR, 3600)

    fake_client = MagicMock()
    fake_client.chat.completions.create = AsyncMock(
        side_effect=AssertionError("API should not be called when rate-limited")
    )
    with patch.object(ai_module, "_get_client", return_value=fake_client):
        out = _run(ai_module.get_ai_response("hello", user_id=42))

    assert "rate limit" in out.lower()


def test_happy_path_returns_model_text():
    fake_client = MagicMock()
    fake_choice = MagicMock()
    fake_choice.message.content = "Use a binary search."
    fake_response = MagicMock()
    fake_response.choices = [fake_choice]
    fake_client.chat.completions.create = AsyncMock(return_value=fake_response)

    with patch.object(ai_module, "_get_client", return_value=fake_client):
        out = _run(ai_module.get_ai_response("how do I find an item fast?", user_id=7))

    assert out == "Use a binary search."
    fake_client.chat.completions.create.assert_awaited_once()


def test_provider_exception_returns_safe_message():
    fake_client = MagicMock()
    fake_client.chat.completions.create = AsyncMock(
        side_effect=RuntimeError("openrouter exploded")
    )
    with patch.object(ai_module, "_get_client", return_value=fake_client):
        out = _run(ai_module.get_ai_response("hi", user_id=1))

    # User-facing text should never leak the internal exception
    assert "openrouter exploded" not in out
    assert "temporarily unavailable" in out.lower()


def test_rate_limit_increments_per_user():
    fake_client = MagicMock()
    fake_choice = MagicMock()
    fake_choice.message.content = "ok"
    fake_response = MagicMock()
    fake_response.choices = [fake_choice]
    fake_client.chat.completions.create = AsyncMock(return_value=fake_response)

    with patch.object(ai_module, "_get_client", return_value=fake_client):
        _run(ai_module.get_ai_response("a", user_id=99))
        _run(ai_module.get_ai_response("b", user_id=99))

    assert cache.get("ai_ratelimit_99") == 2
    # Different user has its own bucket
    assert cache.get("ai_ratelimit_100", 0) == 0
