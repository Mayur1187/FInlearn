"""
FinLiteracy – AI Mentor Routes
Handles: GET  /mentor
         POST /mentor/chat
         GET  /mentor/status   ← new: live Ollama health check for UI
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response, stream_with_context
from services.ai_mentor import call_ai_mentor, get_ollama_status
from utils import get_current_user
import os, requests, json

mentor_bp = Blueprint('mentor', __name__)


@mentor_bp.route('/mentor')
def mentor():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    return render_template('ai_mentor.html', user=user)


@mentor_bp.route('/mentor/status')
def mentor_status():
    """Returns Ollama live status for the UI indicator."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    status = get_ollama_status()
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
    Streaming endpoint — yields SSE tokens as Ollama produces them.
    The frontend EventSource reads these for a real-time typewriter effect.
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

    from services.ai_mentor import _SYSTEM_PROMPT, _pick_model, _smart_fallback
    system = _SYSTEM_PROMPT
    if ctx:
        system += f"\n\nUser profile: {ctx}"

    base_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434').strip().rstrip('/')

    def generate():
        try:
            # Detect model
            tag_resp = requests.get(f'{base_url}/api/tags', timeout=3)
            models = [m['name'] for m in tag_resp.json().get('models', [])]
            model = _pick_model(models)
        except Exception:
            model = 'llama3'

        try:
            with requests.post(
                f'{base_url}/api/chat',
                json={
                    'model': model,
                    'stream': True,
                    'options': {'temperature': 0.7, 'num_predict': 600},
                    'messages': [
                        {'role': 'system', 'content': system},
                        {'role': 'user',   'content': message},
                    ],
                },
                stream=True,
                timeout=120,
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        token = chunk.get('message', {}).get('content', '')
                        if token:
                            yield f"data: {json.dumps({'token': token})}\n\n"
                        if chunk.get('done'):
                            yield "data: [DONE]\n\n"
                            return
        except Exception as exc:
            # Fallback: send full reply as single chunk
            fallback = _smart_fallback(message)
            yield f"data: {json.dumps({'token': fallback})}\n\n"
            yield "data: [DONE]\n\n"

    return Response(stream_with_context(generate()),
                    mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

