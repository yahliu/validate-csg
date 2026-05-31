# csgclaw UI Tests

Automated UI tests for [csgclaw](https://github.com/OpenCSGs/csgclaw) using Python + Playwright.

Tests are driven by real component source code analysis — each file references the actual React components it covers.

## Prerequisites

- Python 3.9+
- `csgclaw serve` running locally
- `csgclaw` CLI on PATH (for E2E test cleanup)

## Install

```bash
pip install -r requirements.txt
playwright install chromium
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CSGCLAW_UI_URL` | `http://127.0.0.1:18080` | csgclaw frontend URL |

## Start the app under test

```bash
csgclaw serve
```

## Run

```bash
# All tests
pytest cases/ -v

# Headless mode (CI)
pytest cases/ --headed=false

# Smoke tests only
pytest cases/ -m smoke

# Skip slow E2E tests
pytest cases/ -m "not slow"

# Single file
pytest cases/test_navigation.py -v

# HTML report
pytest cases/ --html=report.html
```

## Structure

```
ui-tests/
├── config.py                # UI_BASE_URL, timeouts
├── conftest.py              # browser context, base_url fixture
├── pytest.ini               # markers (smoke, slow)
├── requirements.txt
├── utils/
│   ├── __init__.py          # exports: go, cleanup_agent, cleanup_room
│   └── helpers.py           # go() — navigate; cleanup_agent(); cleanup_room()
└── cases/
    ├── test_navigation.py       # 14 tests — all 10 hash routes, switching, reload
    ├── test_workspace.py        # 15 tests — layout, topbar, sidebar, tab bar, settings
    ├── test_agents.py           # 29 tests — agent list, detail pane, profile editor, create worker E2E
    ├── test_conversation.py     # 30 tests — conversation list, header, messages, composer, thread
    ├── test_hub.py              # 24 tests — hub page, template cards, inspector, workspace preview
    ├── test_rooms.py            #  5 tests — create room modal fields, validation, E2E
    └── test_modals.py           #  4 tests — modal backdrop, card, close button
```

## Coverage

| File | Source Components | What's Tested |
|------|------------------|---------------|
| `test_navigation.py` | AppRouter.tsx | All 10 hash routes, inter-route switching, page reload |
| `test_workspace.py` | WorkspaceLayout, WorkspaceTopBar, WorkspaceSidebar, WorkspaceTabBar, SidebarUserButton | Layout shell, topbar logo, sidebar resizer, 3 tabs, settings menu, theme/locale/version |
| `test_agents.py` | AgentList, AgentRow, AgentDetailPane, AgentProfileEditor, AgentProfileModal | Agent list in sidebar, detail pane header, status pills, profile editor form fields, manager agent health, E2E create worker from hub template |
| `test_conversation.py` | ConversationSection, ConversationPane, ThreadPanel, AgentLogsDialog | Conversation list, chat header, member popover, tools menu, message list, composer, thread panel |
| `test_hub.py` | HubDetailPane | Template catalog, cards (icon/title/desc/badges), inspector panel, workspace tree, file preview |
| `test_rooms.py` | CreateRoomModal, WorkspaceTabPanels | Open modal, field validation, create button disable/enable, E2E room creation |
| `test_modals.py` | AgentProfileModal, CreateRoomModal | Modal backdrop, card shell, close button |

## E2E Test Cleanup

E2E tests that create resources (agents, rooms) register a teardown via `request.addfinalizer()`:

```python
request.addfinalizer(lambda: cleanup_agent(agent_name))
request.addfinalizer(lambda: cleanup_room(room_name))
```

Cleanup functions in `utils/helpers.py` call `csgclaw agent delete` / `csgclaw room delete` via CLI. They run after each test regardless of pass/fail.

## Notes

- Tests use `wait_until="commit"` (not `networkidle`) to tolerate backend being unreachable.
- The `go()` helper in `utils/helpers.py` wraps `page.goto` with try/except for robustness.
- E2E create-worker test can take 60s+ due to sandbox setup — skip with `-m "not slow"`.
- Default viewport: 1280x800.
