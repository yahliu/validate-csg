"""Tests for Conversation endpoints."""

import pytest
from utils import cleanup_conversation


class TestListConversations:
    """GET /api/conversations — list conversations."""

    def test_list_conversations_returns_200(self, client):
        r = client.get("/api/conversations")
        assert r.status_code == 200

    def test_list_conversations_response_structure(self, client):
        r = client.get("/api/conversations")
        data = r.json()
        assert "conversations" in data
        assert isinstance(data["conversations"], list)

    def test_conversation_meta_fields(self, client):
        r = client.get("/api/conversations")
        data = r.json()
        for conv in data.get("conversations", []):
            assert "id" in conv
            assert "title" in conv
            assert "created_at" in conv
            assert "updated_at" in conv
            assert "msg_count" in conv


class TestConversationCRUD:
    """CRUD on /api/conversations and /api/conversations/{id}."""

    def test_create_conversation(self, client):
        body = {"title": "Test conversation", "model": "", "messages": []}
        r = client.post("/api/conversations", json=body)
        assert r.status_code == 200
        conv_id = r.json()["id"]

        r = client.get(f"/api/conversations/{conv_id}")
        assert r.status_code == 200

        r = client.patch(f"/api/conversations/{conv_id}", json={"title": "Updated title"})
        assert r.status_code == 200

        cleanup_conversation(client, conv_id)

    def test_get_nonexistent_conversation(self, client):
        r = client.get("/api/conversations/nonexistent-id")
        assert r.status_code == 404
