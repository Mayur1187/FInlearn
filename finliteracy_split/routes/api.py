"""
FinLiteracy – REST API Routes
Handles: GET /api/user/stats
         GET /api/leaderboard
"""

from flask import Blueprint, jsonify
from models import User
from utils import get_current_user

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/user/stats')
def user_stats():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401

    data = user.to_dict()
    if user.progress:
        data['progress'] = user.progress.to_dict()
    return jsonify(data)


@api_bp.route('/leaderboard')
def api_leaderboard():
    users = User.query.order_by(User.xp.desc()).limit(10).all()
    return jsonify([u.to_dict() for u in users])
