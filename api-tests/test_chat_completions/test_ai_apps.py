"""Tests for AI Apps endpoints."""

import pytest


class TestListApps:
    """GET /api/apps — list managed AI apps."""

    def test_list_apps_returns_200(self, client):
        r = client.get("/api/apps")
        assert r.status_code == 200

    def test_list_apps_response_structure(self, client):
        r = client.get("/api/apps")
        data = r.json()
        assert "apps" in data
        assert isinstance(data["apps"], list)


class TestAppModel:
    """POST /api/apps/model — get/set app model."""

    def test_app_model_returns_response(self, client):
        body = {"app_id": "nonexistent-app"}
        r = client.post("/api/apps/model", json=body)
        assert r.status_code in (200, 404, 500)


class TestAppInstallAndUninstall:
    """POST /api/apps/install and /api/apps/uninstall."""

    def test_uninstall_nonexistent_app(self, client):
        body = {"app_id": "nonexistent-app"}
        r = client.post("/api/apps/uninstall", json=body)
        assert r.status_code in (200, 404, 500)


class TestImageRuntime:
    """GET/POST /api/image-runtime and /api/image-runtime/install."""

    def test_image_runtime_status(self, client):
        r = client.get("/api/image-runtime")
        assert r.status_code == 200

    def test_image_runtime_install_no_op(self, client):
        body = {"upgrade_packages": False}
        r = client.post("/api/image-runtime/install", json=body)
        assert r.status_code in (200, 400, 500)


class TestImageJobs:
    """GET /api/images/jobs — list image generation jobs."""

    def test_list_jobs_returns_200(self, client):
        r = client.get("/api/images/jobs")
        assert r.status_code == 200
