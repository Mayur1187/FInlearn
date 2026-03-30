"""
FinLiteracy – AI Mentor Service
Priority chain:
  1. Ollama    (local – primary, offline AI)
  2. Groq API  (LLaMA 3 – cloud fallback if GROQ_API_KEY set)
  3. Anthropic (Claude Haiku – if ANTHROPIC_API_KEY set)
  4. Smart rule-based fallback  ← always works, no API needed
"""

import os
import re
import requests

# ─── System Prompt ────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = (
    "You are FinBot, a friendly and knowledgeable financial literacy mentor "
    "for young Indian adults aged 18–25. You teach personal finance in "
    "simple, engaging language with concrete ₹ examples. "
    "Topics: budgeting (50/30/20 rule), saving, investing (SIPs, mutual funds, "
    "index funds, stocks, FD, bonds), debt management, emergency funds, "
    "credit scores (CIBIL), and financial independence (FIRE movement). "
    "Keep replies to 2–3 focused paragraphs. Use **bold** for key terms. "
    "Never recommend specific stocks or guarantee returns."
)


# ─── Ollama helpers ───────────────────────────────────────────────────────────

def get_ollama_status() -> dict:
    """
    Returns {'online': bool, 'models': [str], 'active_model': str}
    Used by /mentor/status endpoint to show live status in the UI.
    """
    base_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434').strip()
    try:
        resp = requests.get(f'{base_url}/api/tags', timeout=3)
        resp.raise_for_status()
        models = [m['name'] for m in resp.json().get('models', [])]
        active = _pick_model(models)
        return {'online': True, 'models': models, 'active_model': active, 'url': base_url}
    except Exception:
        return {'online': False, 'models': [], 'active_model': None, 'url': base_url}


def _pick_model(models: list) -> str:
    """Pick best available model from Ollama's model list."""
    if not models:
        return 'llama3'   # default attempt even if list is empty
    # Preference order
    preferred = ['llama3', 'llama3:latest', 'llama3:8b', 'llama3.2', 'mistral',
                 'gemma', 'phi3', 'qwen2', 'deepseek-r1', 'llama2']
    for p in preferred:
        for m in models:
            if m.lower().startswith(p):
                return m
    return models[0]   # use whatever is installed


# ─── Public entry point ───────────────────────────────────────────────────────

def call_ai_mentor(user_message: str, user_context: str = None) -> str:
    system = _SYSTEM_PROMPT
    if user_context:
        system += f"\n\nUser profile: {user_context}"

    # 1. Ollama (local – primary offline AI)
   
    # 2. Groq (cloud fallback – only if key set)
    groq_key = os.environ.get('GROQ_API_KEY', '').strip()
    if groq_key:
        reply = _call_groq(user_message, system, groq_key)
        if reply:
            return reply

    # 3. Anthropic Claude (cloud fallback – only if key set)
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '').strip()
    if anthropic_key:
        reply = _call_anthropic(user_message, system, anthropic_key)
        if reply:
            return reply

    # 4. Smart rule-based fallback (always works, no network needed)
    return _smart_fallback(user_message)


# ─── Provider: Groq ───────────────────────────────────────────────────────────

def _call_groq(message: str, system: str, api_key: str):
    try:
        resp = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            json={
                'model': 'llama3-8b-8192',
                'max_tokens': 500,
                'temperature': 0.7,
                'messages': [
                    {'role': 'system', 'content': system},
                    {'role': 'user',   'content': message},
                ],
            },
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json()['choices'][0]['message']['content'].strip()
    except Exception as exc:
        print(f"[AI Mentor] Groq error: {exc}")
        return None


# ─── Provider: Ollama ─────────────────────────────────────────────────────────

def _call_ollama(message: str, system: str, base_url: str):
    base = base_url.rstrip('/')
    # Auto-detect which model is available
    try:
        tag_resp = requests.get(f'{base}/api/tags', timeout=3)
        tag_resp.raise_for_status()
        models = [m['name'] for m in tag_resp.json().get('models', [])]
        model = _pick_model(models)
    except Exception:
        model = 'llama3'   # best-effort default

    # Try /api/chat first (Ollama >= 0.1.14)
    try:
        resp = requests.post(
            f'{base}/api/chat',
            json={
                'model': model,
                'stream': False,
                'options': {'temperature': 0.7, 'num_predict': 600},
                'messages': [
                    {'role': 'system', 'content': system},
                    {'role': 'user',   'content': message},
                ],
            },
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        # /api/chat returns {"message": {"role": "assistant", "content": "..."}}
        text = data.get('message', {}).get('content', '').strip()
        if text:
            print(f"[AI Mentor] Ollama ({model}) responded via /api/chat")
            return text
    except Exception as exc:
        print(f"[AI Mentor] Ollama /api/chat error: {exc}")

    # Fallback to /api/generate (older Ollama builds)
    try:
        prompt = f"<s>[INST] <<SYS>>\n{system}\n<</SYS>>\n\n{message} [/INST]"
        resp = requests.post(
            f'{base}/api/generate',
            json={
                'model': model,
                'prompt': prompt,
                'stream': False,
                'options': {'temperature': 0.7, 'num_predict': 600},
            },
            timeout=120,
        )
        resp.raise_for_status()
        text = resp.json().get('response', '').strip()
        if text:
            print(f"[AI Mentor] Ollama ({model}) responded via /api/generate")
            return text
    except Exception as exc:
        print(f"[AI Mentor] Ollama /api/generate error: {exc}")

    return None


# ─── Provider: Anthropic ──────────────────────────────────────────────────────

def _call_anthropic(message: str, system: str, api_key: str):
    try:
        resp = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json',
            },
            json={
                'model': 'claude-haiku-4-5-20251001',
                'max_tokens': 500,
                'system': system,
                'messages': [{'role': 'user', 'content': message}],
            },
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()['content'][0]['text'].strip()
    except Exception as exc:
        print(f"[AI Mentor] Anthropic error: {exc}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# Smart Rule-Based Fallback
# Scores every topic against the full message, picks the best match,
# then builds a direct, question-specific answer.
# ═══════════════════════════════════════════════════════════════════════════════

# Each topic has: keywords (scored by weight), a direct answer, and follow-up tips.
_TOPICS = [
    {
        'id': 'sip',
        'keywords': {
            'sip': 5, 'systematic investment': 5, 'monthly invest': 3,
            'start sip': 4, 'sip kaise': 4, 'how to sip': 4,
            'rupee cost': 3, 'auto invest': 2,
        },
        'answer': (
            "A **SIP (Systematic Investment Plan)** lets you invest a fixed amount every month automatically into a mutual fund — as low as ₹100/month. "
            "Here's exactly how to start:\n\n"
            "1️⃣ Open a free account on **Groww, Zerodha Coin, or Kuvera** (takes 10 minutes, just Aadhaar + PAN).\n"
            "2️⃣ Choose a **Nifty 50 index fund** (e.g. UTI Nifty 50 or Nippon Nifty 50). Low fees, broadly diversified.\n"
            "3️⃣ Set up a monthly auto-debit on salary day. Start with ₹500–₹1,000 and increase by 10% every year.\n\n"
            "The magic is **Rupee Cost Averaging** — you buy more units when prices are low and fewer when high, so your average cost stays low over time. "
            "₹2,000/month for 10 years at 12% grows to ~₹4.6 lakhs. Start today, not 'someday'. 🚀"
        ),
    },
    {
        'id': 'budget',
        'keywords': {
            'budget': 5, 'budgeting': 5, '50/30/20': 4, '50 30 20': 4,
            'track expense': 4, 'track money': 3, 'monthly budget': 4,
            'spend less': 3, 'manage money': 3, 'how to budget': 4,
            'where does money go': 3, 'salary manage': 3,
        },
        'answer': (
            "Budgeting is simply telling your money where to go instead of wondering where it went. "
            "The easiest starting framework is the **50/30/20 rule**:\n\n"
            "💰 **50% Needs** — rent, food, transport, utilities\n"
            "🎯 **30% Wants** — dining out, Netflix, shopping, travel\n"
            "📈 **20% Savings/Investments** — SIP, FD, emergency fund\n\n"
            "Practical step: For 30 days, track every single expense (use **Walnut** or **Money Manager** app, or just a notes app). "
            "Most people discover they're spending 40%+ on 'wants' without realising. "
            "Once you see the pattern, cutting ₹2,000–₹5,000/month becomes obvious. That's ₹24,000–₹60,000/year working for you instead. 📊"
        ),
    },
    {
        'id': 'emergency_fund',
        'keywords': {
            'emergency fund': 5, 'emergency': 4, 'rainy day': 3,
            'safety net': 3, 'liquid savings': 3, 'job loss': 3,
            'how much save': 3, 'hospital': 2, 'unexpected expense': 3,
        },
        'answer': (
            "An **emergency fund** is 3–6 months of your living expenses kept liquid (instantly accessible). "
            "It's your financial safety net before you do anything else — before SIPs, before stocks.\n\n"
            "If you spend ₹25,000/month → your target is **₹75,000–₹1,50,000**. "
            "Keep it in a **liquid mutual fund** (like Parag Parikh Liquid Fund) or a high-yield savings account — "
            "not a regular FD (locked in) and not invested in stocks (can crash when you need it most).\n\n"
            "Build it in steps: save ₹5,000–₹10,000/month until you hit your target. "
            "Once built, don't touch it except for genuine emergencies (job loss, medical, urgent repairs). "
            "This one fund prevents you from taking high-interest loans in a crisis. 🛡️"
        ),
    },
    {
        'id': 'investing_basics',
        'keywords': {
            'invest': 4, 'investing': 4, 'start invest': 5, 'how to invest': 5,
            'where to invest': 5, 'investment': 3, 'grow money': 4,
            'wealth': 3, 'returns': 3, 'beginner invest': 5,
            'first investment': 5, 'kahan invest': 4,
        },
        'answer': (
            "For a complete beginner, here's the **right order to invest**:\n\n"
            "1️⃣ **Emergency fund first** — 3 months expenses in a liquid fund (non-negotiable).\n"
            "2️⃣ **Clear high-interest debt** — Credit card at 36%? Paying it off = guaranteed 36% return.\n"
            "3️⃣ **Start a Nifty 50 index fund SIP** — ₹500+/month on Groww or Kuvera. Set it, forget it.\n"
            "4️⃣ **Add a PPFAS Flexi Cap or mid-cap fund** — once SIP is running smoothly.\n"
            "5️⃣ **Direct stocks only after 6+ months** — once you understand markets emotionally.\n\n"
            "The most important thing: **start with any amount today**. ₹500 invested at 22 beats ₹5,000 invested at 32 "
            "because compounding rewards time, not size. 📈"
        ),
    },
    {
        'id': 'mutual_funds',
        'keywords': {
            'mutual fund': 5, 'mf': 3, 'nav': 3, 'fund': 3,
            'index fund': 5, 'nifty 50': 4, 'large cap': 3,
            'mid cap': 3, 'small cap': 3, 'flexi cap': 3,
            'active fund': 3, 'passive fund': 3, 'expense ratio': 4,
        },
        'answer': (
            "**Mutual funds** pool money from thousands of investors and invest it in stocks, bonds, or both. "
            "Here's how to choose as a beginner:\n\n"
            "✅ **Start with Index Funds** — They simply track the Nifty 50 (India's top 50 companies). "
            "No fund manager guessing, expense ratio < 0.2%, historically 12–14% annual returns over 10+ years. "
            "Top picks: UTI Nifty 50 Direct, Nippon Nifty 50 Direct.\n\n"
            "❌ **Avoid actively managed funds initially** — 85% of them underperform the index over 10 years, "
            "yet charge 1–2% expense ratio. That 1% difference costs you lakhs over 20 years.\n\n"
            "Key tip: Always invest in **Direct plans** (not Regular plans). Direct plans have no distributor commission, "
            "giving you 0.5–1% higher returns annually. On Groww/Kuvera, all plans are Direct by default. 🌐"
        ),
    },
    {
        'id': 'stocks',
        'keywords': {
            'stock': 5, 'share': 4, 'equity': 4, 'zerodha': 3,
            'nse': 3, 'bse': 3, 'sensex': 3, 'demat': 4,
            'buy stock': 4, 'stock market': 4, 'trading': 3,
            'dividend': 3, 'ipo': 3,
        },
        'answer': (
            "**Stocks** mean owning a tiny piece of a company. When the company profits, your share value rises. "
            "Before buying your first stock:\n\n"
            "📋 **Prerequisites**: Have an emergency fund + at least 1 index fund SIP already running. "
            "Open a **Demat account** on Zerodha (₹300 one-time) or Groww (free).\n\n"
            "🎯 **Beginner approach**: Don't pick individual stocks yet. Start with **Nifty Bees or Nifty 50 ETF** "
            "— trades like a stock, diversified like a fund. Once comfortable, research companies for 3+ months "
            "before buying (read annual reports, understand their business).\n\n"
            "⚠️ **Golden rule**: Never invest money you'll need in the next 3 years. "
            "Stock prices can fall 40–50% in a crash (2008, 2020) — only long-term money belongs here. "
            "If a 30% drop would make you panic-sell, stick to index funds for now. 📊"
        ),
    },
    {
        'id': 'debt',
        'keywords': {
            'debt': 5, 'loan': 4, 'credit card': 5, 'emi': 4,
            'pay off': 4, 'interest': 3, 'personal loan': 4,
            'avalanche': 3, 'snowball': 3, 'borrow': 3,
            'owe': 3, 'outstanding': 3, 'minimum payment': 4,
        },
        'answer': (
            "Carrying debt — especially credit card debt at **36% annual interest** — is like running with a parachute. "
            "Here's how to eliminate it fast:\n\n"
            "🎯 **Avalanche Method** (mathematically optimal):\n"
            "List all debts by interest rate (highest first). Pay the minimum on all of them, "
            "then throw every extra rupee at the highest-rate debt. Once it's gone, roll that payment to the next.\n\n"
            "Example: ₹50,000 credit card (36%) + ₹2,00,000 personal loan (18%).\n"
            "→ Pay minimum on personal loan, attack the credit card first. It saves you more in interest.\n\n"
            "One rule: **Never pay just the minimum on a credit card.** Minimum payments are designed to keep you in debt for years. "
            "A ₹10,000 balance at 3% monthly interest with minimum payments can take 5+ years to clear. "
            "Always pay the full outstanding amount every month if possible. 💳"
        ),
    },
    {
        'id': 'fd_bonds',
        'keywords': {
            'fixed deposit': 5, 'fd': 4, 'bond': 5, 'g-sec': 4,
            'government bond': 4, 'corporate bond': 4, 'rbi bond': 4,
            'guaranteed return': 3, 'safe investment': 3, 'interest rate': 3,
            'post office': 3, 'ppf': 4, 'nsc': 3,
        },
        'answer': (
            "**Fixed Deposits (FDs)** and **Bonds** are fixed-income instruments — you lend money and get guaranteed interest back.\n\n"
            "🏦 **FD** — Bank FDs currently offer 6.5–8% p.a. (small finance banks like AU, IDFC offer higher). "
            "Fully safe up to ₹5 lakh per bank (DICGC insurance). Best use: emergency fund, goals within 1–2 years.\n\n"
            "🏛️ **Bonds** — Government bonds (G-Secs) offer 7–8% and are the safest fixed-income option. "
            "Buy them on **RBI Retail Direct** (rbidirect.org.in) with no intermediary. "
            "Corporate bonds offer 9–12% but carry company default risk — research the credit rating (AAA is safest).\n\n"
            "⚠️ **The inflation problem**: India's inflation runs at 5–6%. An FD at 6.5% gives you only ~1.5% real return. "
            "FDs are great for safety and short goals, but for long-term wealth you need equity (mutual funds/stocks). "
            "Don't park all your money in FDs — your purchasing power erodes over 10–20 years. 🏦"
        ),
    },
    {
        'id': 'credit_score',
        'keywords': {
            'credit score': 5, 'cibil': 5, 'cibil score': 5,
            'improve credit': 4, 'credit report': 4, 'credit history': 4,
            'credit rating': 3, 'loan eligibility': 3,
        },
        'answer': (
            "Your **CIBIL score** (300–900) is your financial reputation — it determines whether banks give you loans and at what rate. "
            "750+ is considered excellent. Here's how to build or fix it:\n\n"
            "✅ **What helps your score**:\n"
            "• Pay your full credit card bill every month (on-time, full payment = biggest positive factor)\n"
            "• Keep credit utilisation below 30% (if your limit is ₹1 lakh, spend max ₹30,000)\n"
            "• Don't close old credit cards — long credit history helps\n"
            "• Avoid applying for multiple loans/cards in short time (hard inquiries hurt score)\n\n"
            "❌ **What destroys your score**: Missed EMIs, defaulting on loans, credit card minimum-only payments.\n\n"
            "Check your score free on **CIBIL.com, Paisabazaar, or BankBazaar** (one free check/year officially, "
            "but aggregator sites let you check anytime). A score of 750+ can save you 1–2% on home loan interest — "
            "that's lakhs of rupees over 20 years. 💳"
        ),
    },
    {
        'id': 'fire',
        'keywords': {
            'fire': 4, 'financial independence': 5, 'retire early': 5,
            'retire': 3, 'early retirement': 5, 'fi': 3,
            'passive income': 4, 'financial freedom': 4,
            '4% rule': 4, 'corpus': 3,
        },
        'answer': (
            "**FIRE** (Financial Independence, Retire Early) is about reaching a point where your investments generate enough passive income to cover your expenses — forever.\n\n"
            "📐 **The FIRE number formula**: Your FIRE corpus = **Annual expenses × 25**\n"
            "If you spend ₹6 lakh/year → FIRE number = ₹1.5 crore\n"
            "At this corpus, you can withdraw 4% annually and your portfolio replenishes itself from returns.\n\n"
            "🔥 **Lean FIRE** (frugal lifestyle, smaller corpus) vs **Fat FIRE** (comfortable lifestyle, larger corpus).\n\n"
            "How to get there: Save and invest 40–60% of your income, primarily in equity index funds. "
            "At a 60% savings rate, you can reach FIRE in ~12 years from zero. At 20%, it takes ~37 years. "
            "The lever isn't your income — it's your **savings rate**. "
            "Track your net worth monthly and watch your 'years to FIRE' countdown. 🔥"
        ),
    },
    {
        'id': 'insurance',
        'keywords': {
            'insurance': 5, 'term insurance': 5, 'life insurance': 4,
            'health insurance': 5, 'mediclaim': 4, 'cover': 3,
            'policy': 3, 'premium': 3, 'claim': 3, 'hospital': 2,
        },
        'answer': (
            "Insurance is not an investment — it's **protection**. The two non-negotiables:\n\n"
            "🏥 **Health Insurance** (most urgent)\n"
            "Get a ₹5–10 lakh individual/family floater policy. One hospitalisation without coverage can wipe out years of savings. "
            "Look at **Care Health, Niva Bupa, or Star Health**. Annual premium: ~₹8,000–₹20,000 for ₹10 lakh cover. "
            "Don't rely only on employer insurance — you lose it if you switch jobs.\n\n"
            "🛡️ **Term Life Insurance** (if anyone depends on your income)\n"
            "Pure term plan — no investment component (avoid ULIPs and endowment plans, they're expensive and low-return). "
            "₹1 crore cover costs ~₹8,000–₹12,000/year for a 25-year-old. Buy from **LIC, HDFC Life, or ICICI Prudential**.\n\n"
            "Rule of thumb: Never mix insurance and investment. Buy cheap term insurance for protection, invest separately in index funds. "
            "Anyone pushing 'insurance + investment' plans is usually earning a high commission. 🏥"
        ),
    },
    {
        'id': 'saving',
        'keywords': {
            'save': 4, 'saving': 4, 'savings': 4, 'save money': 5,
            'how to save': 5, 'save more': 5, 'spend less': 4,
            'cut expense': 4, 'frugal': 3, 'no spend': 3,
        },
        'answer': (
            "The single most powerful saving trick: **pay yourself first**. Don't save what's left after spending — spend what's left after saving.\n\n"
            "⚙️ **Automate it**: Set up an auto-transfer to a savings/investment account on the day your salary arrives. "
            "If you never see the money in your current account, you won't miss it.\n\n"
            "💡 **High-impact places to cut**:\n"
            "• Subscriptions audit (Netflix, Spotify, gym, apps) — cancel what you haven't used in 2 months\n"
            "• Food delivery (Swiggy/Zomato) — cooking just 4 extra days/week saves ₹800–₹2,000/month\n"
            "• Impulsive online shopping — add to cart, wait 48 hours. 80% of the time you won't buy it\n\n"
            "Target: Save at least 20% of take-home salary. Even ₹2,000/month in a liquid fund earning 7% = ₹3.5 lakh in 10 years before adding any investment returns. 💰"
        ),
    },
    {
        'id': 'compounding',
        'keywords': {
            'compound': 5, 'compounding': 5, 'compound interest': 5,
            'power of compounding': 5, 'interest on interest': 4,
            'double money': 3, 'rule of 72': 4,
        },
        'answer': (
            "**Compounding** is earning returns on your returns — making your money grow exponentially, not linearly.\n\n"
            "📐 **Rule of 72**: Divide 72 by your annual return rate to find how many years to double your money.\n"
            "• FD at 7% → doubles in 72/7 = **~10.3 years**\n"
            "• Index fund at 12% → doubles in 72/12 = **6 years**\n"
            "• Credit card debt at 36% → your debt doubles in 72/36 = **2 years** (this is why debt is dangerous!)\n\n"
            "The compounding timeline:\n"
            "₹10,000 invested at 12% per year:\n"
            "• After 10 years: ₹31,058\n"
            "• After 20 years: ₹96,463\n"
            "• After 30 years: ₹2,99,599\n\n"
            "The jump from year 20 to 30 is bigger than the entire first 20 years combined — that's why **starting early matters more than the amount**. "
            "Starting at 22 vs 32 can mean a 3× difference in final wealth at retirement. ⚡"
        ),
    },
    {
        'id': 'tax',
        'keywords': {
            'tax': 5, 'income tax': 5, 'tax saving': 5, '80c': 5,
            'elss': 4, 'nps': 4, 'ppf': 3, 'itr': 4,
            'tds': 4, 'tax slab': 4, 'new tax regime': 4,
            'old tax regime': 4, 'deduction': 4,
        },
        'answer': (
            "Smart tax planning is legal, ethical, and can save you **₹15,000–₹60,000/year**. Key sections:\n\n"
            "📋 **Section 80C** (up to ₹1.5 lakh deduction):\n"
            "Best options: **ELSS mutual funds** (3-year lock-in, equity returns ~12%), PPF (15-year, 7.1% tax-free), NPS (additional ₹50,000 under 80CCD(1B)).\n"
            "Avoid: LIC endowment plans and ULIPs — high charges, low returns.\n\n"
            "🏥 **Section 80D**: Health insurance premiums deductible up to ₹25,000 (₹50,000 for senior citizen parents).\n\n"
            "📊 **New vs Old regime**: New regime has lower slab rates but fewer deductions. "
            "Old regime is better if you have large 80C investments, home loan, and HRA. "
            "Calculate both before filing. Most salaried employees with ₹80C investments benefit from old regime up to ~₹12–15 lakh income.\n\n"
            "File your ITR by July 31 every year. Use ClearTax or Tax2Win for guided filing. 🏛️"
        ),
    },
]


def _score_message(message: str, keywords: dict) -> int:
    """Sum weights of keywords found in message."""
    msg = message.lower()
    score = 0
    for kw, weight in keywords.items():
        if kw in msg:
            score += weight
    return score


def _smart_fallback(user_message: str) -> str:
    """
    Score every topic against the user message and return the best-matching answer.
    Falls back to a helpful generic response only if nothing scores above zero.
    """
    best_score = 0
    best_topic = None

    for topic in _TOPICS:
        score = _score_message(user_message, topic['keywords'])
        if score > best_score:
            best_score = score
            best_topic = topic

    if best_topic and best_score >= 2:
        return best_topic['answer']

    # ── Partial match: at least one keyword hit ──
    if best_topic and best_score == 1:
        return best_topic['answer']

    # ── Nothing matched — still give a useful response ──
    return _contextual_default(user_message)


def _contextual_default(message: str) -> str:
    """Generate a helpful reply even when no topic matched."""
    msg = message.lower()

    # Detect question words to give a more helpful prompt
    if any(w in msg for w in ['how', 'what', 'why', 'when', 'should', 'can i', 'kaise', 'kya']):
        return (
            "Great question! 🤖 I'm FinBot, your financial literacy mentor. "
            "I can give you detailed answers on these money topics:\n\n"
            "💰 **Budgeting** — 50/30/20 rule, tracking expenses\n"
            "🏦 **Saving** — automating savings, high-yield accounts\n"
            "📈 **Investing** — SIPs, mutual funds, index funds, stocks\n"
            "💳 **Debt** — credit card payoff, EMIs, avalanche method\n"
            "🛡️ **Emergency Fund** — how much, where to keep it\n"
            "📊 **CIBIL Score** — how to build and improve it\n"
            "🏥 **Insurance** — term + health insurance essentials\n"
            "🔥 **FIRE** — financial independence, early retirement\n"
            "🏛️ **Tax Saving** — 80C, ELSS, NPS deductions\n\n"
            "Try asking something specific like: *'How do I start a SIP?'* or *'How do I improve my CIBIL score?'*"
        )

    return (
        "I'm FinBot, your personal finance guide! 💡 Here are some topics I can help with:\n\n"
        "Ask me: *'How do I start investing?'*, *'What is a SIP?'*, *'How to pay off debt fast?'*, "
        "*'How much emergency fund do I need?'*, or *'How to save on taxes?'*\n\n"
        "I give clear, actionable answers with real ₹ examples tailored for young Indian adults. 🚀"
    )
