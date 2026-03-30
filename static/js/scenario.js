/**
 * FinLiteracy – Scenario Engine
 * Used by: scenario.html
 * Depends on: notifications.js
 */

// ─── Scenario Engine ──────────────────────────────────────────────────────────

let currentScenarioIndex = 0;
let scenarioCatalog = [];

function initScenarios(catalogJson) {
    try {
        scenarioCatalog = JSON.parse(catalogJson);
        renderScenarioDots();
        loadScenario(0);
    } catch (e) {
        console.error('Failed to parse scenario catalog', e);
    }
}

function renderScenarioDots() {
    const nav = document.getElementById('scenario-nav');
    if (!nav) return;
    nav.innerHTML = scenarioCatalog.map((sc, i) =>
        `<div class="scenario-dot ${i === 0 ? 'active' : ''}" id="dot-${i}" onclick="jumpToScenario(${i})" title="${sc.title}"></div>`
    ).join('');
}

function jumpToScenario(idx) {
    currentScenarioIndex = idx;
    loadScenario(idx);
}

function loadScenario(idx) {
    const sc = scenarioCatalog[idx];
    if (!sc) return;

    // Update dots
    document.querySelectorAll('.scenario-dot').forEach((d, i) => {
        d.classList.toggle('active', i === idx);
    });

    const container = document.getElementById('scenario-main-content');
    if (!container) return;

    container.style.opacity = '0';
    container.style.transform = 'translateY(10px)';

    setTimeout(() => {
        const difficultyStars = sc.difficulty === 'easy' ? '⭐ Easy' : sc.difficulty === 'medium' ? '⭐⭐ Medium' : '⭐⭐⭐ Hard';
        container.innerHTML = `
            <div class="scenario-meta">
                <span class="scenario-tag">${sc.title}</span>
                <span class="scenario-difficulty">${difficultyStars}</span>
            </div>
            <div class="scenario-question">
                <div class="scenario-avatar">${sc.avatar_emoji}</div>
                <h2 class="scenario-title">${sc.title}</h2>
                <p class="scenario-desc">${sc.description}</p>
            </div>
            <div class="scenario-options" id="scenario-options">
                ${sc.choices.map(c => `
                    <button class="scenario-btn" onclick="makeChoice('${sc.slug}', '${c.key}', this)">
                        <div class="option-icon">${c.icon}</div>
                        <div class="option-content">
                            <strong>${c.label}</strong>
                            <p>${c.desc}</p>
                        </div>
                        <div class="option-reward ${c.xp >= 150 ? 'high' : c.xp >= 100 ? 'medium' : 'low'}">+${c.xp} XP</div>
                    </button>
                `).join('')}
            </div>
            <div class="scenario-result hidden" id="scenario-result"></div>
        `;
        container.style.transition = 'all 0.35s ease';
        container.style.opacity = '1';
        container.style.transform = 'translateY(0)';
    }, 180);
}

function makeChoice(slug, choiceKey, btnEl) {
    const buttons = document.querySelectorAll('#scenario-options .scenario-btn');
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.style.opacity = '0.45';
        btn.style.transform = 'none';
    });
    btnEl.style.opacity = '1';
    btnEl.style.transform = 'translateX(4px)';
    btnEl.classList.add('selected');

    fetch('/scenario/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slug, choice: choiceKey })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) { console.error(data.error); return; }
        showScenarioResult(data);

        // Update header coin/XP display
        const coinEl = document.querySelector('.coin-display');
        const xpEl   = document.querySelector('.xp-display');
        if (coinEl) coinEl.textContent = `🪙 ${data.new_coins} coins`;
        if (xpEl)   xpEl.textContent   = `⚡ ${data.new_xp} XP`;

        // Toast
        showToast('success', data.xp >= 150 ? '🎉' : '👍',
            `+${data.xp} XP earned!`,
            `+${data.coins} coins`, 3500);

        // Badges
        (data.new_badges || []).forEach(b => showBadgeToast(b));

        // Level up
        if (data.leveled_up) {
            setTimeout(() => showLevelUpModal(data.new_level), 800);
        }

        // Mark dot as done
        const dot = document.getElementById(`dot-${currentScenarioIndex}`);
        if (dot) dot.classList.add('done');
    })
    .catch(err => {
        console.error(err);
        showToast('success', '👍', 'Choice recorded!', 'Backend unavailable – running in demo mode', 3000);
    });
}

function showScenarioResult(data) {
    const resultEl = document.getElementById('scenario-result');
    if (!resultEl) return;

    const emoji   = data.xp >= 150 ? '🎉' : data.xp >= 100 ? '👍' : '⚠️';
    const title   = data.xp >= 150 ? 'Excellent Decision!' : data.xp >= 100 ? 'Good Thinking!' : 'Room to Improve';
    const isLast  = currentScenarioIndex >= scenarioCatalog.length - 1;

    resultEl.innerHTML = `
        <div class="result-header">
            <div class="result-emoji">${emoji}</div>
            <h3 class="result-message">${title}</h3>
        </div>
        <div class="result-rewards">
            <div class="reward-chip">⚡ +${data.xp} XP</div>
            <div class="reward-chip">🪙 +${data.coins} Coins</div>
            <div class="reward-chip">📊 Score: ${data.financial_score}/100</div>
        </div>
        <div class="result-explanation">${data.message}</div>
        <div class="result-actions">
            ${!isLast
                ? `<button class="btn btn-primary" onclick="nextScenario()">Next Scenario →</button>`
                : `<a href="/dashboard" class="btn btn-primary">Back to Dashboard 🏠</a>`
            }
            <a href="/dashboard" class="btn btn-outline">Dashboard</a>
        </div>
    `;
    resultEl.classList.remove('hidden');
    resultEl.style.animation = 'fadeInUp 0.4s ease';
    setTimeout(() => resultEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
}

function nextScenario() {
    if (currentScenarioIndex < scenarioCatalog.length - 1) {
        currentScenarioIndex++;
        loadScenario(currentScenarioIndex);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Filter scenario library items by category
function filterScenarios(category, tabEl) {
    document.querySelectorAll('.scenario-tab').forEach(t => t.classList.remove('active'));
    tabEl.classList.add('active');
    document.querySelectorAll('.scenario-library-item').forEach(item => {
        item.style.display = (category === 'all' || item.dataset.category === category) ? '' : 'none';
    });
}
