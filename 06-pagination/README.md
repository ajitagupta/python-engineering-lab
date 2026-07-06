# 06 — Pagination

Building on the search/filter API from concept 05, this concept lets callers
fetch workouts in **pages** instead of getting every match at once — with
`limit` and `offset` query parameters, and response **metadata** so the
caller knows how many results exist in total.

## Run it

```powershell
cd 06-pagination
pip install -r requirements.txt
python app.py
```

## Paging through results

`limit` = how many to return; `offset` = how many to skip first.

```powershell
# first page (default limit is 2)
Invoke-RestMethod -Uri "http://127.0.0.1:5000/workouts?limit=2&offset=0"

# next page
Invoke-RestMethod -Uri "http://127.0.0.1:5000/workouts?limit=2&offset=2"

# filtering and paging together
Invoke-RestMethod -Uri "http://127.0.0.1:5000/workouts?sport=run&limit=2"
```

The response is no longer a bare list — it wraps the page in an object with
context:

```json
{
  "workouts": [ ... ],
  "total": 3,
  "limit": 2,
  "offset": 0
}
```

`total` tells the caller how many workouts match in all (3), even though only
`limit` (2) are returned — so they know there's another page.

Defaults: `limit` defaults to 2, `offset` to 0. (2 is deliberately low so
paging is visible on small data; a real API would default higher.)

## Why the total needs a separate query

`search_workouts` is limited by `limit`, so it returns at most one page.
The total count is a *different question* — "how many match in all?" — and
the limited page can't answer it. So `count_workouts` runs a separate
`SELECT COUNT(*)` with the **same filters** but **no LIMIT/OFFSET**:

```python
query = "SELECT COUNT(*) FROM workouts"
if conditions:
    query += " WHERE " + " AND ".join(conditions)
# no LIMIT/OFFSET — count ALL matches, not just a page
count = cur.fetchone()[0]
```

If there were 100 matching workouts and `limit=2`, the page returns 2 but
the count returns 100. You can't derive the total from the page.

## Stable ordering matters

The paged query uses `ORDER BY id` before `LIMIT ? OFFSET ?`:

```sql
SELECT * FROM workouts [WHERE ...] ORDER BY id LIMIT ? OFFSET ?
```

Without an explicit `ORDER BY`, SQL makes **no guarantee** about row order —
so "page 2" wouldn't be stable, and rows could repeat across pages or be
skipped. `ORDER BY id` guarantees insertion order (id is the
auto-incrementing key), which is exactly what makes paging correct and
repeatable. Never rely on implicit row order when order matters.

Clause order is fixed in SQL: `WHERE` → `ORDER BY` → `LIMIT` / `OFFSET`.

## Noticed: duplicated filter logic

`search_workouts` and `count_workouts` build the same filter conditions.
That duplication is a candidate for a shared helper — left as-is here, but
noted as the next natural refactor.

## What I learned

> - What is pagination? Why is it required for large result sets?
> - What do LIMIT and OFFSET each do?
> - Why does the total count need a SEPARATE query — why can't you just
>  count the rows search_workouts returned?
> - Why does pagination need ORDER BY? What breaks without it?
> - Why wrap the response in metadata instead of returning a bare list?

## Concepts touched

Pagination, `LIMIT` / `OFFSET`, query-parameter defaults, response metadata
(wrapping data with context), a separate `COUNT(*)` query for totals, stable
ordering with `ORDER BY`, SQL clause ordering.