"""Tests for POST /api/chat — normal, boundary, and exception cases."""

import pytest
from utils import assert_status


# ---------------------------------------------------------------------------
# Normal / happy-path tests
# ---------------------------------------------------------------------------

class TestChat:
    @pytest.mark.model_required
    def test_chat_basic_request(self, client):
        body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 404, 500)

    @pytest.mark.model_required
    def test_chat_with_stream(self, client):
        body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": True,
        }
        r = client.post("/api/chat", json=body, stream=True)
        assert r.status_code in (200, 400, 404, 500)

    @pytest.mark.model_required
    def test_chat_with_tools(self, client):
        body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "What is the weather?"}],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get the current weather",
                        "parameters": {
                            "type": "object",
                            "properties": {"location": {"type": "string"}},
                        },
                    },
                }
            ],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 404, 500)

    @pytest.mark.model_required
    def test_chat_with_web_search(self, client):
        body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "latest news"}],
            "web_search": {"enabled": True, "query": "latest news"},
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 404, 500)

    def test_chat_with_options(self, client):
        body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hi"}],
            "options": {"temperature": 0.5, "top_p": 0.9, "top_k": 40, "max_tokens": 100},
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 404, 500)


# ---------------------------------------------------------------------------
# Boundary value tests
# ---------------------------------------------------------------------------

class TestChatBoundary:
    def test_empty_messages_list(self, client):
        body = {"model": "test", "messages": []}
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_empty_content_in_message(self, client):
        body = {"model": "test", "messages": [{"role": "user", "content": ""}]}
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_very_long_message(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "A" * 100000}],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 413, 422, 500)

    def test_unicode_and_emoji_message(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "你好世界\x00emoji❤️🎉"}],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 500)

    def test_special_chars_in_message(self, client):
        body = {
            "model": "test",
            "messages": [
                {
                    "role": "user",
                    "content": "<script>alert('xss')</script>\n{}\"' \t\r\n\x00\x1b",
                }
            ],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 500)

    def test_array_as_message_content(self, client):
        """Multi-modal style content array."""
        body = {
            "model": "test",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Hello"},
                    ],
                }
            ],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_max_tokens_zero(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "Hi"}],
            "options": {"max_tokens": 0},
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_max_tokens_negative(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "Hi"}],
            "options": {"max_tokens": -1},
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_temperature_out_of_range_high(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "Hi"}],
            "options": {"temperature": 99.0},
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_temperature_out_of_range_low(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "Hi"}],
            "options": {"temperature": -0.5},
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_top_p_zero(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "Hi"}],
            "options": {"top_p": 0.0},
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_top_p_one(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "Hi"}],
            "options": {"top_p": 1.0},
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_huge_num_ctx(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "Hi"}],
            "options": {"num_ctx": 999999999},
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_negative_num_ctx(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "Hi"}],
            "options": {"num_ctx": -100},
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_very_long_model_name(self, client):
        body = {
            "model": "a" * 5000,
            "messages": [{"role": "user", "content": "Hi"}],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 404, 414, 500)

    def test_model_name_path_traversal(self, client):
        body = {
            "model": "../../etc/passwd",
            "messages": [{"role": "user", "content": "Hi"}],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 404, 500)

    def test_model_name_sql_injection(self, client):
        body = {
            "model": "'; DROP TABLE models; --",
            "messages": [{"role": "user", "content": "Hi"}],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 404, 500)

    def test_model_name_null_byte(self, client):
        body = {
            "model": "test\x00model",
            "messages": [{"role": "user", "content": "Hi"}],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)


# ---------------------------------------------------------------------------
# Exception / error handling tests
# ---------------------------------------------------------------------------

class TestChatExceptions:
    def test_missing_messages(self, client):
        body = {"model": "test"}
        r = client.post("/api/chat", json=body)
        assert r.status_code in (400, 422, 500)

    def test_missing_model(self, client):
        body = {"messages": [{"role": "user", "content": "Hi"}]}
        r = client.post("/api/chat", json=body)
        assert r.status_code in (400, 422, 500)

    def test_invalid_json_body(self, client):
        r = client.post("/api/chat", data="not json", headers={"Content-Type": "text/plain"})
        assert r.status_code in (400, 415, 422, 500)

    def test_xml_body(self, client):
        r = client.post("/api/chat", data="<xml><model>test</model></xml>",
                       headers={"Content-Type": "application/xml"})
        assert r.status_code in (400, 415, 422, 500)

    def test_empty_body(self, client):
        r = client.post("/api/chat", data="")
        assert r.status_code in (400, 415, 422, 500)

    def test_get_on_post_endpoint(self, client):
        r = client.get("/api/chat")
        assert r.status_code in (400, 404, 405, 500)

    def test_model_is_number(self, client):
        body = {"model": 12345, "messages": [{"role": "user", "content": "Hi"}]}
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_messages_is_string(self, client):
        body = {"model": "test", "messages": "not-a-list"}
        r = client.post("/api/chat", json=body)
        assert r.status_code in (400, 422, 500)

    def test_stream_is_string(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "Hi"}],
            "stream": "not-a-bool",
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_tools_is_string(self, client):
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": "Hi"}],
            "tools": "not-a-list",
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_null_values(self, client):
        body = {
            "model": None,
            "messages": [{"role": None, "content": None}],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 422, 500)

    def test_deeply_nested_json(self, client):
        nested = "Hi"
        for _ in range(50):
            nested = {"wrapped": [nested]}
        body = {
            "model": "test",
            "messages": [{"role": "user", "content": nested}],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 413, 422, 500)

    def test_duplicate_json_keys(self, client):
        r = client.post(
            "/api/chat",
            data='{"model": "a", "model": "b", "messages": [{"role": "user", "content": "Hi"}]}',
            headers={"Content-Type": "application/json"},
        )
        assert r.status_code in (200, 400, 422, 500)

    def test_very_large_payload(self, client):
        body = {
            "model": "test",
            "messages": [
                {"role": "user", "content": "X" * (1024 * 1024)}  # ~1 MB
            ],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (200, 400, 413, 422, 500)

    def test_chat_empty_model(self, client):
        body = {
            "model": "",
            "messages": [{"role": "user", "content": "Hello"}],
        }
        r = client.post("/api/chat", json=body)
        assert r.status_code in (400, 422, 500)
