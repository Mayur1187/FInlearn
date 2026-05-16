"""
FinLiteracy – Application Configuration
Contains: Flask config, OAuth config, investment asset catalog.

─── OAuth Setup ────────────────────────────────────────────────────────────────
Set these environment variables before running the app:

  Google OAuth (https://console.cloud.google.com/):
    GOOGLE_CLIENT_ID      = "your-google-client-id.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET  = "your-google-client-secret"
    → Authorised redirect URI: http://localhost:5000/auth/google/callback

  GitHub OAuth (https://github.com/settings/developers):
    GITHUB_CLIENT_ID      = "your-github-client-id"
    GITHUB_CLIENT_SECRET  = "your-github-client-secret"
    → Authorization callback URL: http://localhost:5000/auth/github/callback

  AI Mentor:
    GROQ_API_KEY          = "your-groq-api-key"
────────────────────────────────────────────────────────────────────────────────
"""

import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hackathon-dev-secret-2025')

    # Railway provides DATABASE_URL for managed Postgres.
    _database_url = os.environ.get('DATABASE_URL')
    if _database_url and _database_url.startswith('postgres://'):
        _database_url = _database_url.replace('postgres://', 'postgresql://', 1)
    _sqlite_path = (
        os.path.join(tempfile.gettempdir(), 'finance_app.db')
        if os.environ.get('VERCEL')
        else os.path.join(basedir, 'finance_app.db')
    )
    SQLALCHEMY_DATABASE_URI = _database_url or ('sqlite:///' + _sqlite_path)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Google OAuth ──────────────────────────────────────────
    GOOGLE_CLIENT_ID     = os.environ.get('GOOGLE_CLIENT_ID',     '')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')

    # ── GitHub OAuth ──────────────────────────────────────────
    GITHUB_CLIENT_ID     = os.environ.get('GITHUB_CLIENT_ID',     '')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', '')

    # ── AI Mentor (Groq) ────────────────
    GROQ_API_KEY     = os.environ.get('GROQ_API_KEY', '')


# ─── Investment Assets Catalog ────────────────────────────────────────────────

INVESTMENT_ASSETS = {
    'fd': {
        'name': 'Fixed Deposit',
        'icon': '🏦',
        'color': '#00c875',
        'min_return': 5.5,
        'max_return': 7.5,
        'risk': 'Very Low',
        'description': 'Guaranteed returns, capital protected',
    },
    'stocks': {
        'name': 'Direct Stocks',
        'icon': '📈',
        'color': '#ff7e2d',
        'min_return': -15.0,
        'max_return': 35.0,
        'risk': 'High',
        'description': 'High volatility, high potential reward',
    },
    'mutual_funds': {
        'name': 'Mutual Funds',
        'icon': '🌐',
        'color': '#0cbaba',
        'min_return': 8.0,
        'max_return': 18.0,
        'risk': 'Medium',
        'description': 'Professionally managed, diversified',
    },
    'crypto': {
        'name': 'Cryptocurrency',
        'icon': '🪙',
        'color': '#f7931a',
        'min_return': -40.0,
        'max_return': 80.0,
        'risk': 'Very High',
        'description': 'Extremely volatile, speculative asset',
    },
}
