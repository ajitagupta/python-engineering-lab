# Python Engineering Lab

![Python Engineering Lab — engineering concepts assembled one piece at a time](assets/title.png)

A learning-in-public project. I'm a software engineer consolidating my
Python and software-engineering fundamentals by implementing one
engineering concept at a time — from scratch, by hand — and writing down
what I actually learned.

This repo is aimed at **fellow beginners**. Each concept is small, runnable,
and explained in plain language. If you're learning Python and want to
follow along, you can run every concept yourself and read what tripped me up.

## How this lab works

- One concept per folder, numbered in order (`01-...`, `02-...`).
- I write the first version myself before looking at any reference solution.
  The point is understanding, not copying.
- Each concept is small enough to read in one sitting.
- The notes below each concept are honest — including what confused me.

## How to run a concept

You'll need Python 3.12 or newer. These instructions are for Windows
PowerShell (swap the activate line on macOS/Linux).

```powershell
# 1. Clone the repo and enter it
git clone <your-repo-url>
cd python-engineering-lab

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate

# 3. Install the concept's dependencies and run it
cd 01-rest-api
pip install -r requirements.txt
python app.py
```

Each concept folder has its own `requirements.txt` listing exactly what it
needs, so you only install what that concept uses.

---

## Concepts

### Month 1 — Core Backend

#### 01 — REST API

A minimal REST API with two routes: `GET /workouts` returns a list of
workouts, `POST /workouts` accepts a new one and echoes it back. Built with
Flask. No database yet — the data lives in memory and resets when the app
restarts (that's what later concepts fix).

**Run it:**
```powershell
cd 01-rest-api
pip install -r requirements.txt
python app.py
# then open http://127.0.0.1:5000/workouts in your browser
```

**What I learned:**

> I learn how to scaffold a Flask app.
> I was familiar with REST, but I learnt to write out a GET and POST request for a sports tracker API.
> I experimented with lists and later converted them into dictionaries to optimize for the JSON format.
> What's the difference between `request.get_json()` and `jsonify()`?
> What does `if __name__ == "__main__":` actually decide?
> The data-modelling bit: why store numbers as numbers, not "6km"?

**Concepts touched:** Flask routes, HTTP methods (GET/POST), request bodies,
JSON responses, basic data modelling.


