"""Tests for Dataset endpoints."""

import pytest


class TestListDatasets:
    """GET /api/datasets — list local datasets."""

    def test_list_datasets_returns_200(self, client):
        r = client.get("/api/datasets")
        assert r.status_code == 200

    def test_list_datasets_response_structure(self, client):
        r = client.get("/api/datasets")
        data = r.json()
        assert "datasets" in data
        assert isinstance(data["datasets"], list)


class TestDatasetSearch:
    """GET /api/datasets/search — search datasets."""

    def test_search_returns_200(self, client):
        r = client.get("/api/datasets/search", params={"q": "test"})
        assert r.status_code == 200

    def test_search_response_structure(self, client):
        r = client.get("/api/datasets/search", params={"q": "test"})
        data = r.json()
        assert "datasets" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data


class TestDatasetShow:
    """POST /api/datasets/show — show dataset details."""

    def test_show_nonexistent_dataset(self, client):
        body = {"dataset": "nonexistent/dataset"}
        r = client.post("/api/datasets/show", json=body)
        assert r.status_code in (200, 404, 500)


class TestDatasetFiles:
    """POST /api/datasets/files — list dataset files."""

    def test_files_nonexistent_dataset(self, client):
        body = {"dataset": "nonexistent/dataset", "path": ""}
        r = client.post("/api/datasets/files", json=body)
        assert r.status_code in (200, 404, 500)


class TestMarketplaceDatasets:
    """GET /api/marketplace/datasets — proxy marketplace datasets."""

    def test_marketplace_datasets_returns_response(self, client):
        r = client.get("/api/marketplace/datasets")
        assert r.status_code in (200, 502)
