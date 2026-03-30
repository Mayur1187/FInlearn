"""
FinLiteracy – Application Configuration
Contains: Flask config, investment asset catalog.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hackathon-dev-secret-2025')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'finance_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# ─── Investment Assets Catalog ────────────────────────────────────────────────

INVESTMENT_ASSETS = {
    'fd': {
        'name': 'Fixed Deposit',
        'icon': '🏦',
        'color': '#00c875',
        'min_return': 5.5,
        'max_return': 7.5,
        'risk': 'Very Low',
        'description': 'Guaranteed returns, capital protected',
    },
    'stocks': {
        'name': 'Direct Stocks',
        'icon': '📈',
        'color': '#ff7e2d',
        'min_return': -15.0,
        'max_return': 35.0,
        'risk': 'High',
        'description': 'High volatility, high potential reward',
    },
    'mutual_funds': {
        'name': 'Mutual Funds',
        'icon': '🌐',
        'color': '#0cbaba',
        'min_return': 8.0,
        'max_return': 18.0,
        'risk': 'Medium',
        'description': 'Professionally managed, diversified',
    },
    'crypto': {
        'name': 'Cryptocurrency',
        'icon': '🪙',
        'color': '#f7931a',
        'min_return': -40.0,
        'max_return': 80.0,
        'risk': 'Very High',
        'description': 'Extremely volatile, speculative asset',
    },
}
