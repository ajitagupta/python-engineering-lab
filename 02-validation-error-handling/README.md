# 02 — Validation & Error Handling

Building on the REST API from concept 01, this concept makes the API
**robust**: instead of trusting whatever the caller sends, it validates
input and responds with clear error messages and correct HTTP status codes.
No new functionality — the same API, hardened.

The `POST /workouts` route now rejects bad input with `400 Bad Request`,
and a new `GET /workouts/<id>` route returns `404 Not Found` when a workout
doesn't exist.

## Run it

From the repo root, with your virtual environment activated:

```powershell
cd 02-validation-error-handling
pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000/workouts> in your browser to see the list.

## Validation rules

A workout is validated by **tier**, because different sports need different
fields:

| Sport | duration_min | distance_km |
|-------|--------------|-------------|
| rest | optional | optional |
| strength, badminton | required | optional |
| run, swim, cycle | required | required |

Universal rules (all sports): `sport` must be present, non-empty, and one of
`swim, run, badminton, cycle, strength, rest`. Any `distance_km` or
`duration_min` that is present must be a number `>= 0`.

## Test the validation

A browser only sends `GET`, so test `POST` from a second terminal while the
app runs. Each of these should return a `400` with a clear error message:

```powershell
# missing/invalid sport
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts -Method Post -ContentType "application/json" -Body '{"sport": "banana"}'

# run missing required distance
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts -Method Post -ContentType "application/json" -Body '{"sport": "run", "duration_min": 30}'

# negative number
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts -Method Post -ContentType "application/json" -Body '{"sport": "run", "distance_km": -5, "duration_min": 30}'
```

A valid workout should be echoed back (no error):

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts -Method Post -ContentType "application/json" -Body '{"sport": "run", "distance_km": 6, "duration_min": 35}'
```

A rest day is valid with no distance or duration:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts -Method Post -ContentType "application/json" -Body '{"sport": "rest"}'
```

## Test the 404

Look up a workout by id. An existing id returns the workout; a missing one
returns `404`:

```powershell
# exists -> returns the workout
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts/1

# does not exist -> 404 Not Found
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts/9999
```

## What I learned

> I learned a lot about validation and error handling in this concept. Some of the key takeaways include:
> - An optional field needs an `is not None` guard BEFORE checking its value?
> - type validation (is it a number?) and business rule validation (is "banana" a real sport?).
> - why 400 (caller sent bad input) vs 404 (resource not found) vs 500 (the server broke)
> - conditional validation: the required fields and the values depend on the sport.
> - the difference between data.get("sport") and data["sport"] — the former returns None if the key is missing, the latter raises KeyError.

## Concepts touched

Input validation, HTTP status codes (400/404), guarded checks on optional
fields, type vs. business-rule validation, conditional validation, path
parameters (`<int:workout_id>`), resource-not-found handling.
