# 07 — File Upload

Building on the API from concept 06, this concept adds a route to upload a
**CSV file** of workouts, rather than posting them one at a time as JSON.

> **Status: part 1 of 2.** The upload and CSV parsing are done. The cleanup
> (strings to numbers, empty strings to None), per-row validation, and
> bulk insertion — including the design decision about what to do when
> some rows are invalid — are the unfinished second half.

## Run it

```powershell
cd 07-file-upload
pip install -r requirements.txt
python app.py
```

## Uploading a CSV

Files are sent as `multipart/form-data`, not JSON. Create a test CSV
(`test_workouts.csv`):

```
sport,distance_km,duration_min
run,6.0,35
swim,0.4,27
badminton,,90
rest,,
cycle,10,30
```

Upload it with `curl.exe` (real curl, not PowerShell's alias):

```powershell
curl.exe -F "file=@test_workouts.csv" http://127.0.0.1:5000/workouts/upload
```

`-F "file=@..."` sends a multipart form field named `file`; the `@` means
"upload the file's contents". The route currently returns the parsed rows
as JSON.

## How it works (so far)

The file arrives through `request.files`, not the JSON body:

```python
file = request.files.get("file")
if file is None:
    return jsonify({"error": "No file provided."}), 400
text = file.read().decode("utf-8")
```

The decoded text is parsed with `csv.DictReader`, which reads the first row
as headers and yields each row as a dict keyed by those headers:

```python
reader = csv.DictReader(io.StringIO(text))
workouts = list(reader)
```

`io.StringIO` wraps the string so DictReader can read it like a file.

## The messy-data problem (to solve in part 2)

The parsed rows expose two issues that part 2 must handle:

- **Every value is a string.** `distance_km` comes in as `"6.0"`, not the
  number `6.0` — CSV has no types. These need converting before they can be
  validated or stored.
- **Empty fields are empty strings, not None.** A rest day's blank
  `distance_km` parses as `""`, but the data model uses `None` (SQL NULL)
  for absent optional fields. `""` is neither a valid number nor a proper
  null, so it must be converted to `None`.

## Still to build (part 2)

- Convert numeric strings to numbers; convert empty strings to `None`.
- Validate each row (reusing the validation rules from concept 02).
- Insert the valid workouts (reusing `add_workout` from concept 04).
- **Design decision:** when some rows are valid and some aren't, does the
  upload reject the whole file, or insert the valid rows and report the
  failures? (To be decided in part 2.)

## What I learned

> - How does a file upload differ from a JSON body as an input channel?
>  (request.files vs request.get_json.)_
> - Why does csv.DictReader need io.StringIO?
> - Why do CSV values arrive as strings, and why are empty fields empty
>  strings rather than None?

## Concepts touched (so far)

Multipart file uploads (`request.files`), reading and decoding an uploaded
file, CSV parsing with `csv.DictReader`, `io.StringIO`, the string-vs-typed
and empty-string-vs-None problems of parsed data.