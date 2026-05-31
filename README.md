# validate-csg

Automated test suites for the [OpenCSG](https://github.com/OpenCSGs) ecosystem.

| Suite | Target | Tech | Cases |
|-------|--------|------|-------|
| [API tests](api-tests/README.md) | [csghub-lite](https://github.com/OpenCSGs/csghub-lite) | pytest + requests | 242 |
| [UI tests](ui-tests/README.md) | [csgclaw](https://github.com/OpenCSGs/csgclaw) | Playwright | 121 |

## Quick Start

```bash
# API tests (requires csghub-lite on localhost:11435)
cd api-tests && pip install -r requirements.txt && pytest test_chat_completions/ -v

# UI tests (requires csgclaw serve on localhost:18080)
cd ui-tests && pip install -r requirements.txt && playwright install chromium && pytest cases/ -v
```

## Design

- **API tests** — Three-tier per endpoint: Normal → Boundary → Exception
- **UI tests** — Component-driven, from actual React source code analysis
- **Shared utils** — Common helpers extracted to avoid duplication

## Claude Skill

`/write-test-case` — parses a test case description, determines API vs UI, reuses existing utils, and writes to the correct directory.
