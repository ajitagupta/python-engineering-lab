# 08 — Background Scheduler

Building on the API from concept 07, this concept adds a **background job**
that runs on a schedule — on its own, without any request. Every 10 seconds
it computes and logs a summary of the workouts in the database.

This is a new *kind* of behaviour. Every earlier concept was
request-driven: code ran because a caller hit an endpoint. A scheduled job
runs periodically in the background, triggered by a timer rather than a
request — the same idea as a cron job, but running inside the app process.

## Run it

```powershell
cd 08-background-scheduler
pip install -r requirements.txt
python app.py
```

Watch the terminal. Every 10 seconds, a line like this appears on its own —
no request needed:

```
[Scheduler] 5 workouts logged, 16.4 km total
```

Add workouts (POST, or CSV upload) and within 10 seconds the next tick
reflects them — the background job reads live data.

## How it works

APScheduler runs a function on an interval, on a background thread:

```python
from apscheduler.schedulers.background import BackgroundScheduler

def scheduled_job():
    count = db.count_workouts(None, None, None)
    workouts = db.search_workouts(None, None, None, 1000000, 0)
    total = sum(w["distance_km"] for w in workouts if w["distance_km"] is not None)
    print(f"[Scheduler] {count} workouts logged, {total} km total")

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, "interval", seconds=10)
scheduler.start()
```

The job calls the `db.py` functions directly. It has **no request context**
(nobody called an endpoint), but that's fine — `db.py` never depended on
Flask or the request object, so a background thread can call it freely. The
clean data-access layer from concept 04 is what makes this work.

The distance sum skips `None` distances (rest, badminton, strength have
none) — the same optional-field handling as elsewhere.

## The debug-reloader gotcha

With `debug=True`, Flask runs the app in **two** processes (a watcher and
the real one), so module-level code runs twice — starting **two**
schedulers, and the job fired twice per interval. The fix is to start the
scheduler only in the real app process:

```python
import os
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job, "interval", seconds=10)
    scheduler.start()
```

`WERKZEUG_RUN_MAIN` is `"true"` only in the process that actually serves.
General lesson: any **startup side effect that should happen once**
(schedulers, connection pools, background threads) is dangerous at module
level under the debug reloader, because the module runs twice.

## Known gaps (deliberately deferred)

- **`search_workouts` can't express "no limit".** To sum over all workouts,
  the job passes a large limit (`1000000`). A cleaner fix would let
  `limit=None` mean unlimited by omitting the `LIMIT` clause, or a dedicated
  `SELECT SUM(distance_km)` aggregate query (letting SQL do the summing
  instead of fetching every row into Python).

## What I learned

> - How is a scheduled job different from a request-driven endpoint?
>   (Timer-triggered, runs itself, no caller — like cron, in-process.)
> - Why did the job fire TWICE at first, and what did the
>   WERKZEUG_RUN_MAIN guard fix? (The debug reloader's two processes.)
> - db.py is used inside the background job of app.py — no request context, no Flask, just the clean data-access layer.

## Concepts touched

Background scheduling (APScheduler), interval jobs, request-driven vs
scheduled execution, background threads, the debug-reloader double-start gotcha (`WERKZEUG_RUN_MAIN`),
reusing the data-access layer from a background thread.