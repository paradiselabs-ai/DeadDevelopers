"""
AI assistant — OpenRouter-backed chat completion.

Why OpenRouter and not the Anthropic SDK directly:
- Single account / single bill across providers (Claude, Llama, GPT, Gemini)
- Users can BYO API key later (post-MVP feature) without changing the wire format
- OpenRouter exposes an OpenAI-compatible API, so the standard `openai` SDK
  works as the client — no extra dependency.

Env vars:
- OPENROUTER_API_KEY (required for the assistant to function)
- OPENROUTER_DEFAULT_MODEL (optional, default: anthropic/claude-haiku-4-5)
- SITE_URL (optional, used in the HTTP-Referer header OpenRouter expects)
"""
import os
from openai import AsyncOpenAI
from django.core.cache import cache


DEFAULT_MODEL = os.environ.get(
    "OPENROUTER_DEFAULT_MODEL", "anthropic/claude-haiku-4-5"
)

SYSTEM_PROMPT = (
    "You are the AI coding assistant for DeadDevelopers — a community of "
    "developers who write 80%+ of their code with AI. Be terse, technical, "
    "and direct. Skip filler and disclaimers. Use fenced code blocks for "
    "code. Assume the user knows their stack and is asking a real question, "
    "not looking for a tutorial."
)

RATE_LIMIT_PER_HOUR = 20
MAX_TOKENS = 1024
MAX_PROMPT_CHARS = 8000

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI | None:
    """Lazily build the OpenAI-compatible client pointed at OpenRouter.

    Returns None when OPENROUTER_API_KEY is missing so callers can degrade
    gracefully (used for local dev without an AI key).
    """
    global _client
    if _client is not None:
        return _client

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return None

    _client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            # OpenRouter uses these for request attribution on their dashboard
            "HTTP-Referer": os.environ.get("SITE_URL", "https://deaddevelopers.com"),
            "X-Title": "DeadDevelopers",
        },
    )
    return _client


async def get_ai_response(prompt: str, user_id: int) -> str:
    """Send `prompt` to OpenRouter and return the assistant's reply text.

    - Per-user rate limit: 20 requests/hour (django.core.cache).
    - Token cap: 1024 (cost ceiling per call).
    - Prompt cap: 8000 chars (rough request-size guard).
    - Errors return a generic user-safe message; provider errors are not
      surfaced to the UI so we don't leak internals.
    """
    client = _get_client()
    if client is None:
        return (
            "AI assistant not configured yet. "
            "Set OPENROUTER_API_KEY in the server environment."
        )

    if not prompt or not prompt.strip():
        return "Type a question first."

    if len(prompt) > MAX_PROMPT_CHARS:
        return f"Prompt too long ({len(prompt)} chars > {MAX_PROMPT_CHARS})."

    rate_key = f"ai_ratelimit_{user_id}"
    used = cache.get(rate_key, 0)
    if used >= RATE_LIMIT_PER_HOUR:
        return (
            f"Rate limit reached ({RATE_LIMIT_PER_HOUR}/hour). "
            "Wait an hour or BYO key."
        )
    cache.set(rate_key, used + 1, 3600)

    try:
        msg = await client.chat.completions.create(
            model=DEFAULT_MODEL,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        text = msg.choices[0].message.content
        return text or "(empty response from model)"
    except Exception:
        return "AI assistant temporarily unavailable. Try again shortly."
