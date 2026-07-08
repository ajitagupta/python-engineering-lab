# 07 — File Upload

Building on the API from concept 06, this concept adds a route to upload a
**CSV file** of workouts and bulk-insert them, rather than posting one at a
time as JSON.

The upload is **all-or-nothing**: every row is cleaned and validated first,
and only if *all* rows are valid does *any* get inserted. One bad row rejects
the whole file, so the database is never left half-imported.

## Run it

```powershell
cd 07-file-upload
pip install -r requirements.txt
python app.py
```

## Uploading a CSV

Files are sent as `multipart/form-data`. Create a test CSV
(`test_workouts.csv`):

```
sport,distance_km,duration_min
run,6.0,35
swim,0.4,27
badminton,,90
rest,,
cycle,10,30
```

Upload it with real curl (not PowerShell's alias):

```powershell
curl.exe -F "file=@test_workouts.csv" http://127.0.0.1:5000/workouts/upload
```

- All rows valid -> `201` with `{"inserted": 5}`, and the workouts persist.
- Any row invalid -> `400` with a list of errors (by row number), and
  **nothing** is inserted.


### Failure cases (rejected uploads)

**Invalid sport.** A CSV with a sport not in the allowed list:

```
sport,distance_km,duration_min
banana,5,30
```

```powershell
curl.exe -F "file=@bad_sport.csv" http://127.0.0.1:5000/workouts/upload
```

Returns `400` with:
```json
{ "errors": ["Row 1: The key sport is invalid. Must be swim, run, badminton, cycle, strength, or rest."] }
```

**All-or-nothing: one bad row among good ones.** A CSV where most rows are
valid but one is not (here a `run` missing its required distance and
duration):

```
sport,distance_km,duration_min
run,6.0,35
swim,0.4,27
run,,
cycle,10,30
```

```powershell
curl.exe -F "file=@mixed.csv" http://127.0.0.1:5000/workouts/upload
```

Returns `400` naming the bad row, and **inserts nothing** — not even the
three valid rows. Confirm with `GET /workouts`: the count is unchanged. This
is the all-or-nothing guarantee: one bad row rejects the whole file.


## The pipeline

Upload -> parse -> clean -> validate -> (all-or-nothing) -> insert.

**Parse.** The file comes through `request.files`, is decoded to text, and
parsed with `csv.DictReader` (via `io.StringIO`) into a list of dicts keyed
by the CSV headers.

**Clean.** CSV gives everything as strings, and blank fields as empty
strings. `clean_row` converts numeric strings to numbers and empty strings
to `None` (matching the data model, where absent optional fields are NULL):

```python
"distance_km": float(distance_km) if distance_km else None
```

**Validate.** `validate_data` checks each cleaned row against the same rules
as the POST route (valid sport, tier requirements, numbers not negative) and
returns an error string or `None`.

**All-or-nothing insert.** Two phases: first loop cleans and validates every
row, collecting errors; only if there are zero errors does the second loop
insert. This is why validation must finish for *all* rows before *any*
insert — otherwise a bad row 4 would leave rows 1-3 already in the database.

## Known gaps (deliberately deferred)

- **Duplicated validation.** `validate_data` duplicates the validation logic
  from concept 02's POST route. They are kept in sync by hand for now; a
  future refactor should extract one shared `validate_workout` called by both
  paths.
- **Non-numeric values crash cleaning.** A CSV value like `distance_km=abc`
  makes `float("abc")` raise during `clean_row`, before validation — a 500
  instead of a clean per-row error. Wrapping the conversion to report it as a
  validation failure would fix this.
- **No transaction.** If an insert failed partway through phase two, earlier
  rows would already be committed. A database transaction (concept 08
  territory) would make the insert truly atomic.
- **No file-size / type limits.** Production uploads should cap size and
  check the file is actually a CSV.

## What I learned

> - How does a file upload differ from a JSON body as an input channel?
>  (request.files vs request.get_json.)_
> - Why does csv.DictReader need io.StringIO?
> - Why do CSV values arrive as strings, and why are empty fields empty
>  strings rather than None?
> - Why does all-or-nothing require validating ALL rows before inserting ANY?
> - How did earlier concepts (add_workout, the validation rules) get reused here?
> - What is refactoring and why is it important to avoid duplicated validation logic?

## Concepts touched

Multipart file uploads (`request.files`), CSV parsing (`csv.DictReader`,
`io.StringIO`), cleaning messy data (strings to numbers, empty to None),
per-row validation, all-or-nothing bulk insert, `enumerate` for row-numbered
errors, reusing earlier building blocks (`add_workout`, validation rules).