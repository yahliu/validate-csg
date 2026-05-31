"""Pytest fixtures for csghub-lite API tests."""

import pytest
from config import BASE_URL, API_KEY
from utils import APIClient


@pytest.fixture(scope="session")
def client():
    return APIClient(BASE_URL, API_KEY)


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "model_required: marks tests that need a model")
