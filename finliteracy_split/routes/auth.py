"""
FinLiteracy – Auth Routes
Handles: GET /  →  redirect to login
         GET/POST /login
         GET /logout
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User

auth_bp = Blueprint('auth', __name__)


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
        if user and user.password == password:
            session['user_id']  = user.id
            session['username'] = user.username
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
