# 03 — Pytest API Tests

Building on the validated API from concept 02, this concept adds an
automated test suite. Instead of testing the API by hand (typing
`Invoke-RestMethod` commands over and over), the same checks are written
once as pytest tests and run in a fraction of a second, every time.

The tests cover both **failure paths** (bad input is rejected with the
right status code and error message) and **happy paths** (valid input is
accepted and the right data comes back), plus the `404` lookup route.

## Run the tests

From the repo root, with your virtual environment activated:

```powershell
cd 03-pytest-api-tests
pip install -r requirements.txt
pytest -v
```

`pytest` automatically discovers `test_app.py` (any file starting with
`test_`) and runs every function starting with `test_`. The `-v` flag lists
each test by name with PASSED / FAILED.

## What the tests check

| Test | Verifies |
|------|----------|
| missing sport → 400 | required field rejected, error mentions `sport` |
| invalid sport → 400 | business-rule validation ("banana" isn't a sport) |
| missing distance → 400 | conditional rule (run requires distance) |
| negative distance → 400 | value rule (numbers must be >= 0) |
| valid workout → 200 | happy path: valid input accepted, workout echoed back |
| valid rest day → 200 | edge case: rest needs no distance/duration |
| existing id → 200 | lookup returns the right workout |
| missing id → 404 | resource-not-found handled cleanly |

Each failure test asserts the **status code** AND the **error message**, so
it confirms the API failed for the *right reason* — not just that *some*
error occurred.

## The test client and the fixture

Tests call the API through Flask's **test client**, which runs the app
in-process — no server, no network. The client is provided by a pytest
**fixture**:

```python
@pytest.fixture
def client():
    return app.test_client()
```

A test gets the client by naming `client` as a parameter; pytest sees the
matching fixture and passes a fresh client in automatically. Each test gets
its own clean client.

## What I learned

> - How is pytest different from unittest? (plain functions + `assert`,
> no class / no `self`; fixtures instead of setUp.)
> - What does a fixture do, and how does a test get hold of it?
> - Why test the happy path, not just the failures?
> - Why assert the error MESSAGE, not just the status code?
> - The big one: the 404 workout id test failed, and it was the TEST that was wrong, because
> it wasn't testing the API error messages correctly.

## Concepts touched

pytest, the Flask test client, fixtures, dependency injection (a test
declares the `client` it needs; pytest provides it), status-code and
response-body assertions, testing happy paths vs failure paths.
