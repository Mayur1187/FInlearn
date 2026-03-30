"""
FinLiteracy – Learning Path Route
Handles: GET /learning
"""

from flask import Blueprint, render_template, redirect, url_for
from models import Progress
from utils import get_current_user

learning_bp = Blueprint('learning', __name__)

# Curated recommendations keyed by weak area
_RECOMMENDATIONS = {
    'budgeting': [
        {'title': '50/30/20 Budget Rule',       'icon': '📊', 'desc': 'Split income into needs, wants, savings'},
        {'title': 'Zero-Based Budgeting',        'icon': '🎯', 'desc': 'Assign every rupee a purpose'},
        {'title': 'Budget Apps for Indians',     'icon': '📱', 'desc': 'Walnut, Money Manager, Spendee'},
    ],
    'saving': [
        {'title': 'Pay Yourself First',          'icon': '💡', 'desc': 'Automate savings before spending'},
        {'title': 'High-Yield Savings Accounts', 'icon': '🏦', 'desc': 'Small Finance Banks offer 6–7%'},
        {'title': 'Goal-Based Saving Buckets',   'icon': '🎯', 'desc': 'Separate accounts for each goal'},
    ],
    'debt': [
        {'title': 'Good vs Bad Debt',            'icon': '⚖️', 'desc': 'Education loans vs credit card debt'},
        {'title': 'Avalanche vs Snowball Method','icon': '❄️', 'desc': 'Two popular debt payoff strategies'},
        {'title': 'How CIBIL Score Works',       'icon': '📈', 'desc': 'Improve your credit score step by step'},
    ],
    'investing': [
        {'title': 'Mutual Funds 101',            'icon': '🌐', 'desc': 'Types, returns, and how to start'},
        {'title': 'SIP: Power of Compounding',   'icon': '📈', 'desc': '₹2,000/month → ₹50 lakh in 20 years'},
        {'title': 'Stock Market Basics',         'icon': '🏛️', 'desc': 'NSE, BSE, Nifty, Sensex explained'},
    ],
}


@learning_bp.route('/learning')
def learning():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    progress = user.progress or Progress(user_id=user.id)
    weak_area   = progress.weak_area or 'budgeting'
    recommended = _RECOMMENDATIONS.get(weak_area, _RECOMMENDATIONS['budgeting'])

    # Overall completion percentage across all five learning levels
    levels    = [
        progress.budgeting_level, progress.saving_level,
        progress.debt_level, progress.investing_level, progress.independence_level,
    ]
    overall_pct = int(sum(min(l, 2) for l in levels) / (len(levels) * 2) * 100)

    return render_template('learning_path.html',
        user=user,
        progress=progress,
        overall_pct=overall_pct,
        recommended=recommended,
        weak_area=weak_area,
    )
