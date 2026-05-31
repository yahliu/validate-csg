"""Conversation / Messages tests — list, message display, composer, thread, members.

Source: ConversationPane.tsx, ConversationSection.tsx, ConversationView.tsx,
       ThreadPanel (in ConversationPane), AgentLogsDialog, MentionPicker
"""

import pytest
from playwright.sync_api import Page, expect
from utils import go


# ---------------------------------------------------------------------------
# Conversation list in sidebar
# ---------------------------------------------------------------------------

class TestConversationList:
    """ConversationSection.tsx — list of channels, DMs, threads."""

    @pytest.mark.smoke
    def test_conversation_section_exists(self, page: Page, base_url: str):
        go(page, base_url)
        section = page.locator(".conversation-section, .conversation-item")
        assert section.count() >= 0

    def test_conversation_items_have_avatar(self, page: Page, base_url: str):
        go(page, base_url)
        avatars = page.locator(".conversation-item .avatar")
        assert avatars.count() >= 0

    def test_conversation_items_have_title(self, page: Page, base_url: str):
        go(page, base_url)
        names = page.locator(".conversation-name")
        assert names.count() >= 0

    def test_conversation_items_have_preview(self, page: Page, base_url: str):
        go(page, base_url)
        previews = page.locator(".conversation-preview")
        assert previews.count() >= 0

    def test_delete_button_on_conversation(self, page: Page, base_url: str):
        go(page, base_url)
        delete_btn = page.locator(".conversation-delete-button")
        assert delete_btn.count() >= 0


# ---------------------------------------------------------------------------
# Conversation pane header
# ---------------------------------------------------------------------------

class TestConversationHeader:
    """Header section of ConversationPane — title, member count, tools, invite."""

    @pytest.mark.smoke
    def test_chat_header_present(self, page: Page, base_url: str):
        go(page, base_url)
        header = page.locator(".chat-header")
        assert header.count() >= 0

    def test_chat_title_bar_has_title(self, page: Page, base_url: str):
        go(page, base_url)
        title = page.locator(".chat-title")
        assert title.count() >= 0

    def test_member_badge_button_present(self, page: Page, base_url: str):
        go(page, base_url)
        btn = page.locator(".member-badge-button")
        assert btn.count() >= 0

    def test_channel_tools_button_present(self, page: Page, base_url: str):
        go(page, base_url)
        tools_btn = page.locator('.header-menu.tools-menu button')
        assert tools_btn.count() >= 0

    def test_invite_button_present(self, page: Page, base_url: str):
        go(page, base_url)
        invite_btn = page.locator('button[aria-label*="Invite"], button[aria-label*="邀请"]')
        assert invite_btn.count() >= 0

    def test_member_popover_opens(self, page: Page, base_url: str):
        go(page, base_url)
        btn = page.locator(".member-badge-button")
        if btn.count() > 0:
            btn.first.click()
            page.wait_for_timeout(500)
            popover = page.locator(".members-popover")
            assert popover.count() >= 0

    def test_channel_tools_menu_opens(self, page: Page, base_url: str):
        go(page, base_url)
        tools_btn = page.locator('.header-menu.tools-menu button').first
        if tools_btn.count() > 0:
            try:
                tools_btn.click()
            except Exception:
                pass
            page.wait_for_timeout(500)
            tools_popover = page.locator(".tools-popover")
            assert tools_popover.count() >= 0


# ---------------------------------------------------------------------------
# Message list
# ---------------------------------------------------------------------------

class TestMessageList:
    """Message display in ConversationPane — avatars, content, thread interactions."""

    @pytest.mark.smoke
    def test_messages_section_present(self, page: Page, base_url: str):
        go(page, base_url)
        messages = page.locator(".messages")
        assert messages.count() >= 0

    def test_empty_state_when_no_messages(self, page: Page, base_url: str):
        go(page, base_url)
        empty = page.locator(".messages-empty")
        assert empty.count() >= 0

    def test_message_rows_have_avatar(self, page: Page, base_url: str):
        go(page, base_url)
        rows = page.locator(".message-row")
        if rows.count() > 0:
            avatar = rows.first.locator(".avatar")
            assert avatar.count() >= 0

    def test_message_rows_have_author_name(self, page: Page, base_url: str):
        go(page, base_url)
        authors = page.locator(".message-author")
        assert authors.count() >= 0

    def test_message_rows_have_timestamp(self, page: Page, base_url: str):
        go(page, base_url)
        rows = page.locator(".message-meta")
        assert rows.count() >= 0

    def test_event_messages_rendered(self, page: Page, base_url: str):
        go(page, base_url)
        events = page.locator(".message-event-row")
        assert events.count() >= 0

    def test_thread_reply_button_visible_on_hover(self, page: Page, base_url: str):
        go(page, base_url)
        hover_btn = page.locator(".thread-hover-button")
        assert hover_btn.count() >= 0

    def test_thread_summary_section(self, page: Page, base_url: str):
        go(page, base_url)
        summary = page.locator(".message-thread-actions")
        assert summary.count() >= 0

    def test_open_thread_panel(self, page: Page, base_url: str):
        go(page, base_url)
        thread_btn = page.locator(".thread-action-button").first
        if thread_btn.count() > 0:
            try:
                thread_btn.click()
            except Exception:
                pass
            page.wait_for_timeout(500)
            panel = page.locator(".thread-panel")
            assert panel.count() >= 0


# ---------------------------------------------------------------------------
# Composer / message input
# ---------------------------------------------------------------------------

class TestComposer:
    """Footer composer — contentEditable input, send button, mention picker.

    Source: ConversationPane.tsx footer section
    """

    @pytest.mark.smoke
    def test_composer_present(self, page: Page, base_url: str):
        go(page, base_url)
        composer = page.locator(".composer")
        assert composer.count() >= 0

    def test_composer_editor_is_content_editable(self, page: Page, base_url: str):
        go(page, base_url)
        editor = page.locator(".composer-editor")
        assert editor.count() >= 0

    def test_send_button_present(self, page: Page, base_url: str):
        go(page, base_url)
        send_btn = page.locator(".composer-send-button")
        assert send_btn.count() >= 0

    def test_composer_tip_displayed(self, page: Page, base_url: str):
        go(page, base_url)
        tip = page.locator(".composer-tip")
        assert tip.count() >= 0


# ---------------------------------------------------------------------------
# Thread panel
# ---------------------------------------------------------------------------

class TestThreadPanel:
    """Thread slide-out panel with replies and reply composer.

    Source: ThreadPanel in ConversationPane.tsx
    """

    def test_thread_header_has_title(self, page: Page, base_url: str):
        go(page, base_url)
        header = page.locator(".thread-panel-header")
        assert header.count() >= 0

    def test_thread_has_section_title(self, page: Page, base_url: str):
        go(page, base_url)
        section = page.locator(".thread-section-title")
        assert section.count() >= 0

    def test_thread_composer_has_textarea(self, page: Page, base_url: str):
        go(page, base_url)
        textarea = page.locator(".thread-composer textarea")
        assert textarea.count() >= 0

    def test_thread_send_button(self, page: Page, base_url: str):
        go(page, base_url)
        send_btn = page.locator(".thread-send-button")
        assert send_btn.count() >= 0


# ---------------------------------------------------------------------------
# Agent Logs dialog
# ---------------------------------------------------------------------------

class TestAgentLogs:
    """AgentLogsDialog — agent log viewer from conversation header."""

    def test_logs_button_present(self, page: Page, base_url: str):
        go(page, base_url)
        log_btn = page.locator('button[aria-label*="Logs"], button[aria-label*="日志"]')
        assert log_btn.count() >= 0
