# 04 — SQLite Persistence

Building on the tested API from concept 03, this concept replaces the
in-memory workouts list with a **SQLite database**, so data survives a
restart and IDs are assigned by the database instead of being faked.

All database code lives in a separate `db.py` module (a **data access
layer**). The Flask routes call functions like `get_all_workouts()` and
`add_workout()` and never touch SQL directly — routes handle HTTP, `db.py`
handles storage.

## Run it

From the repo root, with your virtual environment activated:

```powershell
cd 04-sqlite-persistence
pip install -r requirements.txt
python app.py
```

On startup the app calls `init_db()`, which creates the `workouts` table if
it doesn't already exist. The database lives in a local file, `workouts.db`.

## Try it out

The table starts empty. Add a workout — the response comes back with an
`id` you never sent, because SQLite assigns it automatically:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts -Method Post -ContentType "application/json" -Body '{"sport": "run", "distance_km": 6, "duration_min": 35}'
```

List all workouts, or fetch one by id:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts/1
```

**The key test — persistence:** add a workout, then stop the app (Ctrl+C)
and start it again. The workout is still there, because it lives on disk in
`workouts.db`, not in memory.

## The data access layer (`db.py`)

| Function | Does | SQL |
|----------|------|-----|
| `init_db()` | create the table if absent | `CREATE TABLE IF NOT EXISTS` |
| `get_all_workouts()` | list all workouts | `SELECT * FROM workouts` |
| `get_workout_by_id(id)` | fetch one, or None | `SELECT ... WHERE id = ?` |
| `add_workout(data)` | insert, return with new id | `INSERT INTO ...` |

Two `sqlite3` details worth knowing:

- `con.row_factory = sqlite3.Row` makes rows accessible by column name, so
  they convert cleanly to dicts (`dict(row)`) for JSON responses.
- After an `INSERT`, `cursor.lastrowid` holds the id SQLite just assigned —
  that's how a new workout gets a real id instead of a faked one.

## Parameterized queries (`?`)

Values from a request are always passed with `?` placeholders, never built
into the SQL string:

```python
cur.execute("SELECT * FROM workouts WHERE id = ?", (workout_id,))
```

This keeps user input as **data**, never executable SQL — which is what
prevents SQL injection. Building the query with an f-string
(`f"... id = {workout_id}"`) would let malicious input run as commands.

## What I learned

> - Why `?` placeholders instead of f-strings? (data, not code — the SQL
> injection boundary.)
> - What does a "data access layer" give you? Why keep all SQL in db.py
>  and out of the routes?_
> - Why does INSERT omit the id, and how does the database assign it?
> - Why does commit() matter, and what happens if you forget it?
> - Reuse of db functions from db.py / db module
> - dict(row) to convert a sqlite3.Row to a dict for JSON responses

## Concepts touched

SQLite, the `sqlite3` library (connect / cursor / execute / fetch /
commit), parameterized queries and SQL injection, `row_factory`,
auto-incrementing primary keys, `lastrowid`, the data-access-layer pattern.
