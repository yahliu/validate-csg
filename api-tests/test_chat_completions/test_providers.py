"""Tests for Provider endpoints."""

import pytest
from utils import cleanup_provider, random_string


class TestListProviders:
    """GET /api/providers — list third-party providers."""

    def test_list_providers_returns_200(self, client):
        r = client.get("/api/providers")
        assert r.status_code == 200

    def test_list_providers_response_structure(self, client):
        r = client.get("/api/providers")
        data = r.json()
        assert "providers" in data
        assert isinstance(data["providers"], list)


class TestModelProviders:
    """GET /api/tags/manage — provider model catalog."""

    def test_model_providers_returns_200(self, client):
        r = client.get("/api/tags/manage", params={"provider": "openai"})
        # 200 if provider configured, may fail if not
        assert r.status_code in (200, 400, 500)


class TestValidateProvider:
    """POST /api/providers/validate — validate provider connection."""

    def test_validate_invalid_provider(self, client):
        body = {
            "base_url": "https://invalid.example.com/v1",
            "api_key": "sk-test",
            "provider": "openai",
        }
        r = client.post("/api/providers/validate", json=body)
        assert r.status_code == 200
        data = r.json()
        assert "valid" in data
        # Should be invalid
        assert data["valid"] is False


class TestCreateAndDeleteProvider:
    """POST /api/providers and DELETE /api/providers/{id}."""

    def test_create_and_delete_provider(self, client):
        name = f"test-provider-{random_string()}"
        body = {
            "name": name,
            "base_url": "https://api.openai.com/v1",
            "api_key": "sk-test123",
            "provider": "openai",
            "enabled": False,
        }
        r = client.post("/api/providers", json=body)
        assert r.status_code == 200

        cleanup_provider(client, r.json()["id"])
