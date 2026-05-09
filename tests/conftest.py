"""
Shared pytest configuration for the FastHTML test suite.

Most route tests hit `/` or `/login` etc. via Starlette's TestClient; those
routes go through AuthBridge which queries Django's session model. Without
explicit DB access enabled, pytest-django blocks the query with
`RuntimeError: Database access not allowed`.

We use `transactional_db` (real commits, table-truncate teardown) instead
of the faster `db` fixture (savepoints) because Starlette's TestClient
runs the ASGI app in a worker thread, and sqlite refuses cross-thread
reads inside an open transaction with `database table is locked`. Real
commits avoid that. Trade-off: the suite runs ~30% slower; production
runs against postgres where this doesn't matter.

Tests that specifically want to assert the no-DB invariant can opt out
by adding `@pytest.mark.no_db`.
"""
import pytest


@pytest.fixture(autouse=True)
def _enable_db_access_for_all_tests(request, transactional_db):
    """Grant Django DB access (with real commits) to every test."""
    if 'no_db' in request.keywords:
        return
    return transactional_db
