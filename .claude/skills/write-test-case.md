# Write Test Case

Write a new test case into the correct test directory based on the case description provided by the user.

## Steps

### 1. Analyze the test case description

Read the user's test case description. Determine whether it is an **API test** or **UI test**:

- **API test**: Tests HTTP endpoints, request/response validation, status codes, chat completions, models, providers, conversations, etc. These talk to a REST API (csghub-lite on port 11435).
- **UI test**: Tests browser interactions, page rendering, navigation, modals, form fields, agent sidebar, hub templates, etc. These use Playwright to drive a browser against csgclaw (port 18080).

If ambiguous, ask the user.

### 2. Check existing utils for reusable functions

**For API tests**, check `api-tests/utils/`:
- `client.py` — `APIClient` class with `get()`, `post()`, `put()`, `patch()`, `delete()`
- `helpers.py` — `assert_status()`, `random_string()`, `cleanup_key()`, `cleanup_provider()`, `cleanup_conversation()`

**For UI tests**, check `ui-tests/utils/`:
- `helpers.py` — `go(page, url, timeout)` for navigation with server-down tolerance

Reuse these directly — don't duplicate utility code.

### 3. Determine the target directory and naming

- **API test**: Write to `api-tests/test_chat_completions/test_<name>.py`
- **UI test**: Write to `ui-tests/cases/test_<name>.py`

### 4. Write the test file

- Follow the existing patterns in the test directory (class structure, method naming, assertion style).
- Use the shared utilities from `utils/`.
- Add a docstring at the top referencing the source component or endpoint.
- Use pytest markers (`@pytest.mark.smoke`, `@pytest.mark.slow`) where appropriate.
- For API tests: group into Normal → Boundary → Exception classes.
- For UI tests: group by component/feature in class-based organization.
- Use `assert` for UI tests, `assert_status()` helper for API tests.

### 5. Validate

After writing, run the new test to verify it compiles and passes (or skips cleanly if preconditions not met).
