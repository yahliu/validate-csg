# csghub-lite API Tests

Automated API tests for [csghub-lite](https://github.com/OpenCSGs/csghub-lite) using Python + pytest + requests.


## Prerequisites

- Python 3.9+
- A running csghub-lite instance (local or remote)

## Install

```bash
pip install -r requirements.txt
```

## Configuration

Set environment variables to configure the test target:

| Variable | Default | Description |
|----------|---------|-------------|
| `CSGHUB_BASE_URL` | `http://localhost:11435` | csghub-lite server URL |
| `CSGHUB_API_KEY` | (empty) | API key if auth is enabled |

## Run

```bash
# Run all tests
pytest

# Skip tests that require a loaded model
pytest -m "not model_required"

# Skip slow tests
pytest -m "not slow"

# Run a single file
pytest test_chat_completions/test_health.py -v

# Run only the chat endpoint tests
pytest test_chat_completions/test_chat.py -v

# Generate HTML report
pytest --html=report.html

# Run in parallel
pytest -n auto
```

## Test Design

Each test file follows a three-tier pattern:

- **Normal** — happy-path requests with valid inputs
- **Boundary** — edge values: empty inputs, very long strings, special chars (Unicode, null bytes, XSS, SQL injection, path traversal), parameter out-of-range, etc.
- **Exception** — error handling: invalid JSON, wrong HTTP method, missing required fields, wrong field types, oversized payloads, deep nesting, duplicate keys

## Utilities

`utils/` provides shared helpers used across test files:

| Module | What it provides |
|--------|-----------------|
| `utils.client` | `APIClient` — session-based HTTP wrapper with auth, JSON defaults, timeout |
| `utils.helpers` | `assert_status()` — flexible status code assertion; `random_string()` — test data generation; `cleanup_key/cleanup_provider/cleanup_conversation()` — best-effort teardown |


## Endpoint Coverage

| Area | Endpoints | Notes |
|------|-----------|-------|
| Health | `GET /api/health` | Liveness check |
| System | `GET /api/system` | System status |
| Models | `GET /api/tags`, `/api/pipeline-tags`, `/api/models/search`, `/api/ps`, `/api/marketplace/models` | Listing, search, running models |
| Model Actions | `POST /api/show`, `POST /api/pull`, `DELETE /api/delete` | Model detail, download, deletion — normal, boundary & exception |
| Generation Options | `temperature`, `top_p`, `top_k`, `max_tokens`, `seed`, `num_ctx`, `num_parallel`, `cache_type_k`, `cache_type_v`, `dtype` | All 10 common options — normal, boundary & exception per option |
| Chat | `POST /api/chat` | Chat completion — normal, boundary & exception |
| Generate | `POST /api/generate` | Text generation — normal, boundary & exception |
| Load / Stop | `POST /api/load`, `POST /api/stop` | Model lifecycle — normal, boundary & exception |
| Settings | `GET /api/settings`, `PATCH /api/settings`, `GET /api/settings/directories` | Config & directory browsing |
| API Keys | `GET /api/api-keys`, `POST /api/api-keys`, `DELETE /api/api-keys/{id}`, `GET /api/api-keys/settings`, `GET /api/api-usage` | Key management & usage stats |
| Providers | `GET /api/providers`, `POST /api/providers`, `DELETE /api/providers/{id}`, `POST /api/providers/validate` | Third-party provider CRUD |
| Conversations | `GET/POST /api/conversations`, `GET/PATCH/DELETE /api/conversations/{id}` | Full CRUD |
| Datasets | `GET /api/datasets`, `/api/datasets/search` | Listing, search |
| AI Apps | `GET /api/apps`, `/api/image-runtime`, `/api/images/jobs` | App listing, runtime, jobs |
| Compatibility | `GET /v1/models`, `POST /v1/chat/completions`, `POST /v1/embeddings`, `POST /v1/messages`, `POST /v1/messages/count_tokens` | OpenAI & Anthropic compatible |
