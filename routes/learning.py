"""
FinLiteracy – Learning Path Routes (Full Implementation)

Endpoints:
  GET  /learning                          – Overview of all levels
  GET  /learning/<level_slug>             – Level detail: list of topics
  GET  /learning/<level_slug>/<topic>     – Topic reader with steps
  POST /learning/<level_slug>/<topic>/complete  – Mark topic done
  GET  /learning/<level_slug>/quiz        – Quiz page
  POST /learning/<level_slug>/quiz/submit – Submit quiz answers
  GET  /learning/<level_slug>/certificate – Download PDF certificate
"""

from flask import (Blueprint, render_template, redirect, url_for,
                   request, jsonify, send_file, flash)
from models import db, Progress, LearningStepProgress, LevelQuizResult, UserAchievement
from utils import get_current_user
from data.learning_content import LEVELS, LEVELS_BY_SLUG, get_level, get_topic
from services.certificate import generate_certificate
import io

learning_bp = Blueprint('learning', __name__)

PASS_SCORE   = 70
QUIZ_XP      = 100
TOPIC_XP     = 50
TOPIC_COINS  = 10


def _completed_topics(user_id, level_slug):
    rows = LearningStepProgress.query.filter_by(user_id=user_id, level_slug=level_slug).all()
    return {r.topic_slug for r in rows}


def _all_topics_done(user_id, level):
    done = _completed_topics(user_id, level['slug'])
    return all(t['slug'] in done for t in level['topics'])


def _best_quiz_score(user_id, level_slug):
    return (LevelQuizResult.query
            .filter_by(user_id=user_id, level_slug=level_slug)
            .order_by(LevelQuizResult.score.desc())
            .first())


def _is_level_unlocked(user_id, level):
    prereq_slug = level.get('prerequisite')
    if prereq_slug is None:
        return True
    result = _best_quiz_score(user_id, prereq_slug)
    return result is not None and result.passed


def _level_status(user_id, level):
    if not _is_level_unlocked(user_id, level):
        return 'locked'
    result = _best_quiz_score(user_id, level['slug'])
    if result and result.passed:
        return 'complete'
    return 'active'


def _award_badge(user, badge_id):
    already = UserAchievement.query.filter_by(user_id=user.id, badge_id=badge_id).first()
    if not already:
        db.session.add(UserAchievement(user_id=user.id, badge_id=badge_id))
        if user.progress:
            existing = user.progress.badges_earned or ''
            badges = [b for b in existing.split(',') if b]
            if badge_id not in badges:
                badges.append(badge_id)
                user.progress.badges_earned = ','.join(badges)


def _update_level_field(progress, level_field, value):
    current = getattr(progress, level_field, 0) or 0
    if value > current:
        setattr(progress, level_field, value)


@learning_bp.route('/learning')
def learning():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    progress = user.progress or Progress(user_id=user.id)
    levels_data = []
    for level in LEVELS:
        status   = _level_status(user.id, level)
        done_set = _completed_topics(user.id, level['slug'])
        total_t  = len(level['topics'])
        done_t   = sum(1 for t in level['topics'] if t['slug'] in done_set)
        quiz_res = _best_quiz_score(user.id, level['slug'])
        levels_data.append({
            'level': level, 'status': status,
            'done_topics': done_t, 'total_topics': total_t,
            'pct': int(done_t / total_t * 100) if total_t else 0,
            'quiz_score': quiz_res.score if quiz_res else None,
            'quiz_passed': quiz_res.passed if quiz_res else False,
        })
    completed_count = sum(1 for ld in levels_data if ld['status'] == 'complete')
    overall_pct     = int(completed_count / len(LEVELS) * 100)
    return render_template('learning_path.html',
        user=user, progress=progress,
        levels_data=levels_data, overall_pct=overall_pct)


@learning_bp.route('/learning/<level_slug>')
def level_overview(level_slug):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    level = get_level(level_slug)
    if not level:
        return redirect(url_for('learning.learning'))
    if not _is_level_unlocked(user.id, level):
        flash('Complete the previous level first!', 'warning')
        return redirect(url_for('learning.learning'))
    done_set    = _completed_topics(user.id, level_slug)
    all_done    = all(t['slug'] in done_set for t in level['topics'])
    quiz_res    = _best_quiz_score(user.id, level_slug)
    topics_info = [{'topic': t, 'done': t['slug'] in done_set} for t in level['topics']]
    return render_template('learning_level.html',
        user=user, level=level, topics_info=topics_info,
        all_topics_done=all_done, quiz_result=quiz_res)


@learning_bp.route('/learning/<level_slug>/<topic_slug>')
def topic_reader(level_slug, topic_slug):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    level = get_level(level_slug)
    if not level or not _is_level_unlocked(user.id, level):
        return redirect(url_for('learning.learning'))
    topic = next((t for t in level['topics'] if t['slug'] == topic_slug), None)
    if not topic:
        return redirect(url_for('learning.level_overview', level_slug=level_slug))
    done_set   = _completed_topics(user.id, level_slug)
    is_done    = topic_slug in done_set
    topic_list = level['topics']
    idx        = next(i for i, t in enumerate(topic_list) if t['slug'] == topic_slug)
    prev_topic = topic_list[idx - 1] if idx > 0 else None
    next_topic = topic_list[idx + 1] if idx < len(topic_list) - 1 else None
    return render_template('learning_topic.html',
        user=user, level=level, topic=topic, is_done=is_done,
        prev_topic=prev_topic, next_topic=next_topic,
        topic_index=idx + 1, total_topics=len(topic_list))


@learning_bp.route('/learning/<level_slug>/<topic_slug>/complete', methods=['POST'])
def complete_topic(level_slug, topic_slug):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    level = get_level(level_slug)
    if not level or not _is_level_unlocked(user.id, level):
        return jsonify({'error': 'Level not available'}), 403
    topic = next((t for t in level['topics'] if t['slug'] == topic_slug), None)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    existing = LearningStepProgress.query.filter_by(
        user_id=user.id, level_slug=level_slug, topic_slug=topic_slug).first()
    new_completion = False
    if not existing:
        db.session.add(LearningStepProgress(
            user_id=user.id, level_slug=level_slug, topic_slug=topic_slug))
        user.xp    = (user.xp or 0) + TOPIC_XP
        user.coins = (user.coins or 0) + TOPIC_COINS
        new_completion = True
        if user.progress:
            _update_level_field(user.progress, level['level_field'], 1)
    done_set = _completed_topics(user.id, level_slug)
    done_set.add(topic_slug)
    all_done = all(t['slug'] in done_set for t in level['topics'])
    db.session.commit()
    return jsonify({
        'success': True, 'all_done': all_done,
        'xp_earned': TOPIC_XP if new_completion else 0,
        'coins_earned': TOPIC_COINS if new_completion else 0,
    })


@learning_bp.route('/learning/<level_slug>/quiz')
def quiz_page(level_slug):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    level = get_level(level_slug)
    if not level:
        return redirect(url_for('learning.learning'))
    if not _is_level_unlocked(user.id, level):
        flash('Complete the previous level first!', 'warning')
        return redirect(url_for('learning.learning'))
    if not _all_topics_done(user.id, level):
        flash('Complete all topics before taking the quiz!', 'warning')
        return redirect(url_for('learning.level_overview', level_slug=level_slug))
    quiz_res = _best_quiz_score(user.id, level_slug)
    return render_template('learning_quiz.html',
        user=user, level=level, questions=level['quiz'], previous_result=quiz_res)


@learning_bp.route('/learning/<level_slug>/quiz/submit', methods=['POST'])
def quiz_submit(level_slug):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    level = get_level(level_slug)
    if not level:
        return jsonify({'error': 'Level not found'}), 404
    if not _is_level_unlocked(user.id, level) or not _all_topics_done(user.id, level):
        return jsonify({'error': 'Not eligible'}), 403
    data      = request.get_json()
    answers   = data.get('answers', {})
    questions = level['quiz']
    correct_count = 0
    results = []
    for i, q in enumerate(questions):
        user_ans   = answers.get(str(i), '')
        is_correct = user_ans.upper() == q['correct'].upper()
        if is_correct:
            correct_count += 1
        results.append({
            'question': q['q'], 'your_answer': user_ans,
            'correct': q['correct'], 'is_correct': is_correct,
            'explanation': q['explanation'], 'options': q['options'],
        })
    score  = int(correct_count / len(questions) * 100)
    passed = score >= PASS_SCORE
    db.session.add(LevelQuizResult(
        user_id=user.id, level_slug=level_slug, score=score, passed=passed))
    if passed:
        if user.progress:
            _update_level_field(user.progress, level['level_field'], 2)
            score_field_map = {
                'budgeting': 'budgeting_score', 'saving': 'saving_score',
                'debt': 'debt_score', 'investing': 'investing_score',
            }
            sf = score_field_map.get(level_slug)
            if sf:
                setattr(user.progress, sf, max(getattr(user.progress, sf, 0), score))
            scores = [user.progress.budgeting_score, user.progress.saving_score,
                      user.progress.debt_score, user.progress.investing_score]
            user.progress.financial_score = min(100, sum(scores) / len(scores))
        user.xp    = (user.xp or 0) + level['xp_reward'] + QUIZ_XP
        user.coins = (user.coins or 0) + level['coins_reward']
        badge_map  = {
            'budgeting': 'budgeting_cert', 'saving': 'saving_cert',
            'debt': 'debt_cert', 'investing': 'investing_cert',
            'independence': 'independence_cert',
        }
        if level_slug in badge_map:
            _award_badge(user, badge_map[level_slug])
        if all(_best_quiz_score(user.id, l['slug']) and
               _best_quiz_score(user.id, l['slug']).passed for l in LEVELS):
            _award_badge(user, 'finance_champ')
    db.session.commit()
    return jsonify({
        'score': score, 'passed': passed,
        'correct': correct_count, 'total': len(questions),
        'results': results,
        'xp_earned': level['xp_reward'] + QUIZ_XP if passed else 0,
    })


@learning_bp.route('/learning/<level_slug>/certificate')
def download_certificate(level_slug):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    level    = get_level(level_slug)
    if not level:
        return redirect(url_for('learning.learning'))
    quiz_res = _best_quiz_score(user.id, level_slug)
    if not quiz_res or not quiz_res.passed:
        flash('Pass the quiz first to download your certificate!', 'warning')
        return redirect(url_for('learning.quiz_page', level_slug=level_slug))
    pdf_bytes = generate_certificate(
        username=user.username, level_title=level['title'],
        level_slug=level_slug, quiz_score=quiz_res.score,
        completion_date=quiz_res.attempted_at)
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf',
        as_attachment=True,
        download_name=f'FinLiteracy_{level_slug}_certificate.pdf')
