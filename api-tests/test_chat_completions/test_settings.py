"""Tests for Settings endpoints."""

import pytest


class TestGetSettings:
    """GET /api/settings — application settings."""

    def test_get_settings_returns_200(self, client):
        r = client.get("/api/settings")
        assert r.status_code == 200

    def test_get_settings_has_expected_fields(self, client):
        r = client.get("/api/settings")
        data = r.json()
        assert "version" in data
        assert "server_url" in data
        assert "autostart" in data

    def test_get_settings_version_is_string(self, client):
        r = client.get("/api/settings")
        data = r.json()
        assert isinstance(data["version"], str)


class TestUpdateSettings:
    """PATCH /api/settings — update application settings."""

    def test_update_autostart(self, client):
        # First get current value
        r = client.get("/api/settings")
        current = r.json().get("autostart", False)

        # Try to set it
        body = {"autostart": not current}
        r = client.patch("/api/settings", json=body)
        assert r.status_code == 200

        # Reset back
        r = client.patch("/api/settings", json={"autostart": current})
        assert r.status_code == 200

    def test_update_empty_payload_no_change(self, client):
        r = client.patch("/api/settings", json={})
        # Should accept empty update
        assert r.status_code == 200


class TestDirectories:
    """GET /api/settings/directories — browse directory."""

    def test_browse_root(self, client):
        r = client.get("/api/settings/directories")
        assert r.status_code == 200
        data = r.json()
        assert "current_path" in data
        assert "entries" in data

    def test_browse_home_directory(self, client):
        import os
        home = os.path.expanduser("~")
        r = client.get("/api/settings/directories", params={"path": home})
        data = r.json()
        assert data.get("current_path") == home
        assert isinstance(data.get("entries", []), list)
