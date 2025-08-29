# Student Performance Tracker

A Python + Flask app to add students, assign grades, view details, calculate averages, and simple analytics. Uses SQLite for storage, supports CLI and Web UI.

## Run locally (CLI)
```bash
python -m venv .venv
Windows: .venv\Scripts\activate
macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python cli.py
```

## Run locally (Web)
```bash
python -m venv .venv
Windows: .venv\Scripts\activate
macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Deploy (Heroku-like)
1. Set up a new app.
2. Push this repo.
3. Ensure `Procfile` exists and a Python buildpack is used.
4. Optionally set `FLASK_ENV=production` and provide a persistent storage add-on if needed.

## Files
- `db.py` — SQLite helpers and analytics
- `cli.py` — menu-driven CLI
- `app.py` — Flask web app
- `templates/` — Jinja2 HTML
- `static/style.css` — basic styles
- `requirements.txt`, `Procfile` — deployment
