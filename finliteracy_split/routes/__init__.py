"""
FinLiteracy – Route Blueprint Registration
Import and register all blueprints here, then call register_routes(app).
"""

from .auth         import auth_bp
from .dashboard    import dashboard_bp
from .scenarios    import scenarios_bp
from .learning     import learning_bp
from .investment   import investment_bp
from .leaderboard  import leaderboard_bp
from .achievements import achievements_bp
from .mentor       import mentor_bp
from .api          import api_bp


def register_routes(app):
    """Register all blueprints on the Flask app."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(scenarios_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(investment_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(achievements_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(api_bp)
