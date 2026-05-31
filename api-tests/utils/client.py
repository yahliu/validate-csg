"""API client wrapper for csghub-lite."""

import requests
from config import DEFAULT_TIMEOUT


class APIClient:
    """Thin wrapper around requests for csghub-lite API."""

    def __init__(self, base_url: str, api_key: str = ""):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"
        self.session.headers["Content-Type"] = "application/json"

    def get(self, path: str, **kwargs):
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    def post(self, path: str, **kwargs):
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        return self.session.post(f"{self.base_url}{path}", **kwargs)

    def put(self, path: str, **kwargs):
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        return self.session.put(f"{self.base_url}{path}", **kwargs)

    def patch(self, path: str, **kwargs):
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        return self.session.patch(f"{self.base_url}{path}", **kwargs)

    def delete(self, path: str, **kwargs):
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        return self.session.delete(f"{self.base_url}{path}", **kwargs)
