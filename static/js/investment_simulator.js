/**
 * FinLiteracy – Investment Simulator
 * Used by: investment_simulator.html
 * Depends on: notifications.js
 */

// ─── Investment Simulator ─────────────────────────────────────────────────────

let selectedAsset = null;
let investmentAssets = {};
let portfolioChart = null;

function initInvestSimulator(assetsJson) {
    try {
        investmentAssets = JSON.parse(assetsJson);
    } catch (e) {
        console.error('Failed to parse assets', e);
    }
}

function selectAsset(assetType) {
    selectedAsset = assetType;
    document.querySelectorAll('.asset-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.asset === assetType);
    });
    const formEl = document.getElementById('invest-form');
    const assetCfg = investmentAssets[assetType] || {};
    if (formEl) {
        formEl.style.display = 'block';
        const title = formEl.querySelector('h3');
        if (title) title.textContent = `Invest in ${assetCfg.name || assetType} ${assetCfg.icon || ''}`;
    }
}

function setAmount(val) {
    const input = document.getElementById('invest-amount');
    if (input) input.value = val;
}

function buyInvestment() {
    if (!selectedAsset) {
        showToast('success', '⚠️', 'Select an asset first!', 'Click on one of the asset cards', 3000);
        return;
    }
    const amountEl = document.getElementById('invest-amount');
    const amount   = parseFloat(amountEl?.value || 0);
    if (!amount || amount < 100) {
        showToast('success', '⚠️', 'Minimum ₹100 required', '', 2500);
        return;
    }

    const btn = document.getElementById('invest-btn');
    if (btn) { btn.disabled = true; btn.textContent = 'Processing…'; }

    fetch('/invest/buy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ asset_type: selectedAsset, amount })
    })
    .then(r => r.json())
    .then(data => {
        if (btn) { btn.disabled = false; btn.textContent = 'Invest Now 📈'; }
        if (data.error) { showToast('success', '❌', data.error, '', 3000); return; }

        const resultEl = document.getElementById('invest-result');
        if (resultEl) {
            const isPos = data.return_pct >= 0;
            resultEl.innerHTML = `
                <div class="result-return ${isPos ? 'return-positive' : 'return-negative'}">
                    ₹${data.amount.toLocaleString('en-IN')} → ₹${data.current_value.toLocaleString('en-IN', {minimumFractionDigits: 0, maximumFractionDigits: 0})}
                    (${isPos ? '+' : ''}${data.return_pct.toFixed(1)}%)
                </div>
                <p style="margin-top:0.5rem;font-size:0.85rem;color:var(--text-secondary)">${data.message}</p>
            `;
            resultEl.classList.add('show');
        }

        showToast('success', '📈', `Investment placed! +${data.xp_earned} XP`, data.message.substring(0, 60), 4000);
        (data.new_badges || []).forEach(b => showBadgeToast(b));

        // Refresh holdings list
        setTimeout(() => location.reload(), 2000);
    })
    .catch(() => {
        if (btn) { btn.disabled = false; btn.textContent = 'Invest Now 📈'; }
        showToast('success', '❌', 'Failed to invest', 'Please try again', 3000);
    });
}

function simulateMarket() {
    const btn = document.getElementById('simulate-btn');
    if (btn) { btn.disabled = true; btn.textContent = '⏳ Simulating…'; }

    fetch('/invest/simulate', { method: 'POST', headers: { 'Content-Type': 'application/json' } })
    .then(r => r.json())
    .then(data => {
        if (btn) { btn.disabled = false; btn.textContent = '🔄 Simulate Market'; }
        showToast('success', '📊', 'Market updated!', `${data.updates?.length || 0} positions refreshed`, 3000);
        setTimeout(() => location.reload(), 1500);
    })
    .catch(() => {
        if (btn) { btn.disabled = false; btn.textContent = '🔄 Simulate Market'; }
    });
}

// ─── Portfolio Doughnut Chart ─────────────────────────────────────────────────

function initPortfolioChart(holdings) {
    const canvas = document.getElementById('portfolio-chart');
    if (!canvas || !holdings || !holdings.length) return;
    if (typeof Chart === 'undefined') return;

    if (portfolioChart) portfolioChart.destroy();

    const colorMap = {
        fd: '#00c875', stocks: '#ff7e2d',
        mutual_funds: '#0cbaba', crypto: '#f7931a'
    };
    const labels = holdings.map(h => h.name);
    const values = holdings.map(h => h.current_value);
    const colors = holdings.map(h => colorMap[h.type] || '#7c5cbf');

    portfolioChart = new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{ data: values, backgroundColor: colors, borderWidth: 2, borderColor: '#fff' }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { font: { family: 'DM Sans', size: 11 } } },
                tooltip: {
                    callbacks: {
                        label: (ctx) => ` ₹${ctx.parsed.toLocaleString('en-IN')}`
                    }
                }
            },
            cutout: '65%',
        }
    });
}
