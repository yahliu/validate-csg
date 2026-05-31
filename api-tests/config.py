"""Configuration for csghub-lite API tests."""

import os

BASE_URL = os.environ.get("CSGHUB_BASE_URL", "http://localhost:11435")
API_KEY = os.environ.get("CSGHUB_API_KEY", "")

DEFAULT_TIMEOUT = 30  # seconds
