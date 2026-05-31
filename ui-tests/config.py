"""Configuration for csgclaw UI tests."""

import os

# The base URL where csgclaw UI is accessible
UI_BASE_URL = os.environ.get("CSGCLAW_UI_URL", "http://127.0.0.1:18080")

# Timeouts
DEFAULT_TIMEOUT = 10000  # milliseconds
NAVIGATION_TIMEOUT = 15000  # milliseconds
