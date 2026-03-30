"""
FinLiteracy – AI Mentor Routes
Handles: GET  /mentor
         POST /mentor/chat
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from services.ai_mentor import call_ai_mentor
from utils import get_current_user

mentor_bp = Blueprint('mentor', __name__)


@mentor_bp.route('/mentor')
def mentor():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    return render_template('ai_mentor.html', user=user)


@mentor_bp.route('/mentor/chat', methods=['POST'])
def mentor_chat():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401

    data    = request.get_json()
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Empty message'}), 400

    # Build personalised context from user's progress
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
