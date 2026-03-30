"""
FinLiteracy – Auth Routes
Handles:
  GET/POST  /login
  GET       /logout
  GET       /auth/google          → redirect to Google OAuth
  GET       /auth/google/callback → handle Google callback
  GET       /auth/github          → redirect to GitHub OAuth
  GET       /auth/github/callback → handle GitHub callback
"""

import re
import secrets
from datetime import datetime
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, current_app, jsonify)
import requests as http_req
from models import db, User, Progress

auth_bp = Blueprint('auth', __name__)


# ─── Helper: create or fetch OAuth user ───────────────────────────────────────

def _get_or_create_oauth_user(email, name, provider, oauth_id, avatar_url=None):
    """
    Return the User for this OAuth identity, creating one if needed.
    First look by (provider, oauth_id), then fall back to email match.
    """
    # 1. Exact OAuth match
    user = User.query.filter_by(oauth_provider=provider, oauth_id=str(oauth_id)).first()
    if user:
        user.last_login = datetime.utcnow()
        if avatar_url:
            user.avatar_url = avatar_url
        db.session.commit()
        return user

    # 2. Email already registered (link OAuth to existing account)
    user = User.query.filter_by(email=email).first()
    if user:
        user.oauth_provider = provider
        user.oauth_id       = str(oauth_id)
        user.last_login     = datetime.utcnow()
        if avatar_url:
            user.avatar_url = avatar_url
        db.session.commit()
        return user

    # 3. Brand-new user – derive a unique username
    base = re.sub(r'[^a-z0-9_]', '', (name or email.split('@')[0]).lower())[:20] or 'user'
    username = base
    counter  = 1
    while User.query.filter_by(username=username).first():
        username = f"{base}{counter}"
        counter += 1

    user = User(
        username       = username,
        email          = email,
        password       = None,          # OAuth users have no local password
        oauth_provider = provider,
        oauth_id       = str(oauth_id),
        avatar_url     = avatar_url,
        last_login     = datetime.utcnow(),
    )
    db.session.add(user)
    db.session.flush()   # get user.id

    # Bootstrap progress record
    db.session.add(Progress(user_id=user.id, budgeting_level=1))
    db.session.commit()
    return user


def _login_user(user):
    session['user_id']  = user.id
    session['username'] = user.username


# ─── Classic login / logout ───────────────────────────────────────────────────

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and user.password and user.password == password:
            _login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('dashboard.dashboard'))
        else:
            error = 'Invalid credentials. Try demo / demo123'
    return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# ─── Google OAuth ─────────────────────────────────────────────────────────────

GOOGLE_AUTH_URL     = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL    = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
GOOGLE_SCOPE        = 'openid email profile'


@auth_bp.route('/auth/google')
def google_login():
    client_id = current_app.config.get('GOOGLE_CLIENT_ID', '')
    if not client_id:
        return render_template('login.html',
            error='Google OAuth is not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.')

    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state

    callback_url = url_for('auth.google_callback', _external=True)
    params = (
        f"?client_id={client_id}"
        f"&redirect_uri={callback_url}"
        f"&response_type=code"
        f"&scope={GOOGLE_SCOPE.replace(' ', '%20')}"
        f"&state={state}"
        f"&access_type=offline"
    )
    return redirect(GOOGLE_AUTH_URL + params)


@auth_bp.route('/auth/google/callback')
def google_callback():
    error = request.args.get('error')
    if error:
        return render_template('login.html', error=f'Google login cancelled: {error}')

    state = request.args.get('state', '')
    if state != session.pop('oauth_state', None):
        return render_template('login.html', error='Invalid OAuth state. Please try again.')

    code          = request.args.get('code')
    client_id     = current_app.config['GOOGLE_CLIENT_ID']
    client_secret = current_app.config['GOOGLE_CLIENT_SECRET']
    callback_url  = url_for('auth.google_callback', _external=True)

    try:
        # Exchange code for tokens
        token_resp = http_req.post(GOOGLE_TOKEN_URL, data={
            'code':          code,
            'client_id':     client_id,
            'client_secret': client_secret,
            'redirect_uri':  callback_url,
            'grant_type':    'authorization_code',
        }, timeout=10)
        token_resp.raise_for_status()
        tokens = token_resp.json()

        # Fetch user info
        info_resp = http_req.get(GOOGLE_USERINFO_URL,
            headers={'Authorization': f"Bearer {tokens['access_token']}"},
            timeout=10)
        info_resp.raise_for_status()
        info = info_resp.json()

        user = _get_or_create_oauth_user(
            email      = info.get('email', ''),
            name       = info.get('name', ''),
            provider   = 'google',
            oauth_id   = info.get('sub', ''),
            avatar_url = info.get('picture', None),
        )
        _login_user(user)
        return redirect(url_for('dashboard.dashboard'))

    except Exception as exc:
        return render_template('login.html', error=f'Google login failed: {exc}')


# ─── GitHub OAuth ─────────────────────────────────────────────────────────────

GITHUB_AUTH_URL     = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL    = 'https://github.com/login/oauth/access_token'
GITHUB_USERINFO_URL = 'https://api.github.com/user'
GITHUB_EMAIL_URL    = 'https://api.github.com/user/emails'
GITHUB_SCOPE        = 'read:user user:email'


@auth_bp.route('/auth/github')
def github_login():
    client_id = current_app.config.get('GITHUB_CLIENT_ID', '')
    if not client_id:
        return render_template('login.html',
            error='GitHub OAuth is not configured. Please set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET.')

    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state

    callback_url = url_for('auth.github_callback', _external=True)
    params = (
        f"?client_id={client_id}"
        f"&redirect_uri={callback_url}"
        f"&scope={GITHUB_SCOPE.replace(':', '%3A').replace(' ', '%20')}"
        f"&state={state}"
    )
    return redirect(GITHUB_AUTH_URL + params)


@auth_bp.route('/auth/github/callback')
def github_callback():
    error = request.args.get('error')
    if error:
        return render_template('login.html', error=f'GitHub login cancelled: {error}')

    state = request.args.get('state', '')
    if state != session.pop('oauth_state', None):
        return render_template('login.html', error='Invalid OAuth state. Please try again.')

    code          = request.args.get('code')
    client_id     = current_app.config['GITHUB_CLIENT_ID']
    client_secret = current_app.config['GITHUB_CLIENT_SECRET']
    callback_url  = url_for('auth.github_callback', _external=True)

    try:
        # Exchange code for access token
        token_resp = http_req.post(GITHUB_TOKEN_URL, json={
            'client_id':     client_id,
            'client_secret': client_secret,
            'code':          code,
            'redirect_uri':  callback_url,
        }, headers={'Accept': 'application/json'}, timeout=10)
        token_resp.raise_for_status()
        access_token = token_resp.json().get('access_token', '')

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept':        'application/vnd.github+json',
        }

        # Fetch user profile
        info_resp = http_req.get(GITHUB_USERINFO_URL, headers=headers, timeout=10)
        info_resp.raise_for_status()
        info = info_resp.json()

        # GitHub may not expose email publicly – fetch via emails endpoint
        email = info.get('email')
        if not email:
            emails_resp = http_req.get(GITHUB_EMAIL_URL, headers=headers, timeout=10)
            if emails_resp.ok:
                for e in emails_resp.json():
                    if e.get('primary') and e.get('verified'):
                        email = e['email']
                        break
        if not email:
            email = f"github_{info['id']}@noreply.github.com"

        user = _get_or_create_oauth_user(
            email      = email,
            name       = info.get('name') or info.get('login', ''),
            provider   = 'github',
            oauth_id   = info.get('id', ''),
            avatar_url = info.get('avatar_url', None),
        )
        _login_user(user)
        return redirect(url_for('dashboard.dashboard'))

    except Exception as exc:
        return render_template('login.html', error=f'GitHub login failed: {exc}')
