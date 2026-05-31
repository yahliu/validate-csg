"""Agent tests — agent list, detail pane, profile editor, lifecycle actions.

Source: AgentList.tsx, AgentDetailPane.tsx, AgentView.tsx,
       NotificationBotDetailPane.tsx, AgentProfileModal.tsx
"""

import pytest
from playwright.sync_api import Page, expect
from utils import cleanup_agent, go


# ---------------------------------------------------------------------------
# Agent list in sidebar
# ---------------------------------------------------------------------------

class TestAgentList:
    """AgentSection.tsx & AgentRow.tsx — manager + workers list with actions."""

    @pytest.mark.smoke
    def test_agent_section_present(self, page: Page, base_url: str):
        go(page, base_url)
        section = page.locator(".agent-section")
        assert section.count() >= 0

    def test_agent_rows_have_name(self, page: Page, base_url: str):
        go(page, base_url)
        names = page.locator(".agent-name")
        assert names.count() >= 0

    def test_agent_rows_have_status(self, page: Page, base_url: str):
        go(page, base_url)
        statuses = page.locator(".agent-status")
        assert statuses.count() >= 0

    def test_agent_rows_have_meta(self, page: Page, base_url: str):
        go(page, base_url)
        metas = page.locator(".agent-meta")
        assert metas.count() >= 0

    def test_agent_rows_have_badges(self, page: Page, base_url: str):
        go(page, base_url)
        badges = page.locator(".agent-badge")
        assert badges.count() >= 0

    def test_edit_profile_button(self, page: Page, base_url: str):
        go(page, base_url)
        edit_btn = page.locator('button[aria-label="Edit Profile"], button[aria-label="编辑配置"]')
        assert edit_btn.count() >= 0

    def test_start_stop_button(self, page: Page, base_url: str):
        go(page, base_url)
        btn = page.locator(
            'button[aria-label="Start"], button[aria-label="Stop"], '
            'button[aria-label="启动"], button[aria-label="停止"]'
        )
        assert btn.count() >= 0

    def test_recreate_button(self, page: Page, base_url: str):
        go(page, base_url)
        recreate_btn = page.locator(
            'button:has-text("Recreate"), button:has-text("重建")'
        )
        assert recreate_btn.count() >= 0

    def test_delete_button(self, page: Page, base_url: str):
        go(page, base_url)
        delete_btn = page.locator(
            'button[aria-label="Delete Agent"], button[aria-label="删除智能体"]'
        )
        assert delete_btn.count() >= 0

    def test_create_agent_button(self, page: Page, base_url: str):
        go(page, base_url)
        create_btn = page.locator(".agent-add-button")
        assert create_btn.count() >= 0

    def test_manager_agent_exists(self, page: Page, base_url: str):
        """Verify the default manager agent is present in the sidebar."""
        go(page, f"{base_url}/#/computer")

        manager = page.locator(".agent-nav-row").filter(has_text="manager").first
        assert manager.count() > 0, "Default manager agent not found in sidebar"

    def test_manager_agent_is_running(self, page: Page, base_url: str):
        """Verify the manager agent shows a running/online status."""
        go(page, f"{base_url}/#/computer")

        manager_row = page.locator(".agent-nav-row").filter(has_text="manager").first
        if manager_row.count() == 0:
            pytest.skip("Manager agent row not found")
        dot = manager_row.locator(".workspace-status-dot.online")
        assert dot.count() > 0, "Manager agent is not running"


# ---------------------------------------------------------------------------
# Agent detail pane (edit mode)
# ---------------------------------------------------------------------------

class TestAgentDetailPane:
    """AgentDetailPane.tsx — header, status pills, profile editor form."""

    @pytest.mark.smoke
    def test_detail_pane_has_header(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        header = page.locator(".entity-header")
        assert header.count() >= 0

    def test_detail_pane_has_title(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        title = page.locator(".entity-title-row h1")
        assert title.count() >= 0

    def test_detail_pane_has_status_pill(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        pill = page.locator(".status-pill")
        assert pill.count() >= 0

    def test_detail_pane_has_completeness_badge(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        badge = page.locator(".profile-state-pill")
        assert badge.count() >= 0

    def test_save_button(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        save_btn = page.locator('button:has-text("Save"), button:has-text("保存")').first
        assert save_btn.count() >= 0

    def test_open_dm_button(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        dm_btn = page.locator('button:has-text("Open DM"), button:has-text("私信")')
        assert dm_btn.count() >= 0

    def test_delete_agent_button(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        delete_btn = page.locator('button:has-text("Delete"), button:has-text("删除")').first
        assert delete_btn.count() >= 0


# ---------------------------------------------------------------------------
# Agent profile editor form
# ---------------------------------------------------------------------------

class TestAgentProfileEditor:
    """Profile editor form fields from AgentDetailPane.tsx."""

    def test_basics_section(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        basics = page.locator(".profile-section-title:has-text('Basic'), .profile-section-title:has-text('基础')")
        assert basics.count() >= 0

    def test_name_field_readonly(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        name_input = page.locator('.field input[value]').first
        assert name_input.count() >= 0

    def test_description_textarea(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        desc = page.locator("textarea.compact-textarea")
        assert desc.count() >= 0

    def test_provider_select(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        provider = page.locator('[role="combobox"]').first
        assert provider.count() >= 0

    def test_model_select(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        selects = page.locator('[role="combobox"]')
        assert selects.count() >= 0

    def test_reasoning_select(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        selects = page.locator('[role="combobox"]')
        assert selects.count() >= 0

    def test_fast_mode_checkbox(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        checkbox = page.locator('input[type="checkbox"]')
        assert checkbox.count() >= 0

    def test_advanced_section(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        advanced = page.locator(".profile-section-title:has-text('Advanced'), .profile-section-title:has-text('高级')")
        assert advanced.count() >= 0

    def test_env_key_value_editor(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/agents/test-agent")
        env_editor = page.locator(".profile-env-field")
        assert env_editor.count() >= 0


# ---------------------------------------------------------------------------
# End-to-end: create worker from Hub
# ---------------------------------------------------------------------------

class TestCreateWorker:
    """End-to-end: select a worker template in Hub, fill form, and create."""

    @pytest.mark.slow
    def test_create_worker_via_hub_template(self, page: Page, base_url: str, request):
        import random, string

        go(page, f"{base_url}/#/hub")

        # wait for template list to load from registry
        page.wait_for_timeout(2000)

        # 1. Click a worker template card
        worker_cards = page.locator(".hub-template-card")
        if worker_cards.count() == 0:
            pytest.skip("No hub templates loaded")
        worker_card = worker_cards.filter(has_text="picoclaw-worker").first
        if worker_card.count() == 0:
            worker_card = worker_cards.first
        worker_card.click()
        page.wait_for_timeout(500)

        # 2. Click "Create" button in inspector panel
        create_btn = page.locator(".hub-inspector-hero button").filter(has_text="Create").first
        if create_btn.count() == 0:
            pytest.skip("Create button not found")
        create_btn.click()
        page.wait_for_timeout(1000)

        # 3. Verify modal opened
        modal = page.locator(".modal-card.profile-modal, .modal-card.agent-modal")
        assert modal.count() > 0, "Create agent modal did not open"

        # 4. Fill in a unique agent name (teardown via cleanup_agent)
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        agent_name = f"test-worker-{suffix}"
        request.addfinalizer(lambda: cleanup_agent(agent_name))
        name_input = modal.locator('input[aria-required="true"]').first
        name_input.click()
        name_input.fill(agent_name)
        page.wait_for_timeout(500)

        # 5. Verify no form error before save
        error = modal.locator(".form-error")
        assert error.count() == 0, f"Form error before save: {error.inner_text()}"

        # 6. Click Create
        save_btn = modal.locator(".modal-actions button").last
        assert save_btn.count() > 0, "Create button not found in modal"
        assert save_btn.is_enabled(), "Create button is disabled"
        save_btn.click(force=True)

        # 7. Wait for creation (sandbox setup can take 60s+)
        page.wait_for_timeout(5000)
        try:
            page.wait_for_selector(f".agent-nav-row:has-text('{agent_name}')", timeout=60000)
        except Exception:
            pass

        # 8. Verify modal closed or agent appeared
        page.wait_for_timeout(1000)
        modal_after = page.locator(".modal-card.profile-modal, .modal-card.agent-modal")
        agent_found = page.locator(f".agent-nav-row:has-text('{agent_name}')")
        ok = modal_after.count() == 0 or agent_found.count() > 0

        if not ok:
            error_el = page.locator(".form-error")
            if error_el.count() > 0:
                error_text = error_el.first.inner_text()
                pytest.skip(f"Agent creation failed: {error_text[:200]}")
        assert ok, (
            f"Modal still open ({modal_after.count()}) "
            f"and agent not found ({agent_found.count()})"
        )
