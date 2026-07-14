# 09 — Caching

Building on the API from concept 08, this concept adds a **cache**: repeated
reads of `GET /workouts` are served from a stored copy instead of hitting the
database every time — and the cache is **invalidated** (cleared) whenever the
data changes, so it never serves stale results.

The cache is hand-rolled (a small `cache.py` module), not a library — because
the point is to understand caching, and the interesting, hard part is
invalidation.

## Run it

```powershell
cd 09-caching
pip install -r requirements.txt
python app.py
```

Call `GET /workouts` twice and watch the `X-Cache` response header:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/workouts   # X-Cache: MISS (computed)
Invoke-WebRequest -Uri http://127.0.0.1:5000/workouts   # X-Cache: HIT  (from cache)
```

POST a new workout, then read again — the header is `MISS` again, because the
write cleared the cache and the read had to recompute.

## How it works

**The cache** (`cache.py`) is a dict keyed by endpoint + sorted query params,
so each unique request (`?sport=run`, `?limit=2`, ...) caches separately:

```python
def make_key(endpoint, params):
    parts = [f"{k}={params[k]}" for k in sorted(params)]
    return endpoint + "|" + "&".join(parts)
```

**Reads** check the cache first: a hit returns the stored copy (no database);
a miss computes the result, stores it, and returns it. An `X-Cache` header
(`HIT`/`MISS`) makes the behaviour observable from outside.

**Writes invalidate.** After any POST or CSV upload, `cache.clear()` runs —
because the write changed the database, so every cached result is now
potentially stale.

## The key idea: why clearing the cache loses nothing

The **database** is the real, growing data. The **cache** is just a
disposable copy of a past read. When a write happens, the database grows, but
the cached copy is now out of date — *stale*. Clearing the cache doesn't
delete data; it throws away the outdated copy so the next read is forced back
to the database for fresh, complete results, and caches that. Growth happens
in the database; the cache is only ever a temporary echo.

## Invalidation: the hard part
 
Caching *reads* is easy — store a result, hand it back next time. The
difficulty is knowing **when a stored result is no longer true** and must be
discarded. Get it wrong in one direction (invalidate too rarely) and you
serve stale data — a user adds a workout and doesn't see it.
 
**When does a cached read go stale?** Only when the underlying data changes.
In this API, that's any *write*: `create_workout` (`POST /workouts`) and
`upload_workout` (`POST /workouts/upload`, the CSV bulk insert). Reads
(`GET`) never change data, so they never invalidate. So the rule is simple to
state: **invalidate on every write, never on a read.** Both write routes —
`create_workout` and `upload_workout` — call `cache.clear()`; the read routes
(`get_workouts`, `get_workout_by_id`) never do. Miss a single write path and
that path silently starts serving stale data — which is why the invalidation
*tests* matter: they fail if a `cache.clear()` ever goes missing.
 
**How much to invalidate?** Here's where it gets genuinely hard. This cache
stores many entries — one per unique query (`?sport=run`, `?limit=2&offset=0`,
the unfiltered list, ...). When a single new `run` is added, *which* of those
cached entries are now stale?
 
- The unfiltered list — stale (missing the new workout).
- The `?sport=run` list — stale.
- The `?sport=swim` list — *not* stale (a new run doesn't affect it).
- Various paginated slices — some shift, some don't.
Working out exactly which entries a given write invalidates is difficult and
error-prone. So this lab takes the **simple, safe** route: on any write,
`cache.clear()` empties **everything**. Nothing stale can survive, because
nothing survives at all. The cost is efficiency — cached entries that were
still valid get thrown away too, so the next reads all recompute. The benefit
is correctness with almost no code, and zero risk of a subtle
"which-entries-are-stale" bug.


## Testing the cache

Three tests (`test_app.py`), with an `autouse` fixture that clears the cache
before each test for isolation (the cache is module-level shared state):

- **Cache hit:** two reads in a row — the second has `X-Cache: HIT`.
- **Invalidation (header):** read, POST, read — the second read is `MISS`,
  proving the POST cleared the cache.
- **Invalidation (content):** read the total, POST, read again — the total
  went up by one, proving fresh data is served, not a stale copy.

The invalidation tests are the important ones: they would fail if someone
removed `cache.clear()` from a write route — catching the exact bug of
serving stale data.

## Known gaps (deliberately deferred)

- **`clear()` wipes the whole cache** on any write, rather than invalidating
  only the affected entries. This is the simple, safe choice — selective
  invalidation (working out *which* cached queries a new workout makes stale)
  is genuinely hard. Deliberate tradeoff: simplicity over cache efficiency.
- **Tests write to the real `workouts.db`,** so it grows on each run. A real
  suite would use a separate test database, reset between runs.
- **No expiry / TTL.** Entries live until a write clears them; there's no
  time-based expiry, which a production cache would usually add.

## What I learned

> - What is a cache, really? (A disposable copy of a computed result — NOT
>   the data itself, which lives in the database.)_
> - Why must the cache be cleared after a write, and why does clearing it
>   lose no data?_
> - Why is invalidation the hard part of caching?
> - What are HIT and MISS response headers, and how do they make caching observable from outside?
> - How to use fixtures to isolate tests that share state (the cache).

## Concepts touched

Caching, cache keys (per-parameter), cache hit/miss, the `X-Cache` header,
cache invalidation on writes, why the database is the source of truth and the
cache is disposable, test isolation for shared state (`autouse` fixture),
the simplicity-vs-efficiency tradeoff of clear-everything invalidation.