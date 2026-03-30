"""
FinLiteracy – Application Entry Point
Creates the Flask app, initialises the database, seeds demo data,
and registers all route blueprints.
"""

from flask import Flask
from models import db
from config import Config
from services.seeder import seed_database
from routes import register_routes


def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialise extensions
    db.init_app(app)

    # Bootstrap DB and seed demo data
    with app.app_context():
        db.create_all()
        seed_database()

    # Register all route blueprints
    register_routes(app)

    return app


app = create_app()

if __name__ == '__main__':
    print("🚀 FinLiteracy running at http://localhost:5000")
    print("   Login: demo / demo123")
    app.run(debug=True, port=5000)
