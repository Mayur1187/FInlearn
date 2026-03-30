"""
FinLiteracy – REST API Routes
Handles: GET  /api/user/stats
         GET  /api/leaderboard
         POST /api/ai_mentor_chat        ← Feature 2
         POST /api/invest_learn/complete ← Feature 3
         GET  /api/invest_learn/progress ← Feature 3
"""

from flask import Blueprint, jsonify, request, session
from models import db, User, InvestmentProgress
from services.ai_mentor import call_ai_mentor
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


# ─── Feature 2 – AI Mentor Chat API ──────────────────────────────────────────

@api_bp.route('/ai_mentor_chat', methods=['POST'])
def ai_mentor_chat():
    """
    POST /api/ai_mentor_chat
    Body: { "message": "How do I start investing?" }
    Returns: { "reply": "..." }
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401

    data    = request.get_json(silent=True) or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Empty message'}), 400

    # Build personalised context from user progress
    ctx = None
    if user.progress:
        p   = user.progress
        ctx = (
            f"Financial score: {p.financial_score:.0f}/100, "
            f"Weak area: {p.weak_area}, "
            f"Scenarios completed: {p.scenarios_completed}, "
            f"Level: {user.level}"
        )

    reply = call_ai_mentor(message, ctx)
    return jsonify({'reply': reply})


# ─── Feature 3 – Invest Learn Progress API ───────────────────────────────────

@api_bp.route('/invest_learn/complete', methods=['POST'])
def invest_learn_complete():
    """
    POST /api/invest_learn/complete
    Body: { "lesson": "what_is_investing", "quiz_score": 80 }
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401

    data       = request.get_json(silent=True) or {}
    lesson     = data.get('lesson', '').strip()
    quiz_score = int(data.get('quiz_score', 0))

    if not lesson:
        return jsonify({'error': 'lesson required'}), 400

    # Upsert: update score if already exists (user retook quiz)
    existing = InvestmentProgress.query.filter_by(
        user_id=user.id, lesson_completed=lesson
    ).first()

    if existing:
        if quiz_score > existing.quiz_score:
            existing.quiz_score = quiz_score
    else:
        db.session.add(InvestmentProgress(
            user_id=user.id,
            lesson_completed=lesson,
            quiz_score=quiz_score,
        ))
        # Award XP for completing a new lesson
        user.xp += 75

    db.session.commit()
    return jsonify({
        'success':   True,
        'lesson':    lesson,
        'quiz_score': quiz_score,
        'new_xp':    user.xp,
    })


@api_bp.route('/invest_learn/progress')
def invest_learn_progress():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401

    records = InvestmentProgress.query.filter_by(user_id=user.id).all()
    return jsonify({'completed': [r.to_dict() for r in records]})
