"""Tests for API Key management endpoints."""

import pytest
from utils import cleanup_key, random_string


class TestListAPIKeys:
    """GET /api/api-keys — list API keys."""

    def test_list_keys_returns_200(self, client):
        r = client.get("/api/api-keys")
        assert r.status_code == 200

    def test_list_keys_response_structure(self, client):
        r = client.get("/api/api-keys")
        data = r.json()
        assert "auth_enabled" in data
        assert "keys" in data
        assert isinstance(data["keys"], list)


class TestAPIKeySettings:
    """GET/PATCH /api/api-keys/settings — auth settings."""

    def test_get_settings_returns_200(self, client):
        r = client.get("/api/api-keys/settings")
        assert r.status_code == 200

    def test_get_settings_has_auth_enabled(self, client):
        r = client.get("/api/api-keys/settings")
        data = r.json()
        assert "auth_enabled" in data

    def test_update_auth_settings(self, client):
        body = {"auth_enabled": True}
        r = client.patch("/api/api-keys/settings", json=body)
        assert r.status_code == 200


class TestCreateAndDeleteAPIKey:
    """POST /api/api-keys and DELETE /api/api-keys/{id}."""

    def test_create_key(self, client):
        name = f"test-key-{random_string()}"
        body = {"name": name}
        r = client.post("/api/api-keys", json=body)
        assert r.status_code == 200
        data = r.json()
        assert "key" in data
        assert "api_key" in data

        cleanup_key(client, data["key"]["id"])


class TestAPIUsage:
    """GET /api/api-usage — usage statistics."""

    def test_usage_returns_200(self, client):
        r = client.get("/api/api-usage")
        assert r.status_code == 200

    def test_usage_response_structure(self, client):
        r = client.get("/api/api-usage")
        data = r.json()
        assert "totals" in data
        assert "rows" in data
        totals = data["totals"]
        assert "requests" in totals
        assert "input_tokens" in totals
        assert "output_tokens" in totals
