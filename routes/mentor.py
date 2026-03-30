"""
FinLiteracy – AI Mentor Routes
Handles: GET  /mentor
         POST /mentor/chat
         GET  /mentor/status
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response, stream_with_context
from services.ai_mentor import call_ai_mentor, get_groq_status
from utils import get_current_user
import json

mentor_bp = Blueprint('mentor', __name__)


@mentor_bp.route('/mentor')
def mentor():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    return render_template('ai_mentor.html', user=user)


@mentor_bp.route('/mentor/status')
def mentor_status():
    """Returns Groq provider status for the UI indicator."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    status = get_groq_status()
    return jsonify(status)


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


@mentor_bp.route('/mentor/chat/stream', methods=['POST'])
def mentor_chat_stream():
    """
    Streaming endpoint — yields SSE chunks for the Groq response.
    Frontend reads these chunks for a real-time typewriter effect.
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401

    data    = request.get_json()
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Empty message'}), 400

    ctx = None
    if user.progress:
        p   = user.progress
        ctx = (
            f"Financial score: {p.financial_score:.0f}/100, "
            f"Weak area: {p.weak_area}, "
            f"Scenarios completed: {p.scenarios_completed}, "
            f"Level: {user.level}"
        )

    def generate():
        try:
            reply = call_ai_mentor(message, ctx)
            for token in reply.split():
                yield f"data: {json.dumps({'token': token + ' '})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as exc:
            err_text = f"Error while generating response: {str(exc)}"
            yield f"data: {json.dumps({'token': err_text})}\n\n"
            yield "data: [DONE]\n\n"

    return Response(stream_with_context(generate()),
                    mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})
