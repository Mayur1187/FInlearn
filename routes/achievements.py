"""
FinLiteracy – Achievements Route
Handles: GET /achievements
"""

from flask import Blueprint, render_template, redirect, url_for
from models import BADGE_CATALOG
from utils import get_current_user

achievements_bp = Blueprint('achievements', __name__)


@achievements_bp.route('/achievements')
def achievements():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    earned_ids = {ua.badge_id for ua in user.achievements}
    all_badges = []
    for bid, info in BADGE_CATALOG.items():
        ua = next((a for a in user.achievements if a.badge_id == bid), None)
        all_badges.append({
            'id':       bid,
            'name':     info['name'],
            'icon':     info['icon'],
            'desc':     info['desc'],
            'earned':   bid in earned_ids,
            'earned_at': ua.earned_at.strftime('%d %b %Y') if ua else None,
        })

    return render_template('achievements.html',
        user=user,
        all_badges=all_badges,
        earned_count=len(earned_ids),
        total_count=len(BADGE_CATALOG),
    )
