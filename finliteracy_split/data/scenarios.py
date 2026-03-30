"""
FinLiteracy – Scenario Catalog
All scenario definitions with choices, XP rewards, and educational messages.
"""

SCENARIO_CATALOG = [
    {
        'slug': 'monthly_allowance',
        'title': 'Monthly Allowance Challenge',
        'description': 'You just received ₹10,000 as your monthly allowance. Bills are covered. How do you allocate the surplus?',
        'category': 'budgeting',
        'difficulty': 'easy',
        'xp_reward': 200,
        'coins_reward': 60,
        'avatar_emoji': '💼',
        'choices': [
            {'key': 'lifestyle', 'label': 'Spend on Lifestyle',      'icon': '🛍️', 'desc': 'Entertainment, clothes, dining out',       'xp': 30,  'coins': 10, 'score_delta': -5,  'msg': '⚠️ Spending everything on lifestyle leaves zero buffer. Balance is key — enjoy life AND save!'},
            {'key': 'save',      'label': 'Save for the Future',     'icon': '🏦', 'desc': 'Put 30%+ into savings for goals',           'xp': 150, 'coins': 50, 'score_delta': 10,  'msg': '🎯 Smart move! Saving first ensures you meet your goals before spending on wants.'},
            {'key': 'invest',    'label': 'Start Investing',         'icon': '📈', 'desc': 'SIP in mutual funds or index funds',        'xp': 200, 'coins': 75, 'score_delta': 15,  'msg': '📈 Excellent! Investing grows wealth over time. Even ₹500/month in a SIP can build crores.'},
            {'key': 'emergency', 'label': 'Build Emergency Fund',    'icon': '🛡️', 'desc': 'Save 3–6 months of expenses as safety net', 'xp': 120, 'coins': 40, 'score_delta': 8,   'msg': '🛡️ Wise! An emergency fund protects you from unexpected shocks without going into debt.'},
        ],
    },
    {
        'slug': 'emergency_medical',
        'title': 'Emergency Medical Expense',
        'description': 'Your parent needs an urgent surgery costing ₹50,000. You have ₹20,000 saved. What do you do?',
        'category': 'saving',
        'difficulty': 'hard',
        'xp_reward': 250,
        'coins_reward': 80,
        'avatar_emoji': '🏥',
        'choices': [
            {'key': 'insurance', 'label': 'Claim Health Insurance',    'icon': '📋', 'desc': 'File a claim on your health policy',    'xp': 220, 'coins': 80, 'score_delta': 18, 'msg': '🏆 Perfect! Health insurance is exactly for this. Always maintain adequate family coverage.'},
            {'key': 'loan',      'label': 'Personal Loan from Bank',   'icon': '🏦', 'desc': 'Apply for a quick personal loan',       'xp': 120, 'coins': 40, 'score_delta': 5,  'msg': '✅ Acceptable if unavoidable. Compare interest rates carefully — personal loans can be 12–18% p.a.'},
            {'key': 'credit',    'label': 'Swipe Credit Card',         'icon': '💳', 'desc': 'Use credit card, pay EMI later',        'xp': 60,  'coins': 20, 'score_delta': -3, 'msg': '⚠️ Credit cards at 36–42% annual interest for revolving credit. Only use if you can pay in full next month.'},
            {'key': 'borrow',    'label': 'Borrow from Friends/Family','icon': '🤝', 'desc': 'Request an informal loan with repayment','xp': 100, 'coins': 35, 'score_delta': 3,  'msg': '👍 Okay option. Treat it formally — write down repayment terms to preserve the relationship.'},
        ],
    },
    {
        'slug': 'credit_card_debt',
        'title': 'Credit Card Debt Trap',
        'description': 'You owe ₹30,000 on your credit card at 36% annual interest. You have ₹8,000/month free after expenses. Strategy?',
        'category': 'debt',
        'difficulty': 'hard',
        'xp_reward': 280,
        'coins_reward': 90,
        'avatar_emoji': '💳',
        'choices': [
            {'key': 'minimum',   'label': 'Pay Only Minimums',           'icon': '😰', 'desc': 'Pay ₹900/month minimum payment',        'xp': 20,  'coins': 5,  'score_delta': -15, 'msg': "❌ Danger zone! Minimum payments barely cover interest. You'll owe MORE in 12 months. Never do this!"},
            {'key': 'avalanche', 'label': 'Avalanche Method',            'icon': '🏔️', 'desc': 'Attack highest-interest debt first',    'xp': 280, 'coins': 90, 'score_delta': 20,  'msg': '🏆 Optimal! Avalanche method saves the most money. Pay maximums on the highest-rate debt first.'},
            {'key': 'balance',   'label': 'Balance Transfer',            'icon': '🔄', 'desc': 'Transfer to 0% introductory card',     'xp': 200, 'coins': 65, 'score_delta': 15,  'msg': '✅ Smart if done right! Zero-interest transfers can save thousands — but watch the transfer fee and end-date.'},
            {'key': 'personal',  'label': 'Personal Loan Consolidation', 'icon': '🏦', 'desc': 'Take 12% personal loan to clear 36% CC', 'xp': 180, 'coins': 55, 'score_delta': 12, 'msg': '👍 Good thinking! Reducing from 36% to 12% interest cuts your cost significantly. Clear it aggressively.'},
        ],
    },
    {
        'slug': 'investment_choice',
        'title': 'Where to Invest ₹1 Lakh?',
        'description': "You have ₹1,00,000 to invest for 5 years. You're 22 years old with a stable income. What's your approach?",
        'category': 'investing',
        'difficulty': 'medium',
        'xp_reward': 260,
        'coins_reward': 85,
        'avatar_emoji': '📊',
        'choices': [
            {'key': 'all_fd',    'label': 'All in Fixed Deposit',  'icon': '🏦', 'desc': '6% guaranteed returns, fully safe',    'xp': 80,  'coins': 30, 'score_delta': 2,   'msg': '😐 Safe but sub-optimal for a 22-year-old. FD returns (6%) barely beat inflation (5%). You need growth.'},
            {'key': 'diversify', 'label': 'Diversified Portfolio', 'icon': '🌐', 'desc': '60% MF + 20% FD + 20% stocks',       'xp': 260, 'coins': 85, 'score_delta': 22,  'msg': '🏆 Textbook perfect! Diversification balances risk and reward. At 22, you can afford equity exposure for growth.'},
            {'key': 'all_crypto','label': 'All into Crypto',       'icon': '🎲', 'desc': 'High risk, potential moonshot',        'xp': 30,  'coins': 10, 'score_delta': -10, 'msg': '⚠️ Never put all eggs in one basket — especially volatile crypto. Limit speculative assets to 5–10% max.'},
            {'key': 'stocks',    'label': 'Direct Equity (Stocks)','icon': '📈', 'desc': 'Research and buy individual stocks',   'xp': 160, 'coins': 55, 'score_delta': 10,  'msg': '✅ Good but risky for beginners. Start with index funds/ETFs before individual stocks to learn without high risk.'},
        ],
    },
    {
        'slug': 'shopping_temptation',
        'title': 'Flash Sale Temptation',
        'description': "It's a 24-hour Diwali sale. You want a new phone (₹25,000) but you don't have the budget. You just got ₹20,000 earmarked for rent next month.",
        'category': 'budgeting',
        'difficulty': 'medium',
        'xp_reward': 180,
        'coins_reward': 55,
        'avatar_emoji': '📱',
        'choices': [
            {'key': 'buy_emi',  'label': 'Buy on No-Cost EMI',             'icon': '📱', 'desc': 'Split ₹25,000 over 6 months "free"',   'xp': 60,  'coins': 20, 'score_delta': -5,  'msg': '⚠️ "No-cost" EMIs often have hidden processing fees. Also — borrowing for depreciating assets is a trap.'},
            {'key': 'skip',     'label': 'Skip & Save for it',             'icon': '⏳', 'desc': 'Save ₹4,000/month and buy in 6 months', 'xp': 180, 'coins': 55, 'score_delta': 15,  'msg': "🏆 Excellent patience! Delayed gratification is a superpower. Save up, then pay cash. You'll feel amazing."},
            {'key': 'credit',   'label': 'Buy on Credit Card',             'icon': '💳', 'desc': 'YOLO — treat yourself, pay later',       'xp': 20,  'coins': 5,  'score_delta': -12, 'msg': '❌ Using rent money for a phone is a financial emergency recipe. This WILL cause a debt spiral.'},
            {'key': 'research', 'label': 'Research & Wait for Better Deal','icon': '🔍', 'desc': 'Compare, wait for refurbished or deal',  'xp': 150, 'coins': 45, 'score_delta': 10,  'msg': '✅ Smart! Patience + research often saves 15–30%. Refurbished flagships offer great value too.'},
        ],
    },
]


def get_scenario_by_slug(slug):
    """Return the full scenario dict (including choices) for a given slug."""
    return next((s for s in SCENARIO_CATALOG if s['slug'] == slug), None)
