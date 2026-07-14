# Python Engineering Lab

![Python Engineering Lab — engineering concepts assembled one piece at a time](assets/title.png)

A learning-in-public project. I'm a software engineer consolidating my Python
and backend fundamentals by implementing one engineering concept at a time —
from scratch, by hand, understanding rather than copying — and writing down what I
actually learned along the way.

The concepts aren't isolated exercises. Together they build **one API** — a
workout / training tracker — that gets more capable with every step. Concept
01 is a bare REST endpoint; by concept 08 the same API validates input, is
covered by tests, persists to a database, supports search, filtering and
pagination, imports data from CSV files, and runs scheduled background jobs.
Each concept adds a real backend capability to the same growing codebase.

## The project: a workout tracker API

The running example is an API for logging workouts — runs, swims, rides,
badminton, strength sessions, rest days. It's a deliberately small domain,
chosen so the *engineering* stays in focus rather than the business logic. A
few decisions from that domain recur throughout:

- A workout has a `sport`, and optionally a `distance_km` and `duration_min`.
- Different sports need different fields: a run needs both distance and
  duration; strength and badminton need only duration; a rest day needs
  neither. This "conditional validation" shows up in several concepts.
- Absent optional fields are stored as `NULL` / `None`, which forces careful
  handling of missing values throughout the stack.

## How this lab works

- One concept per folder, numbered in order (`01-...`, `02-...`).
- I write the first version myself before looking at any reference solution.
  The point is understanding, not copying.
- Each concept builds on the previous one's code — the API is cumulative.
- Each concept folder has its own README with run instructions, an
  explanation of the pattern, and honest notes on what tripped me up and what
  I deliberately left for later.

## Architecture

A theme that pays off repeatedly: **separation of concerns.** From concept 04
on, all database code lives in a `db.py` data-access layer, and the Flask
routes call those functions rather than touching SQL directly. Routes handle
HTTP; `db.py` handles storage. That split is what lets later concepts — like a
background job that reads the database from outside any request — reuse the
same functions cleanly.

## Getting started

You'll need Python 3.12 or newer.

```powershell
# Clone and enter the repo
git clone https://github.com/ajitagupta/python-engineering-lab.git
cd python-engineering-lab

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
```

Then open the README inside whichever concept folder you want to run — each
lists its own dependencies and how to start it. Later concepts build on
earlier ones, so reading them in order shows the API taking shape.

## Roadmap

Each concept adds one capability to the same workout-tracker API.

| Concept | What it adds to the API | Skill | Status    | Folder |
|---------|------------------------|-------|-----------|--------|
| 01 — REST API | List and create workouts over HTTP | Flask routes, HTTP methods, JSON | ✅ Done    | [01-rest-api](01-rest-api/) |
| 02 — Validation & Error Handling | Reject bad input with clear errors and status codes | Input validation, 400/404, conditional rules | ✅ Done    | [02-validation-error-handling](02-validation-error-handling/) |
| 03 — Pytest API Tests | An automated test suite proving the API works | pytest, test client, fixtures | ✅ Done    | [03-pytest-api-tests](03-pytest-api-tests/) |
| 04 — SQLite Persistence | Store workouts in a database that survives restarts | SQL, a data-access layer, `sqlite3` | ✅ Done    | [04-sqlite-persistence](04-sqlite-persistence/) |
| 05 — Search & Filtering | Filter workouts by sport, distance, duration | Query parameters, dynamic SQL | ✅ Done    | [05-search-filtering](05-search-filtering/) |
| 06 — Pagination | Return results in pages with total-count metadata | `LIMIT`/`OFFSET`, response metadata | ✅ Done    | [06-pagination](06-pagination/) |
| 07 — File Uploads | Bulk-import workouts from a CSV, all-or-nothing | Multipart uploads, CSV parsing | ✅ Done    | [07-file-upload](07-file-upload/) |
| 08 — Background Scheduler | Log a workout summary periodically, on a timer | Scheduled jobs, background threads | ✅ Done    | [08-background-scheduler](08-background-scheduler/) |
| 09 — Caching | Serve repeated reads faster with a cache | Cache strategies, invalidation | ✅ Done      | [09-caching](09-caching/) |
| 10 — Data Parsing & Extraction | Parse structured text into workouts | Parsing, structured text | ⬜ Planned | _coming soon_ |

_Scoped to ten concepts for now; a back half (architecture, performance,
production) may follow once the pace settles._

## Tech

Python 3.12 · Flask · SQLite · pytest · APScheduler — standard library and
small, widely-used dependencies, added only as each concept needs them.

---

_A learning project, updated as I work through it. Progress over speed —_
_one concept genuinely understood beats five rushed._
