"""
FinLiteracy – Leaderboard Route
Handles: GET /leaderboard
"""

from flask import Blueprint, render_template, redirect, url_for
from models import User
from utils import get_current_user

leaderboard_bp = Blueprint('leaderboard', __name__)


@leaderboard_bp.route('/leaderboard')
def leaderboard():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    top_users = User.query.order_by(User.xp.desc()).limit(20).all()
    my_rank   = next((i + 1 for i, u in enumerate(top_users) if u.id == user.id), '20+')

    return render_template('leaderboard.html',
        user=user,
        top_users=top_users,
        my_rank=my_rank,
    )
