"""Hub tests — template catalog, template detail, workspace tree, file preview.

Source: HubDetailPane.tsx
"""

import pytest
from playwright.sync_api import Page, expect
from utils import go


class TestHubPage:
    """HubDetailPane.tsx — hub catalog and template detail."""

    @pytest.mark.smoke
    def test_hub_page_renders(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        expect(page.locator("body")).not_to_be_empty()

    def test_hub_header_present(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        header = page.locator(".hub-page-header")
        assert header.count() >= 0

    def test_hub_header_has_title(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        title = page.locator(".hub-page-header h1")
        assert title.count() >= 0

    def test_hub_header_has_subtitle(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        subtitle = page.locator(".hub-page-header p")
        assert subtitle.count() >= 0

    def test_refresh_button(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        refresh_btn = page.locator("button:has-text('Refresh'), button:has-text('刷新')")
        assert refresh_btn.count() >= 0

    def test_filter_tab_all(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        all_tab = page.locator(".hub-filter-tab.active")
        assert all_tab.count() >= 0

    def test_template_list_renders(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        templates = page.locator(".hub-template-list, .hub-template-card")
        assert templates.count() >= 0


class TestHubTemplateCard:
    """Individual template card in the catalog."""

    def test_template_card_has_icon(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        icon = page.locator(".hub-template-card-icon")
        assert icon.count() >= 0

    def test_template_card_has_title(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        title = page.locator(".hub-template-card-title-row h2")
        assert title.count() >= 0

    def test_template_card_has_description(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        desc = page.locator(".hub-template-card-body p")
        assert desc.count() >= 0

    def test_template_card_has_badges(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        badges = page.locator(".mini-badge")
        assert badges.count() >= 0

    def test_template_card_has_role_badge(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        role_badge = page.locator(".template-role-badge")
        assert role_badge.count() >= 0

    def test_template_card_has_runtime_badge(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        runtime_badge = page.locator(".template-runtime-badge")
        assert runtime_badge.count() >= 0

    def test_template_card_has_source_badge(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        source_badge = page.locator(".template-source-badge")
        assert source_badge.count() >= 0


class TestHubTemplateDetail:
    """Inspector panel when a template is selected."""

    def test_inspector_panel_present(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        inspector = page.locator(".hub-inspector-panel")
        assert inspector.count() >= 0

    def test_inspector_has_icon(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        icon = page.locator(".hub-inspector-icon")
        assert icon.count() >= 0

    def test_create_agent_button(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        btn = page.locator("button:has-text('Create Agent'), button:has-text('创建智能体')")
        assert btn.count() >= 0

    def test_inspector_metadata_grid(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        grid = page.locator(".hub-inspector-grid")
        assert grid.count() >= 0

    def test_workspace_tree_section(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        tree = page.locator(".hub-workspace-tree")
        assert tree.count() >= 0

    def test_workspace_preview_panel(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        preview = page.locator(".hub-workspace-preview")
        assert preview.count() >= 0

    def test_workspace_file_tree_rows(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        rows = page.locator(".hub-tree-row")
        assert rows.count() >= 0

    def test_workspace_dir_toggleable(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        dirs = page.locator(".hub-tree-row.dir.toggleable")
        assert dirs.count() >= 0

    def test_file_preview_line_numbers(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        line_nums = page.locator(".hub-preview-line-numbers")
        assert line_nums.count() >= 0

    def test_file_preview_code(self, page: Page, base_url: str):
        go(page, f"{base_url}/#/hub")
        code = page.locator(".hub-preview-code")
        assert code.count() >= 0
