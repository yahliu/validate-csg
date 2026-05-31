"""Shared helper functions for API tests."""

import string
import random


def assert_status(response, *valid_statuses, status_code=None):
    """Assert response status is one of the valid codes.

    Usage:
        assert_status(r, 200)                    # single code
        assert_status(r, 200, 400, 422)          # multiple codes
        assert_status(r, status_code=200)         # keyword style
    """
    if status_code is not None:
        valid = (status_code,)
    else:
        valid = valid_statuses
    assert response.status_code in valid, \
        f"Expected status in {valid}, got {response.status_code}: {response.text[:500]}"


def random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def cleanup_key(client, key_id: str):
    """Try to delete an API key; ignore failures."""
    try:
        client.delete(f"/api/api-keys/{key_id}")
    except Exception:
        pass


def cleanup_provider(client, provider_id: str):
    """Try to delete a provider; ignore failures."""
    try:
        client.delete(f"/api/providers/{provider_id}")
    except Exception:
        pass


def cleanup_conversation(client, conv_id: str):
    """Try to delete a conversation; ignore failures."""
    try:
        client.delete(f"/api/conversations/{conv_id}")
    except Exception:
        pass
