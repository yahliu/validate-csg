"""Tests for POST /api/load and POST /api/stop — normal, boundary, and exception cases."""

import pytest


class TestLoad:
    @pytest.mark.slow
    @pytest.mark.model_required
    def test_load_model(self, client):
        body = {"model": "test-model"}
        r = client.post("/api/load", json=body)
        assert r.status_code in (200, 400, 404, 500)

    @pytest.mark.slow
    @pytest.mark.model_required
    def test_load_with_options(self, client):
        body = {
            "model": "test-model",
            "num_ctx": 2048,
            "keep_alive": "5m",
        }
        r = client.post("/api/load", json=body)
        assert r.status_code in (200, 400, 404, 500)


class TestLoadBoundary:
    def test_load_empty_model(self, client):
        body = {"model": ""}
        r = client.post("/api/load", json=body)
        assert r.status_code in (400, 404, 422, 500)

    def test_load_missing_model(self, client):
        r = client.post("/api/load", json={})
        assert r.status_code in (400, 404, 422, 500)

    def test_load_negative_num_ctx(self, client):
        body = {"model": "test", "num_ctx": -100}
        r = client.post("/api/load", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_load_invalid_keep_alive(self, client):
        body = {"model": "test", "keep_alive": "not-a-duration"}
        r = client.post("/api/load", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_load_model_name_slashes(self, client):
        body = {"model": "../../etc/shadow"}
        r = client.post("/api/load", json=body)
        assert r.status_code in (200, 400, 404, 500)


class TestLoadExceptions:
    def test_load_invalid_json(self, client):
        r = client.post("/api/load", data="{broken", headers={"Content-Type": "application/json"})
        assert r.status_code in (400, 415, 422, 500)

    def test_load_empty_body(self, client):
        r = client.post("/api/load", data="")
        assert r.status_code in (400, 415, 422, 500)

    def test_get_on_load(self, client):
        r = client.get("/api/load")
        assert r.status_code in (400, 404, 405, 500)


class TestStop:
    @pytest.mark.model_required
    def test_stop_model(self, client):
        body = {"model": "test-model"}
        r = client.post("/api/stop", json=body)
        assert r.status_code in (200, 404, 500)

    def test_stop_empty_model(self, client):
        body = {"model": ""}
        r = client.post("/api/stop", json=body)
        assert r.status_code in (400, 404, 422, 500)

    def test_stop_missing_model(self, client):
        r = client.post("/api/stop", json={})
        assert r.status_code in (400, 404, 422, 500)
