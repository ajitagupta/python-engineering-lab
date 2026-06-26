# 01 — REST API

A minimal REST API with two routes: `GET /workouts` returns a list of
workouts, `POST /workouts` accepts a new one and echoes it back. Built with
Flask. No database yet — the data lives in memory and resets when the app
restarts (that's what later concepts fix).

## Run it

From the repo root, with your virtual environment activated:

```powershell
cd 01-rest-api
pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000/workouts> in your browser — you'll see the
list of workouts as JSON. That's the `GET` route working.

## Test the POST route

A browser can only send `GET` requests by typing a URL, so to test
`POST /workouts` you need to send a request from the command line. Leave the
app running in one terminal and open a second one.

On Windows (PowerShell):
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/workouts -Method Post -ContentType "application/json" -Body '{"sport": "swim", "distance_km": 0.4}'
```

On macOS / Linux (curl):
```bash
curl -X POST http://127.0.0.1:5000/workouts \
  -H "Content-Type: application/json" \
  -d '{"sport": "swim", "distance_km": 0.4}'
```

Both send a workout as JSON and should get the same workout echoed back.
The `Content-Type: application/json` header is required — it's what tells
Flask the body is JSON so `request.get_json()` will parse it. Leave it out
and the request body comes back empty.

## What I learned

> I learn how to scaffold a Flask app.
> I was familiar with REST, but I learnt to write out a GET and POST request for a sports tracker API.
> I experimented with lists and later converted them into dictionaries to optimize for the JSON format.
> What's the difference between `request.get_json()` and `jsonify()`?
> What does `if __name__ == "__main__":` actually decide?
> The data-modelling bit: why store numbers as numbers, not "6km"?

## Concepts touched

Flask routes, HTTP methods (GET/POST), request bodies, JSON responses,
basic data modelling.
