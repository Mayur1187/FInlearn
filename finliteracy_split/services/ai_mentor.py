"""
FinLiteracy – AI Mentor Service
Calls the Claude (Anthropic) API for personalised financial guidance.
Falls back to keyword-based responses when ANTHROPIC_API_KEY is not set.
"""

import os
import requests


def call_ai_mentor(user_message, user_context=None):
    """
    Return a mentor reply for the given user_message.

    If ANTHROPIC_API_KEY is set, the reply comes from Claude Haiku.
    Otherwise a keyword-matching fallback is used.

    Args:
        user_message  (str): The user's chat message.
        user_context  (str): Optional string describing the user's progress
                             (injected into the system prompt).

    Returns:
        str: The mentor reply.
    """
    api_key = os.environ.get('ANTHROPIC_API_KEY')

    if api_key:
        try:
            system_prompt = (
                "You are FinBot, a friendly and knowledgeable financial literacy mentor "
                "for young Indian adults (18-25). You teach personal finance concepts in "
                "simple, engaging language. You focus on: budgeting, saving, investing "
                "(SIPs, mutual funds, stocks), debt management, emergency funds, and "
                "financial independence. Keep responses concise (2-3 paragraphs max), "
                "use emojis sparingly, include concrete Indian rupee examples when helpful, "
                "and always encourage healthy financial habits. Never give specific stock tips."
            )
            if user_context:
                system_prompt += f"\n\nUser context: {user_context}"

            headers = {
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json',
            }
            payload = {
                'model': 'claude-haiku-4-5-20251001',
                'max_tokens': 400,
                'system': system_prompt,
                'messages': [{'role': 'user', 'content': user_message}],
            }
            resp = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=payload,
                timeout=15,
            )
            resp.raise_for_status()
            return resp.json()['content'][0]['text']
        except Exception as e:
            print(f"[AI Mentor] API error: {e} — falling back to keywords")

    return _keyword_fallback(user_message)


# ─── Keyword Fallback ──────────────────────────────────────────────────────────

_KEYWORD_RESPONSES = {
    'budget':    "A great budgeting rule is the **50/30/20 rule**: 50% needs, 30% wants, 20% savings. Start by tracking every rupee for 30 days using any free app — you'll be shocked where money goes! 📊",
    'save':      "Try automating your savings! Set up an auto-transfer on salary day so you save before you spend. Even ₹500/month in a recurring deposit adds up to ₹6,000+ per year. 💰",
    'invest':    "For beginners, index mutual funds (Nifty 50 index funds) are perfect — diversified, low-cost, and historically return 12–14% annually. Start a SIP for as little as ₹100/month! 📈",
    'sip':       "A SIP (Systematic Investment Plan) lets you invest a fixed amount monthly in mutual funds. ₹2,000/month in a good index fund for 10 years at 12% returns = ₹4.5 lakhs! The magic of compounding! 🚀",
    'debt':      "Use the **Avalanche Method**: list all debts by interest rate, pay minimums on all, then throw every extra rupee at the highest-rate debt. Credit cards at 36% should be your first target! 🎯",
    'emergency': "Aim for 3–6 months of expenses in an emergency fund. A ₹25,000/month spender needs ₹75,000–₹1.5 lakh liquid savings. Keep it in a high-yield savings account, not invested. 🛡️",
    'credit':    "Pay your full credit card balance every month — never just the minimum! Your credit score improves with on-time, full payments. A good CIBIL score (750+) gets you better loan rates later. 💳",
    'fd':        "Fixed Deposits offer 6–7% guaranteed returns — safe but barely ahead of inflation (5%). Great for your emergency fund, but for wealth building you need equity exposure too! 🏦",
    'mutual':    "Mutual funds pool money from many investors and are managed professionally. For most beginners, a Nifty 50 index fund beats 80% of actively managed funds — and charges less! 🌐",
    'crypto':    "Crypto is highly speculative — prices can drop 70–80% in bear markets. If you want exposure, limit it to 5–10% of your portfolio max. Never invest money you can't afford to lose! ⚠️",
    'fire':      "FIRE (Financial Independence, Retire Early) means saving 50–70% of income and investing aggressively to retire early. The rule: 25x your annual expenses = your FIRE number! 🔥",
    'insurance': "Health insurance is non-negotiable — one hospitalisation can wipe out years of savings. Get a ₹5 lakh family floater policy (costs ~₹8–15k/year). Term life insurance if you have dependents. 🏥",
}

_DEFAULT_REPLY = (
    "Great financial question! Start with the basics: **track your income and expenses** "
    "for one month to understand your patterns. Then apply the 50/30/20 rule and automate "
    "your savings. 🤖💡\n\n"
    "Ask me about: budgeting, saving, investing, SIPs, debt, emergency funds, credit cards, or FIRE!"
)


def _keyword_fallback(message):
    msg = message.lower()
    for keyword, reply in _KEYWORD_RESPONSES.items():
        if keyword in msg:
            return reply
    return _DEFAULT_REPLY
