# Python Engineering Lab

![Python Engineering Lab — engineering concepts assembled one piece at a time](assets/title.png)

A learning-in-public project. I'm a software engineer consolidating my Python
and backend fundamentals by implementing one engineering concept at a time —
from scratch, by hand, understanding rather than copying — and writing down
what I actually learned along the way.

The concepts aren't isolated exercises. Together they build **one API** — a
workout / training tracker — that grows more capable with every step. Concept
01 is a bare REST endpoint; by concept 10 the same API validates input, is
covered by tests, persists to a database, supports search, filtering and
pagination, imports CSV files, runs scheduled background jobs, caches reads,
and parses free-form text into workouts. Ten concepts, one growing codebase.

## The project: a workout tracker API

The running example logs workouts — runs, swims, rides, badminton, strength
sessions, rest days. A deliberately small domain, chosen so the *engineering*
stays in focus. A few decisions recur throughout:

- A workout has a `sport`, and optionally a `distance_km` and `duration_min`.
- Different sports need different fields: a run needs both distance and
  duration; strength and badminton need only duration; a rest day needs
  neither ("conditional validation").
- Absent optional fields are stored as `NULL` / `None`, which forces careful
  handling of missing values throughout the stack.

## How this lab works

- One concept per folder, numbered in order (`01-...`, `02-...`).
- I write the first version myself before looking at any reference — the
  point is understanding, not copying.
- Each concept builds on the previous one's code; the API is cumulative.
- Each folder has its own README with run instructions and honest notes on
  what tripped me up and what I deliberately left for later.

## Architecture

A theme that pays off repeatedly: **separation of concerns.** From concept 04
on, all database code lives in a `db.py` data-access layer, and the Flask
routes call those functions rather than touching SQL directly. Routes handle
HTTP; `db.py` handles storage. That split is what lets later concepts — like a
background job reading the database from outside any request — reuse the same
functions cleanly.

## Getting started

You'll need Python 3.12 or newer.

```powershell
git clone https://github.com/ajitagupta/python-engineering-lab.git
cd python-engineering-lab
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
```

Then open the README inside whichever concept folder you want to run — each
lists its own dependencies. Reading them in order shows the API take shape.

## Roadmap

Each concept adds one capability to the same workout-tracker API.

| Concept | What it adds | Skill | Folder |
|---------|-------------|-------|--------|
| 01 — REST API | List and create workouts over HTTP | Flask routes, HTTP methods, JSON | [01-rest-api](01-rest-api/) |
| 02 — Validation & Error Handling | Reject bad input with clear errors | Validation, 400/404, conditional rules | [02-validation-error-handling](02-validation-error-handling/) |
| 03 — Pytest API Tests | A test suite proving the API works | pytest, test client, fixtures | [03-pytest-api-tests](03-pytest-api-tests/) |
| 04 — SQLite Persistence | Store workouts in a database | SQL, a data-access layer, `sqlite3` | [04-sqlite-persistence](04-sqlite-persistence/) |
| 05 — Search & Filtering | Filter by sport, distance, duration | Query parameters, dynamic SQL | [05-search-filtering](05-search-filtering/) |
| 06 — Pagination | Return results in pages with metadata | `LIMIT`/`OFFSET`, response metadata | [06-pagination](06-pagination/) |
| 07 — File Uploads | Bulk-import from CSV, all-or-nothing | Multipart uploads, CSV parsing | [07-file-upload](07-file-upload/) |
| 08 — Background Scheduler | Log a summary periodically, on a timer | Scheduled jobs, background threads | [08-background-scheduler](08-background-scheduler/) |
| 09 — Caching | Serve repeated reads from a cache | Cache strategies, invalidation | [09-caching](09-caching/) |
| 10 — Data Parsing & Extraction | Parse free-form text into workouts | Regular expressions, extraction | [10-data-parsing](10-data-parsing/) |

All ten concepts complete. ✅

## Tech

**Python 3.12 · Flask** — the web framework — and **APScheduler** for
background jobs are the only third-party dependencies. Everything else is the
standard library: **SQLite** (`sqlite3`), CSV parsing (`csv`, `io`), and
regular expressions (`re`), plus **pytest** for tests. Dependencies were
added only as each concept needed them.

---

_A finished learning project. Progress over speed — one concept genuinely_
_understood beats five rushed._