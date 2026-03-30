"""
FinLiteracy – Investment Simulator Routes
Handles: GET  /invest
         POST /invest/buy
         POST /invest/simulate
"""

import json
import random
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Investment
from config import INVESTMENT_ASSETS
from services.gamification import check_and_award_badges, badge_info_list
from utils import get_current_user

investment_bp = Blueprint('investment', __name__)

_VIRTUAL_STARTING_BALANCE = 10_000


@investment_bp.route('/invest')
def invest():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    investments    = [inv for inv in user.investments if inv.is_active]
    total_invested = sum(inv.amount for inv in investments)
    total_current  = sum(inv.current_value for inv in investments)

    return render_template('investment_simulator.html',
        user=user,
        investments=investments,
        assets=INVESTMENT_ASSETS,
        total_invested=total_invested,
        total_current=total_current,
        starting_balance=_VIRTUAL_STARTING_BALANCE,
        assets_json=json.dumps(INVESTMENT_ASSETS),
    )


@investment_bp.route('/invest/buy', methods=['POST'])
def invest_buy():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401

    data       = request.get_json()
    asset_type = data.get('asset_type')
    amount     = float(data.get('amount', 0))

    if asset_type not in INVESTMENT_ASSETS:
        return jsonify({'error': 'Invalid asset'}), 400
    if amount < 100:
        return jsonify({'error': 'Minimum investment is ₹100'}), 400
    if amount > user.coins * 10:
        return jsonify({'error': 'Insufficient virtual funds'}), 400

    cfg           = INVESTMENT_ASSETS[asset_type]
    return_pct    = round(random.uniform(cfg['min_return'], cfg['max_return']), 2)
    current_value = round(amount * (1 + return_pct / 100), 2)

    db.session.add(Investment(
        user_id=user.id,
        asset_type=asset_type,
        amount=amount,
        current_value=current_value,
        return_pct=return_pct,
    ))

    xp_bonus  = 150 if return_pct > 0 else 100
    user.xp  += xp_bonus

    new_badges = check_and_award_badges(user)
    db.session.commit()

    direction = 'rose' if return_pct >= 0 else 'fell'
    return jsonify({
        'success':       True,
        'asset_type':    asset_type,
        'amount':        amount,
        'current_value': current_value,
        'return_pct':    return_pct,
        'xp_earned':     xp_bonus,
        'new_xp':        user.xp,
        'message': (
            f"You invested ₹{amount:,.0f} in {cfg['name']}. "
            f"Market {direction} {abs(return_pct):.1f}%. "
            f"Your balance is now ₹{current_value:,.0f}. +{xp_bonus} XP! 🎉"
        ),
        'new_badges': badge_info_list(new_badges),
    })


@investment_bp.route('/invest/simulate', methods=['POST'])
def invest_simulate():
    """Re-simulate market movements on all active investments."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401

    updates = []
    for inv in user.investments:
        if not inv.is_active:
            continue
        cfg           = INVESTMENT_ASSETS.get(inv.asset_type, INVESTMENT_ASSETS['fd'])
        new_return    = round(random.uniform(cfg['min_return'], cfg['max_return']), 2)
        inv.return_pct    = new_return
        inv.current_value = round(inv.amount * (1 + new_return / 100), 2)
        updates.append(inv.to_dict())

    db.session.commit()
    return jsonify({'updates': updates})
