"""Pytest fixtures for csgclaw UI tests."""

import pytest
from config import UI_BASE_URL, DEFAULT_TIMEOUT


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override default browser context args."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def base_url():
    return UI_BASE_URL


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "smoke: core smoke tests")
