"""
FinLiteracy – Shared Utilities
Helpers used across route modules.
"""

from flask import session
from models import User


def get_current_user():
    """Return the logged-in User from the session, or None."""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None
