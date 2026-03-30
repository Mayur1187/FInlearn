"""
FinLiteracy – Application Entry Point
Creates the Flask app, initialises the database, seeds demo data,
and registers all route blueprints.

New in this version:
  - Loads .env file if present (for local development)
  - Session cookie set to SameSite=Lax for OAuth redirects
  - Registers invest_learn_bp (Feature 3)
"""

import os

# ── Load .env for local development ──────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass   # python-dotenv not installed – read env vars from shell

from flask import Flask
from models import db
from config import Config
from services.seeder import seed_database
from routes import register_routes


def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # OAuth callbacks use redirects; SameSite=Lax is required
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE']   = False   # set True in HTTPS production

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
    print("   OAuth: Google & GitHub (set env vars in .env)")
    print("   AI Mentor: Groq (LLaMA 3) → Ollama → Anthropic → keyword fallback")
    app.run(debug=True, port=5000)

from modules.stock_simulator import StockMarket, Portfolio
market = StockMarket()
portfolio = Portfolio()
@app.route('/market')
def market_view():
    market.update_prices()
    prices = market.get_prices()
    return render_template('market.html', prices=prices)


@app.route('/buy/<stock>')
def buy(stock):
    price = market.get_prices()[stock]
    portfolio.buy_stock(stock, price, 1)
    return redirect('/market')


@app.route('/sell/<stock>')
def sell(stock):
    price = market.get_prices()[stock]
    portfolio.sell_stock(stock, price, 1)
    return redirect('/market')
@app.route('/market')
def market_view():
    return render_template('market.html', prices=prices)
@app.route('/market')
def market():
    from modules.stock_simulator import StockMarket
    market = StockMarket()
    prices = market.get_prices()
    return render_template('market.html', prices=prices)
from flask import render_template