"""
FinLiteracy – Database Seeder
Seeds the demo user, leaderboard users, scenario catalog, investments,
and achievements on first run.
"""

import random
from models import db, User, Progress, Scenario, Investment, UserAchievement
from data.scenarios import SCENARIO_CATALOG
from config import INVESTMENT_ASSETS


def seed_database():
    """Seed demo users and the scenario catalog into the database."""
    _seed_scenarios()
    _seed_demo_user()
    _seed_leaderboard_users()
    db.session.commit()


# ─── Internal helpers ──────────────────────────────────────────────────────────

def _seed_scenarios():
    for sc in SCENARIO_CATALOG:
        if not Scenario.query.filter_by(slug=sc['slug']).first():
            new_sc = Scenario(
                slug=sc['slug'],
                title=sc['title'],
                description=sc['description'],
                category=sc['category'],
                difficulty=sc['difficulty'],
                xp_reward=sc['xp_reward'],
                coins_reward=sc['coins_reward'],
                avatar_emoji=sc['avatar_emoji'],
            )
            db.session.add(new_sc)


def _seed_demo_user():
    if User.query.filter_by(username='demo').first():
        return

    demo_user = User(
        username='demo',
        email='demo@finliteracy.app',
        password='demo123',
        xp=1240,
        coins=850,
        level=3,
        streak_days=5,
    )
    db.session.add(demo_user)
    db.session.flush()

    demo_progress = Progress(
        user_id=demo_user.id,
        scenarios_completed=7,
        financial_score=72.5,
        budgeting_score=85.0,
        saving_score=60.0,
        investing_score=30.0,
        debt_score=45.0,
        budgeting_level=2,
        saving_level=1,
        debt_level=0,
        investing_level=0,
        independence_level=0,
        badges_earned='first_save,budget_master,streak_3',
        weak_area='investing',
    )
    db.session.add(demo_progress)

    for asset, amount in [('fd', 2000), ('mutual_funds', 5000), ('stocks', 3000)]:
        cfg = INVESTMENT_ASSETS[asset]
        ret = round(random.uniform(cfg['min_return'], cfg['max_return']), 2)
        db.session.add(Investment(
            user_id=demo_user.id,
            asset_type=asset,
            amount=amount,
            current_value=round(amount * (1 + ret / 100), 2),
            return_pct=ret,
        ))

    for badge_id in ['first_save', 'budget_master', 'streak_3']:
        db.session.add(UserAchievement(user_id=demo_user.id, badge_id=badge_id))

    print("✅ Demo user seeded: username=demo, password=demo123")


def _seed_leaderboard_users():
    for uname, uxp, ulevel in [
        ('aryan_k', 4200, 8),
        ('priya_m', 3850, 7),
        ('rahul_99', 980, 2),
    ]:
        if not User.query.filter_by(username=uname).first():
            u = User(
                username=uname,
                email=f'{uname}@demo.com',
                password='demo123',
                xp=uxp,
                level=ulevel,
                coins=uxp // 4,
            )
            db.session.add(u)
            db.session.flush()
            db.session.add(Progress(
                user_id=u.id,
                scenarios_completed=random.randint(2, 15),
                financial_score=round(random.uniform(40, 90), 1),
            ))
