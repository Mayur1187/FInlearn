"""
FinLiteracy – OAuth Routes  (Feature 1)
Handles Google and GitHub OAuth 2.0 login/registration.

Setup:
  1. pip install authlib requests
  2. Add to .env:
       GOOGLE_CLIENT_ID=...
       GOOGLE_CLIENT_SECRET=...
       GITHUB_CLIENT_ID=...
       GITHUB_CLIENT_SECRET=...
  3. Register redirect URIs in each provider dashboard:
       Google:  http://localhost:5000/oauth/google/callback
       GitHub:  http://localhost:5000/oauth/github/callback
"""

import re
import secrets
from datetime import datetime

from flask import Blueprint, redirect, url_for, session, request, jsonify, current_app
import requests as http_req
from models import db, User, Progress

oauth_bp = Blueprint('oauth', __name__, url_prefix='/oauth')


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _clean_username(raw: str) -> str:
    """Turn a display name into a safe, unique username."""
    base = re.sub(r'[^a-zA-Z0-9_]', '', raw.replace(' ', '_'))[:20] or 'user'
    # Ensure uniqueness
    candidate = base.lower()
    n = 1
    while User.query.filter_by(username=candidate).first():
        candidate = f"{base.lower()}{n}"
        n += 1
    return candidate


def _upsert_oauth_user(provider: str, oauth_id: str, email: str,
                       name: str, avatar_url: str = None) -> User:
    """
    Find-or-create a User record for an OAuth login.
    If the email already exists (password account), attach OAuth to it.
    """
    # 1. Existing OAuth user
    user = User.query.filter_by(oauth_provider=provider, oauth_id=str(oauth_id)).first()
    if user:
        user.last_login = datetime.utcnow()
        db.session.commit()
        return user

    # 2. Existing email account → link OAuth to it
    user = User.query.filter_by(email=email).first()
    if user:
        user.oauth_provider = provider
        user.oauth_id       = str(oauth_id)
        user.avatar_url     = avatar_url
        user.display_name   = name
        user.last_login     = datetime.utcnow()
        db.session.commit()
        return user

    # 3. Brand-new user via OAuth
    username = _clean_username(name or email.split('@')[0])
    user = User(
        username       = username,
        email          = email,
        password       = None,            # No password for OAuth accounts
        oauth_provider = provider,
        oauth_id       = str(oauth_id),
        avatar_url     = avatar_url,
        display_name   = name,
    )
    db.session.add(user)
    db.session.flush()   # Get user.id before committing

    # Seed progress row
    db.session.add(Progress(user_id=user.id, budgeting_level=1))
    db.session.commit()
    return user


def _set_session(user: User):
    session['user_id']  = user.id
    session['username'] = user.username


# ─── Google OAuth ─────────────────────────────────────────────────────────────

GOOGLE_AUTH_URL    = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL   = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO    = 'https://www.googleapis.com/oauth2/v3/userinfo'
GOOGLE_SCOPE       = 'openid email profile'


@oauth_bp.route('/google')
def google_login():
    client_id = current_app.config.get('GOOGLE_CLIENT_ID', '')
    if not client_id:
        return _provider_not_configured('Google')

    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    callback = url_for('oauth.google_callback', _external=True)

    params = {
        'client_id':     client_id,
        'redirect_uri':  callback,
        'response_type': 'code',
        'scope':         GOOGLE_SCOPE,
        'state':         state,
        'access_type':   'online',
    }
    from urllib.parse import urlencode
    return redirect(f"{GOOGLE_AUTH_URL}?{urlencode(params)}")


@oauth_bp.route('/google/callback')
def google_callback():
    client_id     = current_app.config.get('GOOGLE_CLIENT_ID', '')
    client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET', '')

    if request.args.get('state') != session.pop('oauth_state', None):
        return _oauth_error('State mismatch – possible CSRF. Please try again.')

    code = request.args.get('code')
    if not code:
        return _oauth_error(request.args.get('error', 'Google login cancelled.'))

    # Exchange code for token
    callback = url_for('oauth.google_callback', _external=True)
    token_resp = http_req.post(GOOGLE_TOKEN_URL, data={
        'code':          code,
        'client_id':     client_id,
        'client_secret': client_secret,
        'redirect_uri':  callback,
        'grant_type':    'authorization_code',
    }, timeout=10)

    if not token_resp.ok:
        return _oauth_error('Failed to obtain token from Google.')

    access_token = token_resp.json().get('access_token')
    info = http_req.get(GOOGLE_USERINFO,
                        headers={'Authorization': f'Bearer {access_token}'},
                        timeout=10).json()

    user = _upsert_oauth_user(
        provider   = 'google',
        oauth_id   = info['sub'],
        email      = info['email'],
        name       = info.get('name', ''),
        avatar_url = info.get('picture'),
    )
    _set_session(user)
    return redirect(url_for('dashboard.dashboard'))


# ─── GitHub OAuth ─────────────────────────────────────────────────────────────

GITHUB_AUTH_URL  = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_USER_URL  = 'https://api.github.com/user'
GITHUB_EMAIL_URL = 'https://api.github.com/user/emails'
GITHUB_SCOPE     = 'read:user user:email'


@oauth_bp.route('/github')
def github_login():
    client_id = current_app.config.get('GITHUB_CLIENT_ID', '')
    if not client_id:
        return _provider_not_configured('GitHub')

    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state
    callback = url_for('oauth.github_callback', _external=True)

    from urllib.parse import urlencode
    params = {
        'client_id':    client_id,
        'redirect_uri': callback,
        'scope':        GITHUB_SCOPE,
        'state':        state,
    }
    return redirect(f"{GITHUB_AUTH_URL}?{urlencode(params)}")


@oauth_bp.route('/github/callback')
def github_callback():
    client_id     = current_app.config.get('GITHUB_CLIENT_ID', '')
    client_secret = current_app.config.get('GITHUB_CLIENT_SECRET', '')

    if request.args.get('state') != session.pop('oauth_state', None):
        return _oauth_error('State mismatch – possible CSRF. Please try again.')

    code = request.args.get('code')
    if not code:
        return _oauth_error(request.args.get('error', 'GitHub login cancelled.'))

    callback = url_for('oauth.github_callback', _external=True)
    token_resp = http_req.post(GITHUB_TOKEN_URL, data={
        'client_id':     client_id,
        'client_secret': client_secret,
        'code':          code,
        'redirect_uri':  callback,
    }, headers={'Accept': 'application/json'}, timeout=10)

    if not token_resp.ok:
        return _oauth_error('Failed to obtain token from GitHub.')

    access_token = token_resp.json().get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept':        'application/vnd.github+json',
    }

    profile = http_req.get(GITHUB_USER_URL, headers=headers, timeout=10).json()

    # GitHub may hide email → fetch via emails endpoint
    email = profile.get('email')
    if not email:
        emails = http_req.get(GITHUB_EMAIL_URL, headers=headers, timeout=10).json()
        primary = next((e for e in emails if e.get('primary')), None)
        email = primary['email'] if primary else f"gh_{profile['id']}@github.invalid"

    user = _upsert_oauth_user(
        provider   = 'github',
        oauth_id   = profile['id'],
        email      = email,
        name       = profile.get('name') or profile.get('login', ''),
        avatar_url = profile.get('avatar_url'),
    )
    _set_session(user)
    return redirect(url_for('dashboard.dashboard'))


# ─── Error helpers ────────────────────────────────────────────────────────────

def _provider_not_configured(name: str):
    """Redirect to login with a flash-style error in session."""
    session['oauth_error'] = (
        f"{name} OAuth is not configured. "
        f"Please set {name.upper()}_CLIENT_ID and {name.upper()}_CLIENT_SECRET."
    )
    return redirect(url_for('auth.login'))


def _oauth_error(msg: str):
    session['oauth_error'] = msg
    return redirect(url_for('auth.login'))
