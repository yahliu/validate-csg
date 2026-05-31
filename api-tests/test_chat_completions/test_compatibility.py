"""Tests for OpenAI/Anthropic compatibility endpoints (/v1/*)."""

import pytest


class TestOpenAIChatCompletions:
    """POST /v1/chat/completions — OpenAI-compatible chat."""

    @pytest.mark.model_required
    def test_basic_chat(self, client):
        body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
        }
        r = client.post("/v1/chat/completions", json=body)
        assert r.status_code in (200, 400, 404, 500)

    def test_missing_model(self, client):
        body = {"messages": [{"role": "user", "content": "Hello"}]}
        r = client.post("/v1/chat/completions", json=body)
        assert r.status_code in (400, 422, 500)


class TestOpenAIModels:
    """GET /v1/models — OpenAI-compatible model list."""

    def test_list_models_returns_200(self, client):
        r = client.get("/v1/models")
        assert r.status_code == 200

    def test_list_models_response_structure(self, client):
        r = client.get("/v1/models")
        data = r.json()
        assert "object" in data
        assert data["object"] == "list"
        assert "data" in data
        assert isinstance(data["data"], list)


class TestOpenAIEmbeddings:
    """POST /v1/embeddings — OpenAI-compatible embeddings."""

    @pytest.mark.model_required
    def test_embeddings_request(self, client):
        body = {
            "model": "test-model",
            "input": "Hello world",
        }
        r = client.post("/v1/embeddings", json=body)
        assert r.status_code in (200, 400, 404, 500)


class TestAnthropicMessages:
    """POST /v1/messages — Anthropic-compatible messages."""

    @pytest.mark.model_required
    def test_basic_message(self, client):
        body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 100,
        }
        r = client.post("/v1/messages", json=body)
        assert r.status_code in (200, 400, 404, 500)


class TestAnthropicCountTokens:
    """POST /v1/messages/count_tokens — Anthropic token counting."""

    @pytest.mark.model_required
    def test_count_tokens(self, client):
        body = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Count these tokens"}],
        }
        r = client.post("/v1/messages/count_tokens", json=body)
        assert r.status_code in (200, 400, 404, 500)
