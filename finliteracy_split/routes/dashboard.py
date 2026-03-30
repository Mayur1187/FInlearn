"""
FinLiteracy – Dashboard Route
Handles: GET /dashboard
"""

from flask import Blueprint, render_template, redirect, url_for
from models import Progress, BADGE_CATALOG, User
from utils import get_current_user

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    progress    = user.progress or Progress(user_id=user.id, scenarios_completed=0, financial_score=50.0)
    xp_for_next = user.level * 500
    xp_percent  = min(int((user.xp % xp_for_next) / xp_for_next * 100), 100)

    # Build badge display lists
    earned_badge_ids = (progress.badges_earned or '').split(',')
    earned_badges = [
        {'id': bid, **BADGE_CATALOG.get(bid, {'name': bid, 'icon': '🏅', 'desc': ''})}
        for bid in earned_badge_ids if bid
    ]
    locked_badges = [
        {'id': bid, **BADGE_CATALOG[bid]}
        for bid in BADGE_CATALOG if bid not in earned_badge_ids
    ][:6]

    # Leaderboard snippet (top 5)
    top_users = User.query.order_by(User.xp.desc()).limit(5).all()
    my_rank   = next((i + 1 for i, u in enumerate(top_users) if u.id == user.id), '5+')

    # Investment portfolio summary
    investments      = [inv for inv in user.investments if inv.is_active]
    total_invested   = sum(inv.amount for inv in investments)
    total_current    = sum(inv.current_value for inv in investments)
    portfolio_return = round(
        ((total_current - total_invested) / total_invested * 100) if total_invested > 0 else 0, 1
    )

    return render_template('dashboard.html',
        user=user,
        progress=progress,
        xp_percent=xp_percent,
        xp_for_next=xp_for_next,
        earned_badges=earned_badges,
        locked_badges=locked_badges,
        top_users=top_users,
        my_rank=my_rank,
        investments=investments,
        total_invested=total_invested,
        total_current=total_current,
        portfolio_return=portfolio_return,
    )
