"""
FinLiteracy – Scenario Routes
Handles: GET  /scenario
         POST /scenario/submit
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Progress, Scenario, UserScenarioResult, BADGE_CATALOG
from data.scenarios import SCENARIO_CATALOG, get_scenario_by_slug
from services.gamification import check_and_award_badges, level_up_check, badge_info_list
from utils import get_current_user

scenarios_bp = Blueprint('scenarios', __name__)


@scenarios_bp.route('/scenario')
def scenario():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    completed_slugs = {r.scenario.slug for r in user.scenario_results}
    scenarios_with_status = [
        {**sc, 'completed': sc['slug'] in completed_slugs}
        for sc in SCENARIO_CATALOG
    ]

    return render_template('scenario.html',
        user=user,
        scenarios=scenarios_with_status,
        scenario_data=json.dumps(SCENARIO_CATALOG),
    )


@scenarios_bp.route('/scenario/submit', methods=['POST'])
def scenario_submit():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401

    data       = request.get_json()
    slug       = data.get('slug', 'monthly_allowance')
    choice_key = data.get('choice')

    sc_data = get_scenario_by_slug(slug)
    if not sc_data:
        return jsonify({'error': 'Scenario not found'}), 404

    choice_data = next((c for c in sc_data['choices'] if c['key'] == choice_key), None)
    if not choice_data:
        return jsonify({'error': 'Invalid choice'}), 400

    xp_earned    = choice_data['xp']
    coins_earned = choice_data['coins']
    score_delta  = choice_data['score_delta']

    # Update user stats
    user.xp    += xp_earned
    user.coins += coins_earned
    leveled_up  = level_up_check(user)

    # Ensure progress row exists
    if not user.progress:
        user.progress = Progress(user_id=user.id)
        db.session.add(user.progress)

    p = user.progress
    p.scenarios_completed += 1
    p.financial_score = min(100, max(0, p.financial_score + score_delta))

    # Category-specific score update
    cat = sc_data['category']
    _update_category_score(p, cat, score_delta)

    # Identify new weak area
    scores = {
        'budgeting': p.budgeting_score,
        'saving':    p.saving_score,
        'debt':      p.debt_score,
        'investing': p.investing_score,
    }
    p.weak_area = min(scores, key=scores.get)

    # Persist scenario result
    sc_obj = Scenario.query.filter_by(slug=slug).first()
    if sc_obj:
        db.session.add(UserScenarioResult(
            user_id=user.id,
            scenario_id=sc_obj.id,
            choice=choice_key,
            xp_earned=xp_earned,
            score_delta=score_delta,
            category=cat,
        ))

    new_badges = check_and_award_badges(user)
    db.session.commit()

    return jsonify({
        'xp':            xp_earned,
        'coins':         coins_earned,
        'message':       choice_data['msg'],
        'new_xp':        user.xp,
        'new_coins':     user.coins,
        'new_level':     user.level,
        'leveled_up':    leveled_up,
        'new_badges':    badge_info_list(new_badges),
        'financial_score': round(p.financial_score, 1),
    })


# ─── Private helper ───────────────────────────────────────────────────────────

def _update_category_score(progress, category, score_delta):
    multiplier = 1 if score_delta > 0 else -0.5
    delta = abs(score_delta) * multiplier
    if category == 'budgeting':
        progress.budgeting_score = min(100, progress.budgeting_score + delta)
    elif category == 'saving':
        progress.saving_score    = min(100, progress.saving_score    + delta)
    elif category == 'debt':
        progress.debt_score      = min(100, progress.debt_score      + delta)
    elif category == 'investing':
        progress.investing_score = min(100, progress.investing_score + delta)
