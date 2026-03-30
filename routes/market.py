from flask import Blueprint, render_template
from modules.stock_simulator import StockMarket

market_bp = Blueprint('market', __name__)

@market_bp.route('/market')
def market():
    market = StockMarket()
    prices = [
    {"name": "AAPL", "price": 150},
    {"name": "GOOG", "price": 2800},
    {"name": "TSLA", "price": 700},
    {"name": "AMZN", "price": 3300}
]
    return render_template('market.html', prices=prices)
from flask import jsonify
from modules.stock_simulator import StockMarket

@market_bp.route('/api/live')
def live_data():
    market = StockMarket()
    return jsonify(market.get_live_candle())
from flask import Blueprint, render_template

market_bp = Blueprint('market', __name__)

@market_bp.route('/market')
def market():
    return render_template('market.html')