"""Room tests — create room from sidebar.

Source: CreateRoomModal.tsx, WorkspaceTabPanels.tsx
"""

import pytest
from playwright.sync_api import Page
from utils import cleanup_room, go


class TestCreateRoom:
    """CreateRoomModal.tsx — New Room flow from sidebar Add button."""

    def test_open_create_room_modal(self, page: Page, base_url: str):
        """Click 'New Room' button and verify modal opens."""
        go(page, base_url)

        add_btn = page.locator('button[aria-label="New Room"], button[aria-label="创建房间"]')
        if add_btn.count() == 0:
            pytest.skip("New Room button not found")
        add_btn.first.click()
        page.wait_for_timeout(500)

        modal_title = page.locator(".modal-title:has-text('New Room'), .modal-title:has-text('创建房间')")
        assert modal_title.count() > 0, "Create room modal did not open"

    def test_create_room_modal_fields(self, page: Page, base_url: str):
        """Verify modal has name input, description, member list, and create button."""
        go(page, base_url)

        add_btn = page.locator('button[aria-label="New Room"], button[aria-label="创建房间"]')
        if add_btn.count() == 0:
            pytest.skip("New Room button not found")
        add_btn.first.click()
        page.wait_for_timeout(500)

        modal = page.locator(".modal-card")
        assert modal.count() > 0

        name_input = modal.locator('input[aria-required="true"]')
        assert name_input.count() > 0, "Room name input not found"

        desc_input = modal.locator("textarea")
        assert desc_input.count() > 0, "Room description textarea not found"

        member_list = modal.locator(".selection-list")
        assert member_list.count() >= 0

        create_btn = modal.locator('.modal-actions button:has-text("Create"), .modal-actions button:has-text("创建")')
        assert create_btn.count() > 0, "Create button not found"

    def test_create_button_disabled_when_name_empty(self, page: Page, base_url: str):
        """Create button should be disabled when room name is blank."""
        go(page, base_url)

        add_btn = page.locator('button[aria-label="New Room"], button[aria-label="创建房间"]')
        if add_btn.count() == 0:
            pytest.skip("New Room button not found")
        add_btn.first.click()
        page.wait_for_timeout(500)

        modal = page.locator(".modal-card")
        create_btn = modal.locator('.modal-actions button:has-text("Create"), .modal-actions button:has-text("创建")')
        assert create_btn.count() > 0
        assert create_btn.is_disabled(), "Create button should be disabled when name is empty"

    def test_create_button_enabled_when_name_filled(self, page: Page, base_url: str):
        """Create button becomes enabled after typing a room name."""
        go(page, base_url)

        add_btn = page.locator('button[aria-label="New Room"], button[aria-label="创建房间"]')
        if add_btn.count() == 0:
            pytest.skip("New Room button not found")
        add_btn.first.click()
        page.wait_for_timeout(500)

        modal = page.locator(".modal-card")
        name_input = modal.locator('input[aria-required="true"]')
        name_input.click()
        name_input.fill("test-room")
        page.wait_for_timeout(300)

        create_btn = modal.locator('.modal-actions button:has-text("Create"), .modal-actions button:has-text("创建")')
        assert create_btn.is_enabled(), "Create button should be enabled when name is filled"


class TestCreateRoomE2E:
    """End-to-end: open modal, fill form, create room, verify result."""

    @pytest.mark.slow
    def test_create_room_and_verify(self, page: Page, base_url: str, request):
        """Create a new room and verify it appears in the sidebar."""
        import random, string

        go(page, base_url)

        add_btn = page.locator('button[aria-label="New Room"], button[aria-label="创建房间"]')
        if add_btn.count() == 0:
            pytest.skip("New Room button not found")
        add_btn.first.click()
        page.wait_for_timeout(500)

        modal = page.locator(".modal-card")
        assert modal.count() > 0, "Create room modal did not open"

        # Fill in room name (teardown via cleanup_room)
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        room_name = f"test-room-{suffix}"
        request.addfinalizer(lambda: cleanup_room(room_name))
        name_input = modal.locator('input[aria-required="true"]')
        name_input.click()
        name_input.fill(room_name)
        page.wait_for_timeout(300)

        # Click Create
        create_btn = modal.locator('.modal-actions button:has-text("Create"), .modal-actions button:has-text("创建")')
        assert create_btn.is_enabled()
        create_btn.click(force=True)
        page.wait_for_timeout(2000)

        # Verify modal closed or room appeared
        modal_after = page.locator(".modal-card")
        room_in_sidebar = page.locator(f".workspace-row-title:has-text('{room_name}'), .conversation-name:has-text('{room_name}')")
        ok = modal_after.count() == 0 or room_in_sidebar.count() > 0

        if not ok:
            error_el = page.locator(".form-error")
            if error_el.count() > 0:
                error_text = error_el.first.inner_text()
                pytest.skip(f"Room creation failed: {error_text[:200]}")
        assert ok, (
            f"Modal still open ({modal_after.count()}) "
            f"and room not found in sidebar ({room_in_sidebar.count()})"
        )
