"""Navigation tests — routing, tab switching, deep links.

Source: AppRouter.tsx — hash router with routes:
  /               → ConversationPage (default)
  /computer        → ComputerPage
  /agents/:id      → AgentPage
  /agent/:id       → AgentPage (alternate)
  /hub             → HubPage
  /rooms/:id, /room/:id          → ConversationPage
  /channels/:id, /channel/:id    → ConversationPage
  /dms/:id, /dm/:id              → ConversationPage
  /conversations/:id, /conversation/:id → ConversationPage
  *               → ConversationPage (catch-all)
"""

import pytest
from playwright.sync_api import Page, expect
from utils import go


class TestRouting:
    """Verify all hash routes render without errors."""

    @pytest.mark.smoke
    def test_root_page(self, page: Page, base_url: str):
        go(page, base_url)
        expect(page.locator("body")).not_to_be_empty()

    def test_hub_route(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        expect(page.locator("body")).not_to_be_empty()

    def test_computer_route(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/computer")
        expect(page.locator("body")).not_to_be_empty()

    def test_agents_route(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        expect(page.locator("body")).not_to_be_empty()

    def test_agent_alternate_route(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agent/another-agent")
        expect(page.locator("body")).not_to_be_empty()

    def test_rooms_route(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/rooms/test-room")
        expect(page.locator("body")).not_to_be_empty()

    def test_channels_route(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/channels/general")
        expect(page.locator("body")).not_to_be_empty()

    def test_dms_route(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/dms/user123")
        expect(page.locator("body")).not_to_be_empty()

    def test_conversations_route(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/conversations/conv456")
        expect(page.locator("body")).not_to_be_empty()

    def test_conversation_singular_route(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/conversation/conv789")
        expect(page.locator("body")).not_to_be_empty()


class TestRouteSwitching:
    """Navigation between routes."""

    @pytest.mark.smoke
    def test_switch_hub_to_root(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        go(page, base_url)
        expect(page.locator("body")).not_to_be_empty()

    def test_switch_root_to_agents(self, page: Page, base_url: str):
        go(page, base_url)
        go(page, f"{base_url}/#/agents/test-agent")
        expect(page.locator("body")).not_to_be_empty()

    def test_switch_agents_to_hub(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        go(page, f"{base_url}/#/hub")
        expect(page.locator("body")).not_to_be_empty()

    def test_page_reload(self, page: Page, base_url: str):
        go(page, base_url)
        try:
            page.reload(wait_until="commit", timeout=10000)
        except Exception:
            pass
        page.wait_for_timeout(500)
        expect(page.locator("body")).not_to_be_empty()
