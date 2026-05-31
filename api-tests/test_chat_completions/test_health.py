"""Tests for Health endpoint."""

import pytest


class TestHealth:
    """GET /api/health — basic server health check."""

    def test_health_returns_200(self, client):
        r = client.get("/api/health")
        assert r.status_code == 200

    def test_health_returns_json(self, client):
        r = client.get("/api/health")
        data = r.json()
        assert "status" in data
        assert data["status"] == "ok"

    def test_health_no_auth_required(self, client):
        """Health check should work without auth."""
        r = client.get("/api/health")
        assert r.status_code == 200


class TestSystemInfo:
    """GET /api/system — system info endpoint."""

    def test_system_returns_200(self, client):
        r = client.get("/api/system")
        assert r.status_code == 200

    def test_system_has_expected_fields(self, client):
        r = client.get("/api/system")
        assert r.status_code == 200
        data = r.json()
        # System response should at least have some info
        assert isinstance(data, dict)
