"""
FinLiteracy – Database Models
Extended with:
  - OAuth fields (provider, oauth_id, avatar_url)
  - InvestmentProgress (Feature 3)
  - Achievements, Scenarios, UserProgress, Investments, Leaderboard support
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ─── User ─────────────────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password      = db.Column(db.String(200), nullable=True)   # Nullable for OAuth-only users
    xp            = db.Column(db.Integer, default=0)
    coins         = db.Column(db.Integer, default=100)
    level         = db.Column(db.Integer, default=1)
    streak_days   = db.Column(db.Integer, default=0)
    last_login    = db.Column(db.DateTime, default=datetime.utcnow)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # ─── OAuth fields ────────────────────────────────────────────────────
    oauth_provider = db.Column(db.String(30),  nullable=True)   # 'google' | 'github' | None
    oauth_id       = db.Column(db.String(200), nullable=True)   # Provider unique user id
    avatar_url     = db.Column(db.String(500), nullable=True)   # Profile picture URL

    # Relationships
    progress            = db.relationship('Progress',           backref='user', lazy=True, uselist=False)
    investments         = db.relationship('Investment',         backref='user', lazy=True)
    achievements        = db.relationship('UserAchievement',    backref='user', lazy=True)
    investment_progress = db.relationship('InvestmentProgress', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id':             self.id,
            'username':       self.username,
            'xp':             self.xp,
            'coins':          self.coins,
            'level':          self.level,
            'streak_days':    self.streak_days,
            'avatar_url':     self.avatar_url,
            'oauth_provider': self.oauth_provider,
        }

    def __repr__(self):
        return f'<User {self.username}>'


# ─── Progress ─────────────────────────────────────────────────────────────────

class Progress(db.Model):
    __tablename__ = 'progress'

    id                   = db.Column(db.Integer, primary_key=True)
    user_id              = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scenarios_completed  = db.Column(db.Integer, default=0)
    financial_score      = db.Column(db.Float,   default=50.0)
    budgeting_score      = db.Column(db.Float,   default=0.0)
    saving_score         = db.Column(db.Float,   default=0.0)
    investing_score      = db.Column(db.Float,   default=0.0)
    debt_score           = db.Column(db.Float,   default=0.0)
    budgeting_level      = db.Column(db.Integer, default=0)
    saving_level         = db.Column(db.Integer, default=0)
    debt_level           = db.Column(db.Integer, default=0)
    investing_level      = db.Column(db.Integer, default=0)
    independence_level   = db.Column(db.Integer, default=0)
    badges_earned        = db.Column(db.String(500), default='')
    weak_area            = db.Column(db.String(50), default='budgeting')
    updated_at           = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'scenarios_completed': self.scenarios_completed,
            'financial_score':     self.financial_score,
            'budgeting_score':     self.budgeting_score,
            'saving_score':        self.saving_score,
            'investing_score':     self.investing_score,
            'debt_score':          self.debt_score,
            'budgeting_level':     self.budgeting_level,
            'saving_level':        self.saving_level,
            'debt_level':          self.debt_level,
            'investing_level':     self.investing_level,
            'independence_level':  self.independence_level,
            'badges_earned':       self.badges_earned.split(',') if self.badges_earned else [],
            'weak_area':           self.weak_area,
        }


# ─── Scenario ─────────────────────────────────────────────────────────────────

class Scenario(db.Model):
    __tablename__ = 'scenarios'

    id          = db.Column(db.Integer, primary_key=True)
    slug        = db.Column(db.String(60), unique=True, nullable=False)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category    = db.Column(db.String(40), default='general')
    difficulty  = db.Column(db.String(20), default='medium')
    xp_reward   = db.Column(db.Integer, default=100)
    coins_reward= db.Column(db.Integer, default=40)
    avatar_emoji= db.Column(db.String(10), default='💼')

    def to_dict(self):
        return {
            'id':          self.id,
            'slug':        self.slug,
            'title':       self.title,
            'description': self.description,
            'category':    self.category,
            'difficulty':  self.difficulty,
            'xp_reward':   self.xp_reward,
            'coins_reward':self.coins_reward,
            'avatar_emoji':self.avatar_emoji,
        }


# ─── UserScenarioResult ───────────────────────────────────────────────────────

class UserScenarioResult(db.Model):
    __tablename__ = 'user_scenario_results'

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.id'), nullable=False)
    choice      = db.Column(db.String(40))
    xp_earned   = db.Column(db.Integer, default=0)
    score_delta = db.Column(db.Float, default=0.0)
    category    = db.Column(db.String(40))
    completed_at= db.Column(db.DateTime, default=datetime.utcnow)

    user     = db.relationship('User',     backref='scenario_results')
    scenario = db.relationship('Scenario', backref='results')


# ─── Investment ───────────────────────────────────────────────────────────────

class Investment(db.Model):
    __tablename__ = 'investments'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    asset_type   = db.Column(db.String(30), nullable=False)
    amount       = db.Column(db.Float, nullable=False)
    current_value= db.Column(db.Float, nullable=False)
    return_pct   = db.Column(db.Float, default=0.0)
    invested_at  = db.Column(db.DateTime, default=datetime.utcnow)
    is_active    = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id':           self.id,
            'asset_type':   self.asset_type,
            'amount':       self.amount,
            'current_value':self.current_value,
            'return_pct':   self.return_pct,
            'invested_at':  self.invested_at.isoformat(),
        }


# ─── InvestmentProgress (Feature 3) ──────────────────────────────────────────

class InvestmentProgress(db.Model):
    """Tracks which invest-learn lessons and quizzes a user has completed."""
    __tablename__ = 'investment_progress'

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_completed = db.Column(db.String(60), nullable=False)   # e.g. 'what_is_investing'
    quiz_score       = db.Column(db.Integer, default=0)           # 0–100
    completed_at     = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'lesson_completed', name='uq_user_lesson'),
    )

    def to_dict(self):
        return {
            'lesson_completed': self.lesson_completed,
            'quiz_score':       self.quiz_score,
            'completed_at':     self.completed_at.isoformat(),
        }


# ─── Achievement (badge catalog) ──────────────────────────────────────────────

BADGE_CATALOG = {
    'first_save':       {'name': 'First Save',        'icon': '💰', 'desc': 'Made your first smart saving decision'},
    'budget_master':    {'name': 'Budget Master',      'icon': '📊', 'desc': 'Mastered budgeting scenarios'},
    'streak_3':         {'name': '3-Day Streak',       'icon': '🔥', 'desc': 'Learned 3 days in a row'},
    'streak_7':         {'name': 'Week Warrior',       'icon': '⚡', 'desc': 'Kept a 7-day learning streak'},
    'debt_destroyer':   {'name': 'Debt Destroyer',     'icon': '💳', 'desc': 'Conquered debt management scenarios'},
    'smart_investor':   {'name': 'Smart Investor',     'icon': '📈', 'desc': 'Started investing wisely'},
    'diversified':      {'name': 'Diversified',        'icon': '🌐', 'desc': 'Invested across 3+ asset types'},
    'emergency_ready':  {'name': 'Emergency Ready',    'icon': '🛡️', 'desc': 'Built a strong emergency fund'},
    'finance_champ':    {'name': 'Finance Champion',   'icon': '🏆', 'desc': 'Completed all learning modules'},
    'scenario_5':       {'name': 'Scenario Pro',       'icon': '🎯', 'desc': 'Completed 5 scenarios'},
    'invest_learner':   {'name': 'Invest Learner',     'icon': '📚', 'desc': 'Completed the Invest Learning section'},
    'budgeting_cert':   {'name': 'Budget Graduate',    'icon': '🎓', 'desc': 'Passed the Budgeting Basics quiz'},
    'saving_cert':      {'name': 'Saving Expert',      'icon': '🎓', 'desc': 'Passed the Saving Strategies quiz'},
    'debt_cert':        {'name': 'Debt Destroyer',     'icon': '🎓', 'desc': 'Passed the Debt Management quiz'},
    'investing_cert':   {'name': 'Investment Scholar', 'icon': '🎓', 'desc': 'Passed the Investing Basics quiz'},
    'independence_cert':{'name': 'FIRE Graduate',      'icon': '🎓', 'desc': 'Passed the Financial Independence quiz'},
}


# ─── Learning Step Progress ───────────────────────────────────────────────────

class LearningStepProgress(db.Model):
    """
    Tracks which individual topic steps a user has completed.
    One row per (user, level_slug, topic_slug).
    """
    __tablename__ = 'learning_step_progress'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    level_slug   = db.Column(db.String(40), nullable=False)
    topic_slug   = db.Column(db.String(60), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'level_slug', 'topic_slug', name='uq_user_topic'),
    )

    user = db.relationship('User', backref='step_progress')


# ─── Level Quiz Result ────────────────────────────────────────────────────────

class LevelQuizResult(db.Model):
    """
    Stores quiz attempt results for each learning level.
    A user may attempt a quiz multiple times; the best score is kept.
    """
    __tablename__ = 'level_quiz_results'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    level_slug   = db.Column(db.String(40), nullable=False)
    score        = db.Column(db.Integer, default=0)   # percentage 0-100
    passed       = db.Column(db.Boolean, default=False)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='quiz_results')


class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id   = db.Column(db.String(40), nullable=False)
    earned_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        info = BADGE_CATALOG.get(self.badge_id, {})
        return {
            'badge_id':  self.badge_id,
            'name':      info.get('name', self.badge_id),
            'icon':      info.get('icon', '🏅'),
            'desc':      info.get('desc', ''),
            'earned_at': self.earned_at.isoformat(),
        }
