"""
FinLiteracy - Application Entry Point
Creates the Flask app, initialises the database, seeds demo data,
and registers all route blueprints.
"""

import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from models import db
from routes import register_routes
from services.seeder import seed_database


def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Respect Railway/Reverse proxy forwarded scheme and host.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # OAuth callbacks use redirects; SameSite=Lax is required.
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = (
        os.environ.get("SESSION_COOKIE_SECURE", "true").lower() == "true"
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_database()

    register_routes(app)
    return app


app = create_app()

if __name__ == "__main__":
    print("FinLiteracy running on local development mode")
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true",
    )
