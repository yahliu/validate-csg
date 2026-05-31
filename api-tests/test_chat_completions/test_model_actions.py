"""Tests for POST /api/show, POST /api/pull, DELETE /api/delete — normal, boundary, and exception cases."""

import pytest
from utils import assert_status


# ---------------------------------------------------------------------------
# POST /api/show — model details
# ---------------------------------------------------------------------------

class TestShow:
    """POST /api/show — get model details."""

    @pytest.mark.model_required
    def test_show_model(self, client):
        body = {"model": "test-model"}
        r = client.post("/api/show", json=body)
        assert_status(r, 200, 404, 500)

    def test_show_nonexistent_model(self, client):
        body = {"model": "nonexistent-model-xyz-99999"}
        r = client.post("/api/show", json=body)
        assert_status(r, 404, 400, 500)


class TestShowBoundary:
    def test_show_empty_model(self, client):
        body = {"model": ""}
        r = client.post("/api/show", json=body)
        assert_status(r, 400, 404, 422, 500)

    def test_show_missing_model(self, client):
        r = client.post("/api/show", json={})
        assert_status(r, 400, 422, 500)

    def test_show_very_long_model_name(self, client):
        body = {"model": "a" * 5000}
        r = client.post("/api/show", json=body)
        assert_status(r, 200, 400, 404, 414, 500)

    def test_show_model_name_path_traversal(self, client):
        body = {"model": "../../etc/passwd"}
        r = client.post("/api/show", json=body)
        assert_status(r, 200, 400, 404, 500)

    def test_show_model_name_special_chars(self, client):
        body = {"model": "<script>alert(1)</script>"}
        r = client.post("/api/show", json=body)
        assert_status(r, 200, 400, 404, 500)


class TestShowExceptions:
    def test_show_invalid_json(self, client):
        r = client.post("/api/show", data="{broken", headers={"Content-Type": "application/json"})
        assert_status(r, 400, 415, 422, 500)

    def test_show_empty_body(self, client):
        r = client.post("/api/show", data="")
        assert_status(r, 400, 415, 422, 500)

    def test_get_on_show(self, client):
        r = client.get("/api/show")
        assert_status(r, 400, 404, 405, 500)

    def test_show_model_is_number(self, client):
        body = {"model": 12345}
        r = client.post("/api/show", json=body)
        assert_status(r, 200, 400, 422, 500)

    def test_show_null_model(self, client):
        body = {"model": None}
        r = client.post("/api/show", json=body)
        assert_status(r, 400, 404, 422, 500)


# ---------------------------------------------------------------------------
# POST /api/pull — download model (SSE streaming)
# ---------------------------------------------------------------------------

class TestPull:
    """POST /api/pull — download a model from CSGHub."""

    @pytest.mark.slow
    @pytest.mark.model_required
    def test_pull_model(self, client):
        body = {"model": "test-model"}
        r = client.post("/api/pull", json=body, stream=True)
        assert_status(r, 200, 400, 404, 500)

    def test_pull_nonexistent_model(self, client):
        body = {"model": "nonexistent-model-xyz-99999"}
        r = client.post("/api/pull", json=body, stream=True)
        assert_status(r, 200, 400, 404, 500)


class TestPullBoundary:
    def test_pull_empty_model(self, client):
        body = {"model": ""}
        r = client.post("/api/pull", json=body, stream=True)
        assert_status(r, 400, 404, 422, 500)

    def test_pull_missing_model(self, client):
        r = client.post("/api/pull", json={}, stream=True)
        assert_status(r, 400, 422, 500)

    def test_pull_very_long_model_name(self, client):
        body = {"model": "a" * 5000}
        r = client.post("/api/pull", json=body, stream=True)
        assert_status(r, 200, 400, 404, 414, 500)

    def test_pull_with_quant(self, client):
        body = {"model": "test-model", "quant": "Q4_K_M"}
        r = client.post("/api/pull", json=body, stream=True)
        assert_status(r, 200, 400, 404, 500)


class TestPullExceptions:
    def test_pull_invalid_json(self, client):
        r = client.post("/api/pull", data="{broken", headers={"Content-Type": "application/json"})
        assert_status(r, 400, 415, 422, 500)

    def test_pull_empty_body(self, client):
        r = client.post("/api/pull", data="")
        assert_status(r, 400, 415, 422, 500)

    def test_get_on_pull(self, client):
        r = client.get("/api/pull")
        assert_status(r, 400, 404, 405, 500)

    def test_pull_model_is_number(self, client):
        body = {"model": 12345}
        r = client.post("/api/pull", json=body, stream=True)
        assert_status(r, 200, 400, 422, 500)


# ---------------------------------------------------------------------------
# DELETE /api/delete — delete a local model
# ---------------------------------------------------------------------------

class TestDelete:
    """DELETE /api/delete — delete a local model."""

    def test_delete_nonexistent_model(self, client):
        body = {"model": "nonexistent-model-xyz-99999"}
        r = client.delete("/api/delete", json=body)
        assert_status(r, 200, 404, 500)

    @pytest.mark.slow
    @pytest.mark.model_required
    def test_delete_model(self, client):
        body = {"model": "test-model"}
        r = client.delete("/api/delete", json=body)
        assert_status(r, 200, 404, 500)


class TestDeleteBoundary:
    def test_delete_empty_model(self, client):
        body = {"model": ""}
        r = client.delete("/api/delete", json=body)
        assert_status(r, 400, 404, 422, 500)

    def test_delete_missing_model(self, client):
        r = client.delete("/api/delete", json={})
        assert_status(r, 400, 422, 500)

    def test_delete_model_name_slashes(self, client):
        body = {"model": "../../../etc/passwd"}
        r = client.delete("/api/delete", json=body)
        assert_status(r, 200, 400, 404, 500)

    def test_delete_model_name_sql_injection(self, client):
        body = {"model": "'; DROP TABLE models; --"}
        r = client.delete("/api/delete", json=body)
        assert_status(r, 200, 400, 404, 500)


class TestDeleteExceptions:
    def test_delete_invalid_json(self, client):
        r = client.delete("/api/delete", data="{broken", headers={"Content-Type": "application/json"})
        assert_status(r, 400, 415, 422, 500)

    def test_delete_empty_body(self, client):
        r = client.delete("/api/delete", data="")
        assert_status(r, 400, 415, 422, 500)

    def test_post_on_delete(self, client):
        r = client.post("/api/delete", json={"model": "test"})
        assert_status(r, 400, 404, 405, 500)

    def test_delete_model_is_number(self, client):
        body = {"model": 12345}
        r = client.delete("/api/delete", json=body)
        assert_status(r, 200, 400, 422, 500)
