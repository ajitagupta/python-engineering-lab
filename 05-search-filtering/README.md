# 05 — Search & Filtering

Building on the persistent API from concept 04, this concept lets callers
**narrow** the results with query parameters instead of always getting every
workout. Filter by sport, minimum distance, minimum duration — or any
combination.

The filters are optional and combine with `AND`. The query is built
**dynamically** based on which filters are present, while still using `?`
placeholders so it stays safe from SQL injection.

## Run it

```powershell
cd 05-search-filtering
pip install -r requirements.txt
python app.py
```

Add a few workouts first (one per request), then try the filters.

## Filtering

Query parameters go after a `?` in the URL:

```powershell
# only runs
Invoke-RestMethod -Uri "http://127.0.0.1:5000/workouts?sport=run"

# workouts of at least 5 km
Invoke-RestMethod -Uri "http://127.0.0.1:5000/workouts?min_distance=5"

# workouts of at least 30 min
Invoke-RestMethod -Uri "http://127.0.0.1:5000/workouts?min_duration=30"

# all three at once
Invoke-RestMethod -Uri "http://127.0.0.1:5000/workouts?sport=run&min_distance=5&min_duration=30"

# no filters -> everything
Invoke-RestMethod -Uri "http://127.0.0.1:5000/workouts"
```

## How the dynamic query works

The route reads each query parameter from `request.args` (converting the
numeric ones to `float`) and passes plain values to `db.search_workouts()`.
That function builds the query from two parallel lists:

```python
conditions = []          # query STRUCTURE: "sport = ?", "distance_km >= ?"
values = []              # the actual VALUES, kept out of the string

if sport is not None:
    conditions.append("sport = ?")
    values.append(sport)
# ... same shape for each filter

query = "SELECT * FROM workouts"
if conditions:
    query += " WHERE " + " AND ".join(conditions)

cur.execute(query, tuple(values))
```

Each new filter is just another `if` block appending a condition and a
value — the `" AND ".join(...)` handles zero, one, or many filters with no
special cases.

**Why it stays injection-safe:** only the *structure* (the `sport = ?`
fragments, with placeholders) is built into the query string. The *values*
never touch the string — they go through the parameter list and the
database binds them as data. Dynamic query building and parameterized
safety are not in conflict.

## A NULL detail worth knowing

A rest day has `duration_min` of `NULL`. Filtering by `?min_duration=30`
correctly excludes it, because in SQL `NULL >= 30` is "unknown", not true —
so NULL values never match a `>=` filter. That's the behaviour you want,
but SQL's NULL comparisons surprise people.

## Deliberately deferred

Query-parameter values are **not** validated for type here — e.g.
`?min_distance=banana` would fail the `float()` conversion and error. This
is a conscious scope choice to keep the concept focused on filtering, not a
finished behaviour. (Concept 02's validation guards the POST body, a
different input channel — it does not cover query params.) Handling this
cleanly with a 400 would be a natural next improvement.

## What I learned

> - What are query parameters, and how do they differ from path params
> - Request body as an input channel
> - Why do query params always arrive as strings, and what did you have
>  to do about it for the numeric filters?
> - The key one: how is a dynamically-built query still injection-safe?
> (structure as string, values kept separate.)
> - Why does the two-lists-then-join pattern scale to any number of
> filters without special cases?

## Concepts touched

Query parameters (`request.args`), optional filters, dynamic query
building, conditional WHERE clauses, keeping parameterized safety with
dynamic SQL, string-to-number conversion of query params, SQL NULL
comparison behaviour, separation of concerns (route reads HTTP, db.py
builds SQL).
