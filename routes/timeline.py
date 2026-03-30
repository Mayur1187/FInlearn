from flask import Blueprint, jsonify, render_template, request, redirect, url_for

from services.simulator import apply_decision, compare_scenarios, simulate_life
from utils import get_current_user


timeline_bp = Blueprint('timeline', __name__)


@timeline_bp.route('/timeline')
def timeline_page():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    return render_template('timeline.html', user=user)


@timeline_bp.route('/run-simulation', methods=['POST'])
def run_simulation():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json(silent=True) or {}
    primary_data = data.get('primary') or data.get('user_data') or {}
    secondary_data = data.get('secondary')

    try:
        if secondary_data:
            result = compare_scenarios(primary_data, secondary_data)
        else:
            result = {'primary': simulate_life(primary_data)}
        return jsonify(result)
    except Exception as exc:
        return jsonify({'error': f'Simulation failed: {exc}'}), 500


@timeline_bp.route('/decision', methods=['POST'])
def decision():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json(silent=True) or {}
    decision_name = str(data.get('decision', '')).strip().lower()
    base = data.get('user_data') or {}

    if decision_name not in {'invest_more', 'spend_more', 'take_loan'}:
        return jsonify({'error': 'Invalid decision'}), 400

    updated_data = apply_decision(base, decision_name)
    try:
        result = simulate_life(updated_data)
    except Exception as exc:
        return jsonify({'error': f'Decision simulation failed: {exc}'}), 500

    return jsonify({
        'decision': decision_name,
        'updated_user_data': updated_data,
        'primary': result,
    })
