"""
FinLiteracy – Learning Path Content
All topic content, steps, and quiz questions for each level.

Structure:
  LEVELS → list of level dicts, each with:
    - id, slug, title, icon, xp_reward, prerequisite (slug of prior level)
    - topics: list of topic dicts, each with:
        - id, slug, title, icon
        - steps: list of step dicts (title, body HTML)
    - quiz: list of 10 question dicts (question, options A-D, correct, explanation)
"""

LEVELS = [
    # ══════════════════════════════════════════════════════
    # LEVEL 1 — BUDGETING BASICS
    # ══════════════════════════════════════════════════════
    {
        'id': 1,
        'slug': 'budgeting',
        'title': 'Budgeting Basics',
        'icon': '💰',
        'desc': 'Learn to track income vs expenses, apply the 50/30/20 rule, and build your first monthly budget.',
        'xp_reward': 300,
        'coins_reward': 60,
        'prerequisite': None,
        'level_field': 'budgeting_level',
        'topics': [
            {
                'id': 'b1',
                'slug': 'income-expenses',
                'title': 'Income & Expenses',
                'icon': '📋',
                'steps': [
                    {
                        'title': 'What is Income?',
                        'body': """
<p><strong>Income</strong> is all the money that flows <em>into</em> your hands. For most people your age, this includes:</p>
<ul>
  <li>💼 <strong>Salary / Stipend</strong> — your primary take-home pay after TDS</li>
  <li>💻 <strong>Freelance / Gig income</strong> — from Fiverr, Upwork, Swiggy delivery, tutoring</li>
  <li>🎁 <strong>Family allowance</strong> — pocket money or parental support</li>
  <li>🏦 <strong>Interest income</strong> — from savings accounts or FDs</li>
</ul>
<p>Always use your <strong>net income</strong> (after taxes and PF deductions) when making a budget — never gross.</p>
<div class="tip-box">💡 <strong>Pro tip:</strong> If your income varies month to month, use your 3-month average as your budget baseline.</div>
"""
                    },
                    {
                        'title': 'What are Expenses?',
                        'body': """
<p><strong>Expenses</strong> are everything you spend money on. They fall into two buckets:</p>
<div class="two-col">
  <div class="col-box">
    <h4>🔒 Fixed Expenses</h4>
    <p>Same amount every month. Hard to change quickly.</p>
    <ul>
      <li>Rent / EMI</li>
      <li>Phone bill</li>
      <li>Streaming subscriptions</li>
      <li>Insurance premium</li>
    </ul>
  </div>
  <div class="col-box">
    <h4>🔄 Variable Expenses</h4>
    <p>Changes month to month. This is where you can cut.</p>
    <ul>
      <li>Food / groceries</li>
      <li>Transport / Ola/Uber</li>
      <li>Dining / Zomato / Swiggy</li>
      <li>Clothing, entertainment</li>
    </ul>
  </div>
</div>
<div class="tip-box">💡 Track every expense for 30 days. Most people are shocked — they spend 30-40% more than they think.</div>
"""
                    },
                    {
                        'title': 'Calculate Your Net Cash Flow',
                        'body': """
<p>The most important number in your financial life:</p>
<div class="formula-box">
  <strong>Net Cash Flow = Total Income − Total Expenses</strong>
</div>
<p>Three possible outcomes:</p>
<ul>
  <li>✅ <strong>Positive cash flow</strong> → You're saving money. Well done!</li>
  <li>⚠️ <strong>Zero</strong> → You're living paycheck to paycheck. Risky.</li>
  <li>❌ <strong>Negative cash flow</strong> → You're going into debt every month. Urgent action needed.</li>
</ul>
<p>Example: Rohan earns ₹35,000/month after TDS. He spends ₹28,000. His net cash flow = <strong>+₹7,000</strong>. That ₹7,000 should be saved/invested — not spent.</p>
<div class="tip-box">💡 <strong>Goal:</strong> Aim for at least 20% of your income as positive cash flow.</div>
"""
                    },
                ],
            },
            {
                'id': 'b2',
                'slug': '50-30-20-rule',
                'title': '50/30/20 Rule',
                'icon': '📊',
                'steps': [
                    {
                        'title': 'What is the 50/30/20 Rule?',
                        'body': """
<p>The <strong>50/30/20 Rule</strong> is the most popular budgeting framework in the world. It was popularised by Senator Elizabeth Warren.</p>
<p>It divides your <strong>net take-home income</strong> into three buckets:</p>
<div class="three-col">
  <div class="col-box col-blue">
    <div style="font-size:2rem">50%</div>
    <h4>Needs</h4>
    <p>Things you cannot live without</p>
  </div>
  <div class="col-box col-orange">
    <div style="font-size:2rem">30%</div>
    <h4>Wants</h4>
    <p>Nice-to-haves and lifestyle</p>
  </div>
  <div class="col-box col-green">
    <div style="font-size:2rem">20%</div>
    <h4>Savings & Debt</h4>
    <p>Future you will thank you</p>
  </div>
</div>
"""
                    },
                    {
                        'title': 'Breaking Down Each Bucket',
                        'body': """
<h4>50% — Needs</h4>
<ul>
  <li>Rent / home loan EMI</li>
  <li>Groceries and utilities</li>
  <li>Transport to work</li>
  <li>Health insurance premium</li>
  <li>Minimum debt payments</li>
</ul>
<h4>30% — Wants</h4>
<ul>
  <li>Dining out / Zomato / Swiggy</li>
  <li>Movies, OTT subscriptions (Netflix, Prime)</li>
  <li>Gym membership, hobbies</li>
  <li>New clothes, gadgets</li>
</ul>
<h4>20% — Savings & Investments</h4>
<ul>
  <li>Emergency fund contributions</li>
  <li>SIP investments</li>
  <li>Paying off extra debt</li>
  <li>Goal-based savings (vacation, laptop)</li>
</ul>
<div class="tip-box">💡 In India's high-expense cities like Mumbai/Bangalore, 50% for needs might be hard. If rent alone is 40%, cut wants to 15-20% to preserve the savings bucket.</div>
"""
                    },
                    {
                        'title': 'Real Example with ₹ Numbers',
                        'body': """
<p>Priya earns ₹40,000/month take-home. Here's her 50/30/20 budget:</p>
<div class="budget-table">
  <div class="bt-row bt-header"><span>Category</span><span>%</span><span>Amount</span></div>
  <div class="bt-row bt-need"><span>🏠 Rent</span><span>—</span><span>₹12,000</span></div>
  <div class="bt-row bt-need"><span>🛒 Groceries</span><span>—</span><span>₹5,000</span></div>
  <div class="bt-row bt-need"><span>🚌 Transport</span><span>—</span><span>₹2,000</span></div>
  <div class="bt-row bt-need bt-subtotal"><span><strong>Needs Total</strong></span><span>47.5%</span><span><strong>₹19,000</strong></span></div>
  <div class="bt-row bt-want"><span>🍕 Dining out</span><span>—</span><span>₹4,000</span></div>
  <div class="bt-row bt-want"><span>📺 OTT + Phone</span><span>—</span><span>₹2,000</span></div>
  <div class="bt-row bt-want"><span>👗 Shopping</span><span>—</span><span>₹3,000</span></div>
  <div class="bt-row bt-want bt-subtotal"><span><strong>Wants Total</strong></span><span>22.5%</span><span><strong>₹9,000</strong></span></div>
  <div class="bt-row bt-save"><span>📈 SIP Investment</span><span>—</span><span>₹6,000</span></div>
  <div class="bt-row bt-save"><span>🛡️ Emergency Fund</span><span>—</span><span>₹2,000</span></div>
  <div class="bt-row bt-save bt-subtotal"><span><strong>Savings Total</strong></span><span>30%</span><span><strong>₹12,000</strong></span></div>
</div>
<div class="tip-box">✅ Priya is actually saving more than 20% — great! She freed up budget by limiting dining to ₹4k/month.</div>
"""
                    },
                ],
            },
            {
                'id': 'b3',
                'slug': 'monthly-budget',
                'title': 'Build Your Monthly Budget',
                'icon': '🗓️',
                'steps': [
                    {
                        'title': 'Step-by-Step Budget Creation',
                        'body': """
<p>Building a budget takes 15 minutes. Here's exactly how:</p>
<ol>
  <li><strong>List all income sources</strong> — salary, freelance, allowance. Add them up.</li>
  <li><strong>List fixed expenses</strong> — rent, EMIs, subscriptions. These go first.</li>
  <li><strong>Estimate variable expenses</strong> — food, transport, entertainment.</li>
  <li><strong>Subtract everything from income</strong> — what's left is your savings capacity.</li>
  <li><strong>Assign the savings</strong> — SIP, emergency fund, goals. Don't leave it unassigned!</li>
</ol>
<div class="tip-box">💡 <strong>The golden rule:</strong> Budget on paper <em>before</em> the month starts, not after it ends. A budget written on the 1st of the month is 3× more effective than reviewing spending on the 30th.</div>
"""
                    },
                    {
                        'title': 'Envelope Method (Zero-Based Budgeting)',
                        'body': """
<p>Zero-based budgeting means every rupee gets a <em>job</em>:</p>
<div class="formula-box">Income − All Budgeted Expenses − All Savings = ₹0</div>
<p>The classic way: <strong>cash envelopes</strong>. Label envelopes for each category (groceries, transport, fun money). Put cash in each at the start of the month. When the envelope is empty — you're done spending in that category.</p>
<p>Modern digital version: use separate savings accounts or UPI spending limits per category.</p>
<div class="tip-box">💡 Studies show people spend 12-18% less when using cash/envelopes vs cards because spending <em>feels real</em>.</div>
"""
                    },
                    {
                        'title': 'Tracking & Adjusting',
                        'body': """
<p>A budget is a living document. Review it weekly:</p>
<ul>
  <li>📱 <strong>Apps:</strong> Walnut (India-specific, auto-reads SMS), Money Manager, Spendee</li>
  <li>📊 <strong>Spreadsheet:</strong> Google Sheets — free template, full control</li>
  <li>🗒️ <strong>Notebook:</strong> Low-tech but surprisingly effective</li>
</ul>
<p>Every 3 months, do a <strong>budget audit</strong>:</p>
<ul>
  <li>Which categories consistently go over? Find out why.</li>
  <li>Are you hitting your savings targets?</li>
  <li>Has your income changed? Update the budget.</li>
</ul>
<div class="tip-box">🎯 <strong>30-day challenge:</strong> Track every single rupee you spend for one month. No judgement — just data. You'll find at least ₹2,000-3,000 you can redirect to savings.</div>
"""
                    },
                ],
            },
            {
                'id': 'b4',
                'slug': 'budget-apps',
                'title': 'Budget Apps & Tools',
                'icon': '📱',
                'steps': [
                    {
                        'title': 'Best Budget Apps for India',
                        'body': """
<p>These apps are designed for Indian users and work with UPI/SMS:</p>
<div class="app-cards">
  <div class="app-card">
    <div class="app-icon">🌰</div>
    <div class="app-name">Walnut</div>
    <div class="app-desc">Auto-reads bank SMS to track spending. Shows merchant-wise analytics. Free.</div>
  </div>
  <div class="app-card">
    <div class="app-icon">💹</div>
    <div class="app-name">Money Manager</div>
    <div class="app-desc">Manual entry, beautiful charts, export to Excel. Best for detail-oriented people.</div>
  </div>
  <div class="app-card">
    <div class="app-icon">🏦</div>
    <div class="app-name">Fi Money</div>
    <div class="app-desc">Neo-bank + budgeting. Automated savings jars, spending insights built in.</div>
  </div>
</div>
"""
                    },
                    {
                        'title': 'Using Google Sheets as a Budget',
                        'body': """
<p>A simple Google Sheets budget is often better than any app — you control it completely.</p>
<p><strong>Columns you need:</strong></p>
<div class="table-simple">
  <div class="ts-row ts-head"><span>Date</span><span>Category</span><span>Description</span><span>Amount</span><span>Type</span></div>
  <div class="ts-row"><span>01 Jan</span><span>Salary</span><span>Jan Salary</span><span>₹35,000</span><span>IN</span></div>
  <div class="ts-row"><span>02 Jan</span><span>Rent</span><span>Flat rent</span><span>₹10,000</span><span>OUT</span></div>
  <div class="ts-row"><span>05 Jan</span><span>Food</span><span>Zomato</span><span>₹350</span><span>OUT</span></div>
</div>
<p>Then use <code>=SUMIF(E:E,"OUT",D:D)</code> to total expenses and <code>=SUMIF(E:E,"IN",D:D)</code> to total income.</p>
<div class="tip-box">💡 Search "Personal Budget Template India" in Google Sheets template gallery — there are excellent free templates.</div>
"""
                    },
                ],
            },
        ],
        'quiz': [
            {
                'q': 'The 50/30/20 rule divides net income into needs, wants, and savings. What percentage goes to savings?',
                'options': {'A': '10%', 'B': '20%', 'C': '30%', 'D': '50%'},
                'correct': 'B',
                'explanation': 'The 50/30/20 rule allocates 50% to needs, 30% to wants, and 20% to savings and investments.'
            },
            {
                'q': 'Rohan earns ₹30,000/month. He spends ₹28,000. What is his monthly net cash flow?',
                'options': {'A': '−₹2,000', 'B': '₹58,000', 'C': '+₹2,000', 'D': '₹0'},
                'correct': 'C',
                'explanation': 'Net cash flow = Income − Expenses = ₹30,000 − ₹28,000 = +₹2,000. Positive means he is saving money.'
            },
            {
                'q': 'Which of the following is a FIXED expense?',
                'options': {'A': 'Zomato order', 'B': 'Monthly rent', 'C': 'Weekend shopping', 'D': 'Auto-rickshaw fare'},
                'correct': 'B',
                'explanation': 'Rent is a fixed expense — same amount every month. Zomato, shopping, and transport fares are variable.'
            },
            {
                'q': 'What does "zero-based budgeting" mean?',
                'options': {
                    'A': 'Having zero money in your account',
                    'B': 'Every rupee of income is assigned to a specific category',
                    'C': 'Spending nothing for a month',
                    'D': 'Using only cash for purchases'
                },
                'correct': 'B',
                'explanation': 'Zero-based budgeting means Income − All Expenses − All Savings = ₹0. Every rupee has a job.'
            },
            {
                'q': 'Priya earns ₹50,000/month. Using 50/30/20, how much should she budget for "wants"?',
                'options': {'A': '₹25,000', 'B': '₹10,000', 'C': '₹15,000', 'D': '₹20,000'},
                'correct': 'C',
                'explanation': '30% of ₹50,000 = ₹15,000 for wants like dining, entertainment, and lifestyle expenses.'
            },
            {
                'q': 'Which Indian app automatically reads SMS messages to track spending?',
                'options': {'A': 'Zerodha', 'B': 'Groww', 'C': 'Walnut', 'D': 'BHIM UPI'},
                'correct': 'C',
                'explanation': 'Walnut is an India-specific budget app that auto-reads bank SMS messages to categorise spending.'
            },
            {
                'q': 'When should you ideally write your monthly budget?',
                'options': {
                    'A': 'After the month ends to review',
                    'B': 'At the start of the month before spending',
                    'C': 'Only when you run out of money',
                    'D': 'Once a year during tax season'
                },
                'correct': 'B',
                'explanation': 'A budget written BEFORE the month starts is far more effective than reviewing spending after it ends.'
            },
            {
                'q': 'Amit earns ₹40,000/month. His rent is ₹15,000, groceries ₹5,000, transport ₹2,000. What % of income are his needs?',
                'options': {'A': '55%', 'B': '50%', 'C': '37.5%', 'D': '45%'},
                'correct': 'A',
                'explanation': 'Needs = ₹15,000 + ₹5,000 + ₹2,000 = ₹22,000. ₹22,000 / ₹40,000 × 100 = 55%.'
            },
            {
                'q': 'What is the main benefit of using the envelope method for budgeting?',
                'options': {
                    'A': 'It earns interest on cash',
                    'B': 'It makes spending feel real, reducing overspending by 12-18%',
                    'C': 'It automatically invests your savings',
                    'D': 'It eliminates the need for a bank account'
                },
                'correct': 'B',
                'explanation': 'Studies show people spend 12-18% less when using cash envelopes because physically handing over cash makes spending feel more real.'
            },
            {
                'q': 'Which formula do you use to total all expenses in a Google Sheets budget column?',
                'options': {
                    'A': '=SUM(D:D)',
                    'B': '=COUNTIF(E:E,"OUT")',
                    'C': '=SUMIF(E:E,"OUT",D:D)',
                    'D': '=AVERAGE(D:D)'
                },
                'correct': 'C',
                'explanation': 'SUMIF sums values in column D where the corresponding column E equals "OUT" — this totals all expense rows.'
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # LEVEL 2 — SAVING STRATEGIES
    # ══════════════════════════════════════════════════════
    {
        'id': 2,
        'slug': 'saving',
        'title': 'Saving Strategies',
        'icon': '🏦',
        'desc': 'Pay yourself first, build an emergency fund, and discover high-yield places to park your money.',
        'xp_reward': 350,
        'coins_reward': 70,
        'prerequisite': 'budgeting',
        'level_field': 'saving_level',
        'topics': [
            {
                'id': 's1',
                'slug': 'pay-yourself-first',
                'title': 'Pay Yourself First',
                'icon': '💡',
                'steps': [
                    {
                        'title': 'The Most Powerful Saving Habit',
                        'body': """
<p><strong>Pay Yourself First</strong> means automating your savings the moment your salary arrives — before spending a single rupee.</p>
<p>Most people do this:</p>
<div class="flow-box">Salary → Pay all expenses → Save what's left → <span style="color:var(--red)">Often ₹0 left</span></div>
<p>You should do this:</p>
<div class="flow-box">Salary → <span style="color:var(--green)">Save first (auto-transfer)</span> → Pay expenses with what remains</div>
<div class="tip-box">💡 Set up an auto-debit on your salary day (1st or 7th of month) to move a fixed amount to a savings/investment account. If you never see the money, you won't spend it.</div>
"""
                    },
                    {
                        'title': 'How to Automate Your Savings',
                        'body': """
<p>Step-by-step automation:</p>
<ol>
  <li><strong>Open a separate savings account</strong> — different bank from your salary account makes it harder to impulsively spend</li>
  <li><strong>Set up a standing instruction</strong> — log into net banking and create a recurring transfer on salary day</li>
  <li><strong>Or set up SIP</strong> — mutual fund SIPs auto-debit from your account on a fixed date</li>
  <li><strong>Start small</strong> — even ₹500/month is better than ₹0. Increase by 10% every 6 months.</li>
</ol>
<div class="tip-box">💡 <strong>Power of habit:</strong> ₹2,000/month saved at 7% interest = ₹3.5 lakh in 10 years, ₹10.3 lakh in 20 years — with zero effort after setup.</div>
"""
                    },
                ],
            },
            {
                'id': 's2',
                'slug': 'goal-based-saving',
                'title': 'Goal-Based Saving',
                'icon': '🎯',
                'steps': [
                    {
                        'title': 'Save for Specific Goals',
                        'body': """
<p>Saving "in general" rarely works. Saving for a <em>specific goal with a deadline</em> works extremely well.</p>
<div class="goal-examples">
  <div class="goal-card">
    <div>✈️ Europe Trip</div>
    <div>₹1,20,000</div>
    <div>12 months → ₹10,000/month</div>
  </div>
  <div class="goal-card">
    <div>💻 MacBook</div>
    <div>₹1,30,000</div>
    <div>10 months → ₹13,000/month</div>
  </div>
  <div class="goal-card">
    <div>🏠 Home down payment</div>
    <div>₹5,00,000</div>
    <div>36 months → ₹13,900/month</div>
  </div>
</div>
<div class="tip-box">💡 Open one savings account per goal. Label it clearly ("Europe Fund"). Seeing the balance grow toward a specific target is deeply motivating.</div>
"""
                    },
                    {
                        'title': 'Short vs Long-Term Goal Buckets',
                        'body': """
<p>Match your savings vehicle to your goal timeline:</p>
<div class="table-simple">
  <div class="ts-row ts-head"><span>Timeline</span><span>Goal Examples</span><span>Best Vehicle</span></div>
  <div class="ts-row"><span>0-3 months</span><span>Emergency buffer, phone</span><span>Savings account / Liquid fund</span></div>
  <div class="ts-row"><span>3-12 months</span><span>Travel, laptop, bike</span><span>FD or short-term debt fund</span></div>
  <div class="ts-row"><span>1-3 years</span><span>Car, higher education</span><span>Debt mutual fund / RD</span></div>
  <div class="ts-row"><span>3+ years</span><span>Home, retirement</span><span>Equity mutual fund / SIP</span></div>
</div>
<div class="tip-box">⚠️ Never keep long-term money in a savings account — inflation eats it. And never keep short-term money in stocks — you might need it when the market is down.</div>
"""
                    },
                ],
            },
            {
                'id': 's3',
                'slug': 'high-yield-accounts',
                'title': 'High-Yield Savings',
                'icon': '🏦',
                'steps': [
                    {
                        'title': 'Where to Park Your Money in India',
                        'body': """
<p>Regular savings accounts at big banks pay only 2.5-3.5% — often below inflation. Better options:</p>
<div class="rate-cards">
  <div class="rate-card">
    <div class="rate-label">Small Finance Banks</div>
    <div class="rate-pct">6–7%</div>
    <div class="rate-desc">AU Small Finance Bank, IDFC First — DICGC insured up to ₹5 lakh. Safe.</div>
  </div>
  <div class="rate-card">
    <div class="rate-label">Fixed Deposit (FD)</div>
    <div class="rate-pct">6.5–8%</div>
    <div class="rate-desc">Guaranteed returns. Lock-in period. Great for goals 6+ months away.</div>
  </div>
  <div class="rate-card rc-green">
    <div class="rate-label">Liquid Mutual Funds</div>
    <div class="rate-pct">6.5–7.5%</div>
    <div class="rate-desc">No lock-in. Withdraw in 24hrs. Better than FD for emergency fund.</div>
  </div>
</div>
"""
                    },
                    {
                        'title': 'Building Your Emergency Fund',
                        'body': """
<p>An <strong>emergency fund</strong> is 3-6 months of living expenses kept in a liquid, accessible account — <em>only for true emergencies</em> (job loss, medical crisis).</p>
<p><strong>How much do you need?</strong></p>
<div class="formula-box">Monthly Expenses × 3 (minimum) to × 6 (recommended)</div>
<p>If you spend ₹25,000/month → Emergency fund = <strong>₹75,000 – ₹1,50,000</strong></p>
<p><strong>Where to keep it:</strong></p>
<ul>
  <li>✅ Liquid mutual fund (Parag Parikh, HDFC Liquid) — best combination of return + accessibility</li>
  <li>✅ High-yield savings account at a small finance bank</li>
  <li>❌ NOT in a regular savings account (too low returns)</li>
  <li>❌ NOT in stocks or equity funds (could be down 40% when you need it most)</li>
</ul>
<div class="tip-box">🛡️ An emergency fund isn't an investment — it's <em>insurance</em> for your financial life. Without it, one bad month can wipe out years of savings.</div>
"""
                    },
                ],
            },
            {
                'id': 's4',
                'slug': 'saving-automation',
                'title': 'Saving Automations',
                'icon': '⚙️',
                'steps': [
                    {
                        'title': 'Set-It-and-Forget-It Systems',
                        'body': """
<p>The best saving system is one that runs without your involvement:</p>
<ul>
  <li>⚙️ <strong>Standing instructions</strong> — auto-transfer from salary account on 2nd of every month</li>
  <li>📈 <strong>SIP (Systematic Investment Plan)</strong> — auto-invest in mutual funds monthly</li>
  <li>🪣 <strong>Savings jars (Fi Money / Jupiter)</strong> — smart accounts with auto-save rules</li>
  <li>🔄 <strong>Round-up savings</strong> — some neo-banks round up every UPI transaction and save the difference</li>
</ul>
<div class="tip-box">⚡ <strong>The 72-hour rule for subscriptions:</strong> Before subscribing to anything new, wait 72 hours. If you still want it, buy it. You'll cancel 60% of impulse subscriptions during the wait.</div>
"""
                    },
                ],
            },
        ],
        'quiz': [
            {
                'q': '"Pay Yourself First" means:',
                'options': {
                    'A': 'Spending on yourself before paying bills',
                    'B': 'Automating savings before spending any money',
                    'C': 'Earning more than you spend',
                    'D': 'Paying your credit card first'
                },
                'correct': 'B',
                'explanation': 'Pay Yourself First means automatically transferring savings the moment your salary arrives, before any spending happens.'
            },
            {
                'q': 'How many months of expenses should a complete emergency fund cover?',
                'options': {'A': '1 month', 'B': '2 months', 'C': '3-6 months', 'D': '12 months'},
                'correct': 'C',
                'explanation': 'Financial advisors recommend 3-6 months of living expenses in an emergency fund — enough to survive job loss or a medical crisis.'
            },
            {
                'q': 'If your monthly expenses are ₹20,000, what is the minimum emergency fund you need?',
                'options': {'A': '₹20,000', 'B': '₹40,000', 'C': '₹60,000', 'D': '₹1,20,000'},
                'correct': 'C',
                'explanation': '₹20,000 × 3 months (minimum) = ₹60,000. Ideally you would save up to ₹1,20,000 (6 months).'
            },
            {
                'q': 'Which is the BEST place to keep an emergency fund?',
                'options': {
                    'A': 'In stocks for high returns',
                    'B': 'Under the mattress',
                    'C': 'Liquid mutual fund or high-yield savings account',
                    'D': 'In cryptocurrency for maximum growth'
                },
                'correct': 'C',
                'explanation': 'A liquid mutual fund or high-yield savings account gives 6-7% returns while remaining fully accessible within 24 hours — perfect for emergencies.'
            },
            {
                'q': 'Which savings vehicle is BEST for a goal 5 years away?',
                'options': {
                    'A': 'Regular savings account',
                    'B': 'Equity mutual fund SIP',
                    'C': 'Under your pillow',
                    'D': 'Short-term FD'
                },
                'correct': 'B',
                'explanation': 'For 5+ year goals, equity mutual fund SIPs give the best returns (12-15% historically). Short-term vehicles erode real value due to inflation.'
            },
            {
                'q': 'A Small Finance Bank savings account offers around what interest rate?',
                'options': {'A': '2-3%', 'B': '4-5%', 'C': '6-7%', 'D': '10-12%'},
                'correct': 'C',
                'explanation': 'Small Finance Banks like AU Small Finance Bank and IDFC First offer 6-7% on savings accounts, far above the 2.5-3.5% at major banks.'
            },
            {
                'q': 'Neha saves ₹2,000/month at 7% annual return. Approximately how much will she have in 10 years?',
                'options': {'A': '₹2,40,000', 'B': '₹3,50,000', 'C': '₹1,00,000', 'D': '₹5,00,000'},
                'correct': 'B',
                'explanation': '₹2,000/month at 7% for 10 years = approximately ₹3.5 lakh due to compound interest.'
            },
            {
                'q': 'What does a SIP (Systematic Investment Plan) do?',
                'options': {
                    'A': 'Pays your insurance premium automatically',
                    'B': 'Auto-invests a fixed amount in mutual funds each month',
                    'C': 'Opens multiple savings accounts',
                    'D': 'Calculates your tax deductions'
                },
                'correct': 'B',
                'explanation': 'A SIP automatically debits a fixed amount from your bank account each month and invests it in a mutual fund of your choice.'
            },
            {
                'q': 'Why should emergency fund money NOT be kept in stocks?',
                'options': {
                    'A': 'Stocks are illegal for individuals',
                    'B': 'You might need the money when the market is down 40%',
                    'C': 'Stocks earn too much return',
                    'D': 'SEBI does not allow it'
                },
                'correct': 'B',
                'explanation': 'Emergencies often happen during economic downturns when stocks are down. You might be forced to sell at a 30-40% loss — the exact opposite of what you want.'
            },
            {
                'q': 'The "72-hour rule for subscriptions" helps you:',
                'options': {
                    'A': 'Earn cashback in 72 hours',
                    'B': 'Cancel impulse subscription purchases by waiting before buying',
                    'C': 'Pay bills within 72 hours to avoid late fees',
                    'D': 'Get better interest rates after 72 hours'
                },
                'correct': 'B',
                'explanation': 'Waiting 72 hours before buying a new subscription filters out impulse decisions — you end up cancelling about 60% of them.'
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # LEVEL 3 — DEBT MANAGEMENT
    # ══════════════════════════════════════════════════════
    {
        'id': 3,
        'slug': 'debt',
        'title': 'Debt Management',
        'icon': '💳',
        'desc': 'Understand good vs bad debt, master repayment strategies, and learn how your CIBIL score works.',
        'xp_reward': 400,
        'coins_reward': 80,
        'prerequisite': 'saving',
        'level_field': 'debt_level',
        'topics': [
            {
                'id': 'd1',
                'slug': 'good-vs-bad-debt',
                'title': 'Good vs Bad Debt',
                'icon': '⚖️',
                'steps': [
                    {
                        'title': 'Not All Debt is Created Equal',
                        'body': """
<p>Debt is a tool. Like any tool, it can build you up or tear you down depending on how you use it.</p>
<div class="two-col">
  <div class="col-box col-green">
    <h4>✅ Good Debt</h4>
    <p>Helps you earn more or build lasting value. Low interest rate.</p>
    <ul>
      <li>Education loan (increases future income)</li>
      <li>Home loan (builds an asset)</li>
      <li>Business loan (creates income)</li>
    </ul>
    <div style="margin-top:0.5rem;font-size:0.85rem;color:var(--green-dark)">Interest: 7-12%</div>
  </div>
  <div class="col-box col-red">
    <h4>❌ Bad Debt</h4>
    <p>Finances depreciating items or lifestyle. Very high interest.</p>
    <ul>
      <li>Credit card balance (not paid in full)</li>
      <li>Personal loan for phone/vacation</li>
      <li>Buy-now-pay-later for clothes</li>
    </ul>
    <div style="margin-top:0.5rem;font-size:0.85rem;color:var(--red)">Interest: 18-42%</div>
  </div>
</div>
<div class="tip-box">⚠️ A credit card charging 36% APR doubles your debt every 2 years (Rule of 72: 72/36 = 2 years). ₹50,000 in unpaid credit card debt becomes ₹1 lakh in 2 years if you only pay minimums.</div>
"""
                    },
                ],
            },
            {
                'id': 'd2',
                'slug': 'avalanche-method',
                'title': 'Avalanche Method',
                'icon': '🏔️',
                'steps': [
                    {
                        'title': 'The Mathematically Optimal Strategy',
                        'body': """
<p>The <strong>Debt Avalanche</strong> method pays off debt in order of <em>highest interest rate first</em>.</p>
<p><strong>How it works:</strong></p>
<ol>
  <li>List all debts with their balances and interest rates</li>
  <li>Pay the minimum on all debts every month</li>
  <li>Put every extra rupee toward the <strong>highest-interest debt</strong></li>
  <li>Once that's paid off, roll its payment to the next highest</li>
</ol>
<p><strong>Example:</strong></p>
<div class="debt-table">
  <div class="dt-row dt-head"><span>Debt</span><span>Balance</span><span>Rate</span><span>Action</span></div>
  <div class="dt-row dt-active"><span>Credit Card</span><span>₹25,000</span><span>36%</span><span>⚡ Attack first</span></div>
  <div class="dt-row"><span>Personal Loan</span><span>₹1,00,000</span><span>18%</span><span>Pay minimum</span></div>
  <div class="dt-row"><span>Education Loan</span><span>₹3,00,000</span><span>9%</span><span>Pay minimum</span></div>
</div>
<div class="tip-box">📊 The Avalanche method saves the MOST money on interest — it's the mathematically optimal strategy. Best for disciplined people who can stay motivated without quick wins.</div>
"""
                    },
                ],
            },
            {
                'id': 'd3',
                'slug': 'snowball-method',
                'title': 'Snowball Method',
                'icon': '⛄',
                'steps': [
                    {
                        'title': 'The Psychologically Powerful Strategy',
                        'body': """
<p>The <strong>Debt Snowball</strong> method pays off debt in order of <em>smallest balance first</em> — regardless of interest rate.</p>
<p><strong>How it works:</strong></p>
<ol>
  <li>List all debts from smallest to largest balance</li>
  <li>Pay minimums on all debts</li>
  <li>Throw every extra rupee at the <strong>smallest balance</strong></li>
  <li>When it's paid off, roll that payment to the next smallest</li>
</ol>
<div class="two-col">
  <div class="col-box col-green">
    <h4>✅ Snowball Wins At:</h4>
    <ul>
      <li>Motivation — quick wins feel great</li>
      <li>People who've failed at debt payoff before</li>
      <li>Reducing number of bills faster</li>
    </ul>
  </div>
  <div class="col-box col-blue">
    <h4>📊 Avalanche Wins At:</h4>
    <ul>
      <li>Total interest saved</li>
      <li>Time to become debt-free</li>
      <li>Mathematically optimal</li>
    </ul>
  </div>
</div>
<div class="tip-box">🧠 Research shows most people succeed with the Snowball method — the psychological wins matter more than the math. Dave Ramsey popularised it for a reason. Use whichever keeps you going!</div>
"""
                    },
                ],
            },
            {
                'id': 'd4',
                'slug': 'cibil-score',
                'title': 'CIBIL Credit Score',
                'icon': '📊',
                'steps': [
                    {
                        'title': 'What is a CIBIL Score?',
                        'body': """
<p>Your <strong>CIBIL score</strong> (300–900) is your financial reputation number — banks check it before giving you any loan or credit card.</p>
<div class="score-meter">
  <div class="sm-segment sm-bad">300–579<br>Poor</div>
  <div class="sm-segment sm-ok">580–669<br>Fair</div>
  <div class="sm-segment sm-good">670–739<br>Good</div>
  <div class="sm-segment sm-great">740–799<br>Very Good</div>
  <div class="sm-segment sm-excel">800–900<br>Exceptional</div>
</div>
<p>A score of <strong>750+</strong> gets you the best loan interest rates, higher credit limits, and instant approvals.</p>
<div class="tip-box">💡 A 750+ CIBIL score can save you 1-2% on a home loan interest rate. On a ₹50 lakh loan over 20 years, that's ₹8-15 lakh saved in total interest!</div>
"""
                    },
                    {
                        'title': 'How to Build and Improve Your Score',
                        'body': """
<p>Your score is calculated based on:</p>
<div class="factor-bars">
  <div class="fb-row"><span>Payment History</span><div class="fb-bar"><div class="fb-fill" style="width:35%">35%</div></div></div>
  <div class="fb-row"><span>Credit Utilisation</span><div class="fb-bar"><div class="fb-fill" style="width:30%">30%</div></div></div>
  <div class="fb-row"><span>Length of History</span><div class="fb-bar"><div class="fb-fill" style="width:15%">15%</div></div></div>
  <div class="fb-row"><span>Credit Mix</span><div class="fb-bar"><div class="fb-fill" style="width:10%">10%</div></div></div>
  <div class="fb-row"><span>New Inquiries</span><div class="fb-bar"><div class="fb-fill" style="width:10%">10%</div></div></div>
</div>
<p><strong>Key actions to boost your score:</strong></p>
<ul>
  <li>✅ Pay your FULL credit card bill every month (not just minimum)</li>
  <li>✅ Keep credit utilisation below 30% (use max ₹30k of a ₹1L limit)</li>
  <li>✅ Don't close old credit cards — long history helps</li>
  <li>❌ Never apply for 3+ credit cards in a short period (hard inquiries hurt)</li>
  <li>❌ Never miss an EMI — even one missed payment hurts for 7 years</li>
</ul>
"""
                    },
                ],
            },
        ],
        'quiz': [
            {
                'q': 'Which type of debt is generally considered "good debt"?',
                'options': {
                    'A': 'Credit card balance',
                    'B': 'Education loan that increases your earning potential',
                    'C': 'Buy-now-pay-later for a smartphone',
                    'D': 'Personal loan for a vacation'
                },
                'correct': 'B',
                'explanation': 'Good debt helps build value or increase future income. Education loans do both — they have low interest rates and boost your earning potential.'
            },
            {
                'q': 'The Debt Avalanche method pays debts in order of:',
                'options': {
                    'A': 'Smallest balance first',
                    'B': 'Largest balance first',
                    'C': 'Highest interest rate first',
                    'D': 'Oldest debt first'
                },
                'correct': 'C',
                'explanation': 'The Avalanche method targets the highest-interest debt first, saving the most money on total interest — the mathematically optimal approach.'
            },
            {
                'q': 'The Debt Snowball method pays debts in order of:',
                'options': {
                    'A': 'Highest interest rate first',
                    'B': 'Smallest balance first',
                    'C': 'Largest balance first',
                    'D': 'Newest debt first'
                },
                'correct': 'B',
                'explanation': 'The Snowball method targets smallest balances first for quick psychological wins, helping people stay motivated during debt payoff.'
            },
            {
                'q': 'A credit card charges 36% APR. Using the Rule of 72, how long does it take for the debt to double?',
                'options': {'A': '6 years', 'B': '4 years', 'C': '2 years', 'D': '1 year'},
                'correct': 'C',
                'explanation': 'Rule of 72: 72 ÷ 36 = 2 years. A ₹50,000 credit card balance unpaid for 2 years becomes ₹1,00,000!'
            },
            {
                'q': 'What is an excellent CIBIL credit score?',
                'options': {'A': 'Above 600', 'B': 'Above 700', 'C': 'Above 750', 'D': 'Exactly 900'},
                'correct': 'C',
                'explanation': 'A CIBIL score of 750+ is considered excellent and qualifies you for the best loan rates and highest credit limits.'
            },
            {
                'q': 'Credit Utilisation (30% of your CIBIL score) means you should keep usage below:',
                'options': {'A': '10% of credit limit', 'B': '30% of credit limit', 'C': '50% of credit limit', 'D': '80% of credit limit'},
                'correct': 'B',
                'explanation': 'Keep credit card spending below 30% of your limit. If your limit is ₹1 lakh, spend no more than ₹30,000 per billing cycle.'
            },
            {
                'q': 'Priya has ₹10,000 on a credit card (36%), ₹50,000 personal loan (18%), ₹2,00,000 education loan (9%). Using Avalanche, which does she pay off first?',
                'options': {
                    'A': 'Education loan (largest balance)',
                    'B': 'Personal loan (middle balance)',
                    'C': 'Credit card (highest interest)',
                    'D': 'All equally'
                },
                'correct': 'C',
                'explanation': 'Avalanche = highest interest rate first. The credit card at 36% is the most expensive debt and should be cleared first.'
            },
            {
                'q': 'Why is closing old credit cards bad for your CIBIL score?',
                'options': {
                    'A': 'It increases your credit utilisation percentage',
                    'B': 'CIBIL charges a fee for closures',
                    'C': 'It reduces the length of your credit history',
                    'D': 'Both A and C'
                },
                'correct': 'D',
                'explanation': 'Closing an old card reduces credit history length (15% of score) AND increases utilisation ratio if you still have balances on other cards (30% of score).'
            },
            {
                'q': 'Which action has the BIGGEST negative impact on your CIBIL score?',
                'options': {
                    'A': 'Checking your own score',
                    'B': 'Missing an EMI payment',
                    'C': 'Having too many credit cards',
                    'D': 'Paying the minimum amount'
                },
                'correct': 'B',
                'explanation': 'Missing an EMI is the most damaging — payment history is 35% of your score, and a missed payment stays on your record for 7 years.'
            },
            {
                'q': 'A home loan rate of 8.5% vs 10% on ₹50 lakh over 20 years is roughly:',
                'options': {
                    'A': 'Negligible difference',
                    'B': 'A saving of ₹1-2 lakh total',
                    'C': 'A saving of ₹8-15 lakh total',
                    'D': 'A saving of ₹50 lakh total'
                },
                'correct': 'C',
                'explanation': 'A 1.5% rate difference on ₹50 lakh over 20 years is approximately ₹8-15 lakh in total interest paid. A good CIBIL score makes this difference.'
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # LEVEL 4 — INVESTING BASICS
    # ══════════════════════════════════════════════════════
    {
        'id': 4,
        'slug': 'investing',
        'title': 'Investing Basics',
        'icon': '📈',
        'desc': 'Learn mutual funds, SIPs, stock market basics, and how compound interest creates long-term wealth.',
        'xp_reward': 450,
        'coins_reward': 90,
        'prerequisite': 'debt',
        'level_field': 'investing_level',
        'topics': [
            {
                'id': 'i1',
                'slug': 'mutual-funds-101',
                'title': 'Mutual Funds 101',
                'icon': '🌐',
                'steps': [
                    {
                        'title': 'What is a Mutual Fund?',
                        'body': """
<p>A <strong>mutual fund</strong> pools money from thousands of investors and a professional fund manager invests it in stocks, bonds, or both.</p>
<div class="flow-box">
  <span>You invest ₹1,000</span> → <span>Pool with others</span> → <span>Fund manager buys stocks/bonds</span> → <span>You own a small piece of everything</span>
</div>
<p><strong>Types of mutual funds:</strong></p>
<div class="table-simple">
  <div class="ts-row ts-head"><span>Type</span><span>Invests In</span><span>Risk</span><span>Expected Return</span></div>
  <div class="ts-row"><span>Equity Fund</span><span>Stocks</span><span>High</span><span>12-15% (long term)</span></div>
  <div class="ts-row"><span>Debt Fund</span><span>Bonds/FDs</span><span>Low</span><span>6-8%</span></div>
  <div class="ts-row"><span>Hybrid Fund</span><span>Mix of both</span><span>Medium</span><span>8-11%</span></div>
  <div class="ts-row"><span>Index Fund</span><span>Nifty 50 / Sensex</span><span>Medium</span><span>11-13%</span></div>
</div>
<div class="tip-box">💡 For most beginners, a <strong>Nifty 50 index fund</strong> is the best starting point — lowest cost, no fund manager risk, historically strong returns.</div>
"""
                    },
                ],
            },
            {
                'id': 'i2',
                'slug': 'sip-investing',
                'title': 'SIP Investing',
                'icon': '📈',
                'steps': [
                    {
                        'title': 'Power of SIP: Small Amounts, Big Wealth',
                        'body': """
<p>A <strong>SIP (Systematic Investment Plan)</strong> invests a fixed amount in a mutual fund automatically every month.</p>
<p>Why SIP is brilliant:</p>
<ul>
  <li>📅 <strong>Rupee cost averaging</strong> — you buy more units when prices are low, fewer when high</li>
  <li>⚙️ <strong>Automated</strong> — no willpower needed, no market timing</li>
  <li>🎯 <strong>Start small</strong> — as little as ₹100/month on Zerodha or Groww</li>
</ul>
<div class="sip-example">
  <div class="sip-row"><span>₹2,000/month for 20 years at 12%</span><span>→ <strong>₹19.8 lakh</strong></span></div>
  <div class="sip-row"><span>₹5,000/month for 20 years at 12%</span><span>→ <strong>₹49.6 lakh</strong></span></div>
  <div class="sip-row sip-highlight"><span>₹10,000/month for 25 years at 12%</span><span>→ <strong>₹1.88 crore</strong></span></div>
</div>
<div class="tip-box">⚡ Starting a SIP at 22 vs 32 can mean 3× more wealth at retirement — time in the market beats timing the market, every time.</div>
"""
                    },
                ],
            },
            {
                'id': 'i3',
                'slug': 'stock-market',
                'title': 'Stock Market Basics',
                'icon': '🏛️',
                'steps': [
                    {
                        'title': 'NSE, BSE, Nifty, Sensex — Explained Simply',
                        'body': """
<p>Buying a stock means buying a tiny ownership stake in a company.</p>
<div class="two-col">
  <div class="col-box">
    <h4>🏛️ NSE & BSE</h4>
    <p><strong>NSE</strong> (National Stock Exchange) and <strong>BSE</strong> (Bombay Stock Exchange) are where stocks are bought and sold. Like a marketplace for company shares.</p>
  </div>
  <div class="col-box">
    <h4>📊 Nifty & Sensex</h4>
    <p><strong>Nifty 50</strong> = top 50 companies on NSE. <strong>Sensex</strong> = top 30 on BSE. These indices tell you how the overall market is performing.</p>
  </div>
</div>
<p><strong>How to start:</strong></p>
<ol>
  <li>Open a Demat account on Zerodha, Groww, or Upstox (free)</li>
  <li>Complete KYC with Aadhaar + PAN</li>
  <li>Start with index funds or blue-chip stocks</li>
</ol>
<div class="tip-box">⚠️ Direct stock picking requires research and time. For most beginners, index funds or mutual funds are safer and often outperform stock pickers long-term.</div>
"""
                    },
                ],
            },
            {
                'id': 'i4',
                'slug': 'compound-interest',
                'title': 'Compound Interest',
                'icon': '⚡',
                'steps': [
                    {
                        'title': 'The Eighth Wonder of the World',
                        'body': """
<p>Einstein (allegedly) called compound interest <em>"the eighth wonder of the world."</em> Here's why:</p>
<div class="formula-box">Compound Interest = Principal × (1 + Rate)<sup>Time</sup></div>
<p>Simple example: ₹10,000 invested at 12% per year:</p>
<div class="compound-table">
  <div class="ct-row ct-head"><span>Years</span><span>Value</span><span>Gain</span></div>
  <div class="ct-row"><span>5 yrs</span><span>₹17,623</span><span>+₹7,623</span></div>
  <div class="ct-row"><span>10 yrs</span><span>₹31,058</span><span>+₹21,058</span></div>
  <div class="ct-row"><span>20 yrs</span><span>₹96,463</span><span>+₹86,463</span></div>
  <div class="ct-row ct-highlight"><span>30 yrs</span><span>₹2,99,599</span><span>+₹2,89,599</span></div>
</div>
<p>The jump from year 20 to year 30 (₹96k → ₹3L) is bigger than the entire first 20 years combined. <strong>Time is the multiplier.</strong></p>
<div class="tip-box">🔑 <strong>Rule of 72:</strong> Divide 72 by your return rate to find years to double. At 12% → 72/12 = 6 years to double. At 36% credit card debt → doubles in just 2 years!</div>
"""
                    },
                ],
            },
        ],
        'quiz': [
            {
                'q': 'What is a mutual fund?',
                'options': {
                    'A': 'A government-backed savings scheme',
                    'B': 'A pool of investor money managed professionally and invested in markets',
                    'C': 'A fixed deposit with variable interest',
                    'D': 'An insurance product that also invests'
                },
                'correct': 'B',
                'explanation': 'A mutual fund pools money from many investors; a professional fund manager invests it in stocks, bonds, or both based on the fund\'s objective.'
            },
            {
                'q': 'SIP stands for:',
                'options': {
                    'A': 'Systematic Insurance Plan',
                    'B': 'Simple Interest Payment',
                    'C': 'Systematic Investment Plan',
                    'D': 'Stock Income Program'
                },
                'correct': 'C',
                'explanation': 'SIP = Systematic Investment Plan. It automatically invests a fixed amount into a mutual fund every month.'
            },
            {
                'q': 'The Nifty 50 index represents:',
                'options': {
                    'A': 'Top 50 mutual funds in India',
                    'B': 'Top 50 companies listed on NSE',
                    'C': 'The 50 richest people in India',
                    'D': 'Top 50 government bonds'
                },
                'correct': 'B',
                'explanation': 'The Nifty 50 is an index of the 50 largest companies listed on the National Stock Exchange (NSE). It is a barometer of the Indian stock market.'
            },
            {
                'q': '₹10,000 at 12% compound interest for 10 years becomes approximately:',
                'options': {'A': '₹22,000', 'B': '₹31,000', 'C': '₹50,000', 'D': '₹1,20,000'},
                'correct': 'B',
                'explanation': '₹10,000 × (1.12)^10 ≈ ₹31,058. This is the power of compound interest over a decade.'
            },
            {
                'q': 'Using the Rule of 72, how long does it take to double money at 9% annual return?',
                'options': {'A': '4 years', 'B': '6 years', 'C': '8 years', 'D': '12 years'},
                'correct': 'C',
                'explanation': 'Rule of 72: 72 ÷ 9 = 8 years to double. At 9% per year, any investment doubles in approximately 8 years.'
            },
            {
                'q': 'What is "rupee cost averaging" in a SIP?',
                'options': {
                    'A': 'Investing the same rupee amount every month regardless of market levels',
                    'B': 'Averaging out loan interest rates',
                    'C': 'Buying only when the market is at its lowest',
                    'D': 'Dividing your portfolio equally among asset classes'
                },
                'correct': 'A',
                'explanation': 'Rupee cost averaging means investing a fixed ₹ amount monthly. When markets fall, you buy more units; when markets rise, you buy fewer — averaging out your cost.'
            },
            {
                'q': 'Which mutual fund type has the LOWEST cost and tracks the market index?',
                'options': {
                    'A': 'Actively managed equity fund',
                    'B': 'ULIP fund',
                    'C': 'Index fund (Nifty 50)',
                    'D': 'Sectoral fund'
                },
                'correct': 'C',
                'explanation': 'Index funds passively track the Nifty 50 or Sensex with expense ratios as low as 0.05-0.2%, much cheaper than actively managed funds at 1-2%.'
            },
            {
                'q': 'Which platform can you use to start a SIP in India?',
                'options': {'A': 'IRCTC', 'B': 'Paytm Mall', 'C': 'Zerodha or Groww', 'D': 'Amazon Pay'},
                'correct': 'C',
                'explanation': 'Zerodha (Coin), Groww, and Upstox are popular Indian platforms to start mutual fund SIPs with zero commission.'
            },
            {
                'q': 'Amit starts a ₹5,000/month SIP at age 22. Ravi starts the same SIP at age 32. At retirement (age 60), who has more money?',
                'options': {
                    'A': 'Ravi because he was more careful',
                    'B': 'Same amount',
                    'C': 'Amit — by roughly 3× more',
                    'D': 'Cannot be determined'
                },
                'correct': 'C',
                'explanation': 'Amit invests for 38 years vs Ravi\'s 28 years. Due to compounding, the extra 10 years roughly triples the final corpus. Time is the most powerful variable.'
            },
            {
                'q': 'A hybrid mutual fund invests in:',
                'options': {
                    'A': 'Only stocks',
                    'B': 'Only bonds',
                    'C': 'Both stocks and bonds',
                    'D': 'Real estate'
                },
                'correct': 'C',
                'explanation': 'Hybrid funds split investments between equity (stocks) and debt (bonds), offering medium risk and medium return — a balance between equity and debt funds.'
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # LEVEL 5 — FINANCIAL INDEPENDENCE
    # ══════════════════════════════════════════════════════
    {
        'id': 5,
        'slug': 'independence',
        'title': 'Financial Independence',
        'icon': '🏆',
        'desc': 'Master the FIRE movement, passive income, net worth tracking, and building generational wealth.',
        'xp_reward': 500,
        'coins_reward': 100,
        'prerequisite': 'investing',
        'level_field': 'independence_level',
        'topics': [
            {
                'id': 'f1',
                'slug': 'fire-movement',
                'title': 'FIRE Movement',
                'icon': '🔥',
                'steps': [
                    {
                        'title': 'What is FIRE?',
                        'body': """
<p><strong>FIRE</strong> = <strong>F</strong>inancial <strong>I</strong>ndependence, <strong>R</strong>etire <strong>E</strong>arly.</p>
<p>It's not about being rich — it's about building a corpus large enough that investment returns cover your expenses <em>forever</em>, giving you the freedom to stop working if you choose.</p>
<div class="formula-box"><strong>Your FIRE Number = Annual Expenses × 25</strong></div>
<p>Examples:</p>
<ul>
  <li>Spend ₹3 lakh/year → FIRE number = <strong>₹75 lakh</strong></li>
  <li>Spend ₹6 lakh/year → FIRE number = <strong>₹1.5 crore</strong></li>
  <li>Spend ₹12 lakh/year → FIRE number = <strong>₹3 crore</strong></li>
</ul>
<div class="tip-box">📐 The "× 25" comes from the <strong>4% Safe Withdrawal Rate</strong> — at this corpus, you can withdraw 4% annually and statistically never run out of money. Your investments replenish themselves.</div>
"""
                    },
                    {
                        'title': 'Types of FIRE and the Path to Get There',
                        'body': """
<div class="two-col">
  <div class="col-box">
    <h4>🔥 Lean FIRE</h4>
    <p>Frugal lifestyle, smaller corpus. Freedom with simplicity. Annual expenses ~₹3-5 lakh.</p>
  </div>
  <div class="col-box col-gold">
    <h4>💎 Fat FIRE</h4>
    <p>Comfortable lifestyle, larger corpus. Annual expenses ₹10 lakh+. More runway needed.</p>
  </div>
</div>
<p><strong>Savings rate is the most powerful lever:</strong></p>
<div class="table-simple">
  <div class="ts-row ts-head"><span>Savings Rate</span><span>Years to FIRE</span></div>
  <div class="ts-row"><span>10%</span><span>~40 years</span></div>
  <div class="ts-row"><span>25%</span><span>~32 years</span></div>
  <div class="ts-row"><span>50%</span><span>~17 years</span></div>
  <div class="ts-row ts-highlight"><span>70%</span><span>~8 years</span></div>
</div>
<div class="tip-box">🚀 The lever is your <strong>savings rate</strong>, not your income. Someone earning ₹15 lakh but saving 60% reaches FIRE faster than someone earning ₹30 lakh saving 10%.</div>
"""
                    },
                ],
            },
            {
                'id': 'f2',
                'slug': 'passive-income',
                'title': 'Passive Income',
                'icon': '💸',
                'steps': [
                    {
                        'title': 'Building Income That Works While You Sleep',
                        'body': """
<p><strong>Passive income</strong> is money earned with little ongoing effort once the initial work is done.</p>
<div class="income-cards">
  <div class="ic-card">
    <div>📈</div>
    <strong>Dividend Stocks</strong>
    <p>Companies share profits with shareholders. Nifty 50 dividend yield ~1-2%.</p>
  </div>
  <div class="ic-card">
    <div>🏠</div>
    <strong>Rental Property</strong>
    <p>Rent income from real estate. Gross yield 2-4% in Indian cities.</p>
  </div>
  <div class="ic-card">
    <div>🏦</div>
    <strong>Fixed Income</strong>
    <p>FD interest, bond coupons, RBI Floating Rate Bonds (8.05% currently).</p>
  </div>
  <div class="ic-card">
    <div>💻</div>
    <strong>Digital Products</strong>
    <p>Online courses, ebooks, templates — sell once, earn forever.</p>
  </div>
</div>
<div class="tip-box">💡 True financial independence = passive income ≥ living expenses. At that point, work becomes optional.</div>
"""
                    },
                ],
            },
            {
                'id': 'f3',
                'slug': 'net-worth',
                'title': 'Track Your Net Worth',
                'icon': '📊',
                'steps': [
                    {
                        'title': 'Your Financial Scoreboard',
                        'body': """
<p><strong>Net Worth = Total Assets − Total Liabilities</strong></p>
<div class="two-col">
  <div class="col-box col-green">
    <h4>✅ Assets (what you own)</h4>
    <ul>
      <li>Bank account balances</li>
      <li>Mutual fund value</li>
      <li>EPF/PPF balance</li>
      <li>Property value</li>
      <li>Car value (depreciating)</li>
    </ul>
  </div>
  <div class="col-box col-red">
    <h4>❌ Liabilities (what you owe)</h4>
    <ul>
      <li>Home loan outstanding</li>
      <li>Car loan</li>
      <li>Education loan</li>
      <li>Credit card balance</li>
    </ul>
  </div>
</div>
<div class="tip-box">📊 Track net worth monthly in a spreadsheet. Watching it grow is the most motivating financial habit you can build. Even if it starts negative — the trend is what matters.</div>
"""
                    },
                ],
            },
            {
                'id': 'f4',
                'slug': 'wealth-mindset',
                'title': 'Wealth Mindset',
                'icon': '🧠',
                'steps': [
                    {
                        'title': 'The Psychology of Building Wealth',
                        'body': """
<p>Wealth is built in the mind before it's built in the bank. Key mindset shifts:</p>
<div class="mindset-cards">
  <div class="mc-card">
    <div class="mc-old">❌ "I'll invest when I earn more"</div>
    <div class="mc-new">✅ "I'll invest whatever I earn now"</div>
  </div>
  <div class="mc-card">
    <div class="mc-old">❌ "I deserve this purchase — YOLO"</div>
    <div class="mc-new">✅ "Future me deserves financial freedom more"</div>
  </div>
  <div class="mc-card">
    <div class="mc-old">❌ "The stock market is too risky"</div>
    <div class="mc-new">✅ "Not investing is the biggest risk — inflation"</div>
  </div>
  <div class="mc-card">
    <div class="mc-old">❌ "I need a financial guru's hot tips"</div>
    <div class="mc-new">✅ "Boring index funds beat 90% of experts"</div>
  </div>
</div>
<div class="tip-box">🧠 <strong>The final truth:</strong> Financial independence is not about how much you earn — it's about the gap between what you earn and what you spend. Control the gap, and time does the rest.</div>
"""
                    },
                ],
            },
        ],
        'quiz': [
            {
                'q': 'FIRE stands for:',
                'options': {
                    'A': 'Fixed Income Retirement Expectation',
                    'B': 'Financial Independence, Retire Early',
                    'C': 'Fund Investment Retirement Education',
                    'D': 'Fixed Investment Return Engine'
                },
                'correct': 'B',
                'explanation': 'FIRE = Financial Independence, Retire Early — a movement focused on saving aggressively to achieve financial freedom and optional early retirement.'
            },
            {
                'q': 'If Priya spends ₹8 lakh per year, what is her FIRE number?',
                'options': {'A': '₹80 lakh', 'B': '₹1.6 crore', 'C': '₹2 crore', 'D': '₹3.2 crore'},
                'correct': 'C',
                'explanation': 'FIRE Number = Annual Expenses × 25 = ₹8,00,000 × 25 = ₹2,00,00,000 (₹2 crore).'
            },
            {
                'q': 'The "4% Safe Withdrawal Rate" means:',
                'options': {
                    'A': 'Withdraw 4% every week',
                    'B': 'Keep 4% in cash at all times',
                    'C': 'You can withdraw 4% of corpus annually and statistically never run out',
                    'D': 'Earn 4% per year to be financially independent'
                },
                'correct': 'C',
                'explanation': 'The 4% rule says that if your corpus is 25× your annual expenses, you can withdraw 4% per year and your investments will replenish themselves indefinitely.'
            },
            {
                'q': 'Net Worth is calculated as:',
                'options': {
                    'A': 'Monthly income × 12',
                    'B': 'Total Assets + Total Liabilities',
                    'C': 'Total Assets − Total Liabilities',
                    'D': 'Annual savings × 10'
                },
                'correct': 'C',
                'explanation': 'Net Worth = Assets (what you own) − Liabilities (what you owe). A positive and growing net worth is the clearest sign of financial health.'
            },
            {
                'q': 'Which savings rate gets you to FIRE in approximately 17 years?',
                'options': {'A': '10%', 'B': '25%', 'C': '50%', 'D': '70%'},
                'correct': 'C',
                'explanation': 'At a 50% savings rate, you can reach financial independence in approximately 17 years. At 70%, it takes just 8 years!'
            },
            {
                'q': 'Which of the following is passive income?',
                'options': {
                    'A': 'Your monthly salary',
                    'B': 'Freelance project payment',
                    'C': 'Dividend from stocks you own',
                    'D': 'Overtime pay'
                },
                'correct': 'C',
                'explanation': 'Dividends from stocks are passive income — the company pays you a share of profits without you needing to do any work after the initial investment.'
            },
            {
                'q': '"Lean FIRE" refers to:',
                'options': {
                    'A': 'A physical fitness program for investors',
                    'B': 'Financial independence with a frugal, low-expense lifestyle',
                    'C': 'A government pension scheme',
                    'D': 'Investing only in lean sectors like IT'
                },
                'correct': 'B',
                'explanation': 'Lean FIRE means achieving financial independence with a smaller corpus by maintaining a frugal lifestyle with lower annual expenses.'
            },
            {
                'q': 'Rohan earns ₹12 lakh/year and saves ₹3 lakh. Sunita earns ₹6 lakh/year and saves ₹3 lakh. Who reaches FIRE faster (assuming same expenses)?',
                'options': {
                    'A': 'Rohan (higher income)',
                    'B': 'Sunita (higher savings rate)',
                    'C': 'Both reach FIRE at the same time',
                    'D': 'Cannot be determined'
                },
                'correct': 'B',
                'explanation': 'Sunita saves 50% of income vs Rohan\'s 25%. Both save ₹3L/year but Sunita\'s lower expenses mean she needs a smaller FIRE corpus. Higher savings rate wins over higher income.'
            },
            {
                'q': 'Which habit is MOST important for tracking progress toward financial independence?',
                'options': {
                    'A': 'Checking stock prices daily',
                    'B': 'Monthly net worth tracking',
                    'C': 'Reading financial news every morning',
                    'D': 'Changing investment strategies each quarter'
                },
                'correct': 'B',
                'explanation': 'Monthly net worth tracking is the single most powerful habit — it shows you if you are making progress toward financial independence and motivates continued good behaviour.'
            },
            {
                'q': 'What is the most powerful factor in building long-term wealth?',
                'options': {
                    'A': 'Picking the best stocks',
                    'B': 'Having a high salary',
                    'C': 'The gap between income and expenses (savings rate) + time',
                    'D': 'Timing market entry and exit'
                },
                'correct': 'C',
                'explanation': 'Wealth = Savings Rate × Time. Controlling expenses relative to income creates the savings that compound over time. Neither stock-picking skill nor high salary matters as much.'
            },
        ],
    },
]

# ── Helper lookups ────────────────────────────────────────────────────────────

LEVELS_BY_SLUG   = {l['slug']: l for l in LEVELS}
TOPICS_BY_SLUG   = {t['slug']: (l, t) for l in LEVELS for t in l['topics']}

def get_level(slug):
    return LEVELS_BY_SLUG.get(slug)

def get_topic(topic_slug):
    """Returns (level_dict, topic_dict) or (None, None)."""
    return TOPICS_BY_SLUG.get(topic_slug, (None, None))
