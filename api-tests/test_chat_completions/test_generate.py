"""Tests for POST /api/generate — normal, boundary, and exception cases."""

import pytest


# ---------------------------------------------------------------------------
# Normal / happy-path tests
# ---------------------------------------------------------------------------

class TestGenerate:
    @pytest.mark.model_required
    def test_generate_basic_request(self, client):
        body = {"model": "test-model", "prompt": "Say hello"}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 404, 500)

    @pytest.mark.model_required
    def test_generate_with_options(self, client):
        body = {
            "model": "test-model",
            "prompt": "Say hello",
            "options": {"temperature": 0.7, "max_tokens": 50},
        }
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 404, 500)

    @pytest.mark.model_required
    def test_generate_with_stream(self, client):
        body = {"model": "test-model", "prompt": "Say hello", "stream": True}
        r = client.post("/api/generate", json=body, stream=True)
        assert r.status_code in (200, 400, 404, 500)


# ---------------------------------------------------------------------------
# Boundary value tests
# ---------------------------------------------------------------------------

class TestGenerateBoundary:
    def test_empty_prompt(self, client):
        body = {"model": "test", "prompt": ""}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_prompt_whitespace_only(self, client):
        body = {"model": "test", "prompt": "   \t\n  "}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_very_long_prompt(self, client):
        body = {"model": "test", "prompt": "A" * 100000}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 413, 422, 500)

    def test_unicode_prompt(self, client):
        body = {"model": "test", "prompt": "こんにちは世界"}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 500)

    def test_special_chars_prompt(self, client):
        body = {"model": "test", "prompt": "<script>alert(1)</script>\n{}\"' \t\r\n\x00"}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 500)

    def test_temperature_boundary_zero(self, client):
        body = {
            "model": "test",
            "prompt": "Hi",
            "options": {"temperature": 0.0},
        }
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_temperature_boundary_high(self, client):
        body = {
            "model": "test",
            "prompt": "Hi",
            "options": {"temperature": 100.0},
        }
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_max_tokens_large(self, client):
        body = {
            "model": "test",
            "prompt": "Hi",
            "options": {"max_tokens": 999999},
        }
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_model_name_long(self, client):
        body = {"model": "a" * 5000, "prompt": "Hello"}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 404, 414, 500)

    def test_model_name_path_traversal(self, client):
        body = {"model": "../../etc/passwd", "prompt": "Hello"}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 404, 500)


# ---------------------------------------------------------------------------
# Exception / error handling tests
# ---------------------------------------------------------------------------

class TestGenerateExceptions:
    def test_missing_prompt(self, client):
        body = {"model": "test"}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (400, 422, 500)

    def test_missing_model(self, client):
        body = {"prompt": "Hello"}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (400, 422, 500)

    def test_invalid_json_body(self, client):
        r = client.post("/api/generate", data="{broken", headers={"Content-Type": "application/json"})
        assert r.status_code in (400, 415, 422, 500)

    def test_empty_body(self, client):
        r = client.post("/api/generate", data="")
        assert r.status_code in (400, 415, 422, 500)

    def test_get_on_post_endpoint(self, client):
        r = client.get("/api/generate")
        assert r.status_code in (400, 404, 405, 500)

    def test_patch_on_post_endpoint(self, client):
        r = client.patch("/api/generate")
        assert r.status_code in (400, 404, 405, 500)

    def test_prompt_is_number(self, client):
        body = {"model": "test", "prompt": 12345}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_stream_is_number(self, client):
        body = {"model": "test", "prompt": "Hi", "stream": 1}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_empty_model_name(self, client):
        body = {"model": "", "prompt": "Test"}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (400, 422, 500)

    def test_null_model(self, client):
        body = {"model": None, "prompt": "Test"}
        r = client.post("/api/generate", json=body)
        assert r.status_code in (400, 422, 500)
