# FinLiteracy (Railway Ready)

This app is configured for deployment on Railway using Gunicorn.

## Railway Setup

1. Create a new Railway project and connect this repository.
2. Add a PostgreSQL service in Railway.
3. In your web service variables, set:
   - `SECRET_KEY` = a long random secret
   - `SESSION_COOKIE_SECURE` = `true`
   - `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` (optional)
   - `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` (optional)
   - `GROQ_API_KEY` (optional)

`DATABASE_URL` is automatically injected by Railway when PostgreSQL is linked.

## Deploy Behavior

- Build: installs from `requirements.txt`
- Start: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120`
- Config file: `railway.json`

## Local Run

```bash
pip install -r requirements.txt
python app.py
```

For local dev, keep `SESSION_COOKIE_SECURE=false` in `.env`.
