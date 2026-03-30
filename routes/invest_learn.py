"""
FinLiteracy – Invest Learning Routes (Feature 3)
Handles: GET /invest-learn          → lesson hub
         GET /invest-learn/<lesson> → individual lesson page
"""

from flask import Blueprint, render_template, redirect, url_for
from models import InvestmentProgress
from utils import get_current_user

invest_learn_bp = Blueprint('invest_learn', __name__)

LESSONS = [
    'what_is_investing',
    'types_of_investments',
    'risk_vs_return',
    'beginner_strategy',
]


@invest_learn_bp.route('/invest-learn')
def invest_learn_hub():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    completed = {
        r.lesson_completed: r.quiz_score
        for r in InvestmentProgress.query.filter_by(user_id=user.id).all()
    }
    return render_template('invest_learn.html', user=user,
                           lessons=LESSONS, completed=completed)


@invest_learn_bp.route('/invest-learn/<lesson>')
def invest_learn_lesson(lesson):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    if lesson not in LESSONS:
        return redirect(url_for('invest_learn.invest_learn_hub'))

    prev_score = None
    rec = InvestmentProgress.query.filter_by(user_id=user.id, lesson_completed=lesson).first()
    if rec:
        prev_score = rec.quiz_score

    lesson_index = LESSONS.index(lesson)
    next_lesson  = LESSONS[lesson_index + 1] if lesson_index + 1 < len(LESSONS) else None
    return render_template('invest_lesson.html', user=user,
                           lesson=lesson, prev_score=prev_score,
                           next_lesson=next_lesson)
