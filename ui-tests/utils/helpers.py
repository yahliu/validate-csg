"""Shared helpers for csgclaw UI tests."""

import json
import subprocess

from playwright.sync_api import Page


def go(page: Page, url: str, timeout: int = 15000):
    """Navigate to a URL with commit-only wait — tolerant of backend being unreachable."""
    try:
        page.goto(url, wait_until="commit", timeout=timeout)
    except Exception:
        pass
    page.wait_for_timeout(1000)


def cleanup_agent(name: str):
    """Delete an agent by name via csgclaw CLI (ID = u-{name})."""
    agent_id = f"u-{name}"
    try:
        subprocess.run(
            ["csgclaw", "agent", "delete", agent_id],
            capture_output=True,
            timeout=15,
        )
    except Exception:
        pass


def cleanup_room(title: str):
    """Delete a room by title via csgclaw CLI."""
    try:
        result = subprocess.run(
            ["csgclaw", "room", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        rooms = json.loads(result.stdout)
        for room in rooms:
            if room.get("title") == title:
                subprocess.run(
                    ["csgclaw", "room", "delete", room["id"]],
                    capture_output=True,
                    timeout=15,
                )
                break
    except Exception:
        pass
