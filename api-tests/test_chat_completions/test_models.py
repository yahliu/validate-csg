"""Tests for Model endpoints."""

import pytest


class TestListModels:
    """GET /api/tags — list available models."""

    def test_tags_returns_200(self, client):
        r = client.get("/api/tags")
        assert r.status_code == 200

    def test_tags_returns_models_list(self, client):
        r = client.get("/api/tags")
        data = r.json()
        assert "models" in data
        assert isinstance(data["models"], list)

    def test_tags_filter_by_provider_local(self, client):
        r = client.get("/api/tags", params={"provider": "local"})
        assert r.status_code == 200
        data = r.json()
        for model in data.get("models", []):
            assert model.get("source") == "local" or model.get("source") is None

    def test_tags_filter_by_category(self, client):
        """Filter by language_model category should work."""
        r = client.get("/api/tags", params={"category": "language_model"})
        # 200 even if no matching models
        assert r.status_code == 200


class TestPipelineTags:
    """GET /api/pipeline-tags — supported pipeline tags."""

    def test_pipeline_tags_returns_200(self, client):
        r = client.get("/api/pipeline-tags")
        assert r.status_code == 200

    def test_pipeline_tags_has_categories(self, client):
        r = client.get("/api/pipeline-tags")
        data = r.json()
        assert "pipeline_tags" in data
        tags = data["pipeline_tags"]
        if tags:
            assert "category" in tags[0]
            assert "tags" in tags[0]


class TestModelSearch:
    """GET /api/models/search — search models."""

    def test_search_returns_200(self, client):
        r = client.get("/api/models/search", params={"q": "llama"})
        assert r.status_code == 200

    def test_search_response_structure(self, client):
        r = client.get("/api/models/search", params={"q": "test"})
        data = r.json()
        assert "models" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data


class TestPsRunningModels:
    """GET /api/ps — list running models."""

    def test_ps_returns_200(self, client):
        r = client.get("/api/ps")
        assert r.status_code == 200

    def test_ps_has_models_list(self, client):
        r = client.get("/api/ps")
        data = r.json()
        assert "models" in data
        assert isinstance(data["models"], list)


class TestMarketplaceModels:
    """GET /api/marketplace/models — proxy marketplace models."""

    def test_marketplace_models_returns_200(self, client):
        r = client.get("/api/marketplace/models")
        assert r.status_code in (200, 502)  # 502 if no csghub server configured

    def test_marketplace_datasets_returns_200(self, client):
        r = client.get("/api/marketplace/datasets")
        assert r.status_code in (200, 502)


class TestModelManifest:
    """GET /api/models/{namespace}/{name}/manifest — model file manifest."""

    @pytest.mark.model_required
    def test_manifest_for_known_model(self, client):
        """Try to get manifest for a model. May 404 if model doesn't exist."""
        r = client.get("/api/models/testorg/testmodel/manifest")
        # Either 200 (model exists) or 404 (not found)
        assert r.status_code in (200, 404)
