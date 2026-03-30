"""
FinLiteracy – Gamification Service
Handles badge awarding, level-up checks, and achievement tracking.
"""

from models import db, UserAchievement, BADGE_CATALOG


def award_badge(user, badge_id):
    """
    Award a badge to a user if they don't already have it.
    Also keeps the Progress.badges_earned string in sync.
    Returns True if the badge was newly awarded.
    """
    already = UserAchievement.query.filter_by(user_id=user.id, badge_id=badge_id).first()
    if not already:
        ua = UserAchievement(user_id=user.id, badge_id=badge_id)
        db.session.add(ua)

        if user.progress:
            current = user.progress.badges_earned or ''
            badges = [b for b in current.split(',') if b]
            if badge_id not in badges:
                badges.append(badge_id)
                user.progress.badges_earned = ','.join(badges)

        return True
    return False


def check_and_award_badges(user):
    """
    Evaluate all badge conditions for the user and award any newly earned ones.
    Returns a list of newly awarded badge_ids.
    """
    new_badges = []
    progress = user.progress

    if not progress:
        return new_badges

    # Scenario completion milestones
    if progress.scenarios_completed >= 1 and award_badge(user, 'first_save'):
        new_badges.append('first_save')
    if progress.scenarios_completed >= 5 and award_badge(user, 'scenario_5'):
        new_badges.append('scenario_5')

    # Category score thresholds
    if progress.budgeting_score >= 70 and award_badge(user, 'budget_master'):
        new_badges.append('budget_master')
    if progress.debt_score >= 70 and award_badge(user, 'debt_destroyer'):
        new_badges.append('debt_destroyer')
    if progress.investing_score >= 60 and award_badge(user, 'smart_investor'):
        new_badges.append('smart_investor')

    # Login streak milestones
    if user.streak_days >= 3 and award_badge(user, 'streak_3'):
        new_badges.append('streak_3')
    if user.streak_days >= 7 and award_badge(user, 'streak_7'):
        new_badges.append('streak_7')

    # Portfolio diversification (≥3 distinct active asset types)
    active_types = {inv.asset_type for inv in user.investments if inv.is_active}
    if len(active_types) >= 3 and award_badge(user, 'diversified'):
        new_badges.append('diversified')

    # Finance Champion — all learning levels complete
    if (progress.budgeting_level >= 2 and progress.saving_level >= 2 and
            progress.debt_level >= 2 and progress.investing_level >= 2 and
            award_badge(user, 'finance_champ')):
        new_badges.append('finance_champ')

    return new_badges


def level_up_check(user):
    """
    Check whether the user has enough XP to level up.
    Increments user.level if so. Returns True if a level-up occurred.
    """
    xp_needed = user.level * 500
    if user.xp >= xp_needed:
        user.level += 1
        return True
    return False


def badge_info_list(badge_ids):
    """
    Convert a list of badge_ids into full badge-info dicts
    (id, name, icon, desc) suitable for JSON responses.
    """
    return [
        {'id': bid, **BADGE_CATALOG.get(bid, {'name': bid, 'icon': '🏅', 'desc': ''})}
        for bid in badge_ids
    ]
