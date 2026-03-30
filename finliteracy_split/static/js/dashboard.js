/**
 * FinLiteracy – Dashboard Charts
 * Used by: dashboard.html
 * Requires: Chart.js CDN
 */

// ─── Skills Radar Chart ───────────────────────────────────────────────────────

function initDashboardCharts(skillData) {
    const canvas = document.getElementById('skills-radar');
    if (!canvas || typeof Chart === 'undefined') return;

    new Chart(canvas, {
        type: 'radar',
        data: {
            labels: ['Budgeting', 'Saving', 'Investing', 'Debt Mgmt', 'Planning'],
            datasets: [{
                label: 'Your Skills',
                data: skillData || [85, 60, 30, 45, 50],
                backgroundColor: 'rgba(0,200,117,0.15)',
                borderColor: '#00c875',
                pointBackgroundColor: '#00c875',
                pointRadius: 4,
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { display: false },
                    grid: { color: 'rgba(0,0,0,0.06)' },
                    pointLabels: { font: { family: 'DM Sans', size: 11 }, color: '#4a6785' },
                }
            },
            plugins: { legend: { display: false } }
        }
    });
}

// ─── Monthly Savings Bar Chart ────────────────────────────────────────────────

function initSavingsChart(monthlyData) {
    const canvas = document.getElementById('savings-chart');
    if (!canvas || typeof Chart === 'undefined') return;

    const months = ['Aug','Sep','Oct','Nov','Dec','Jan'];
    const data   = monthlyData || [500, 800, 700, 1200, 1100, 1500];

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [{
                label: 'Virtual Savings (₹)',
                data,
                backgroundColor: 'rgba(0,200,117,0.75)',
                borderRadius: 8,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { font: { size: 11 } } },
                x: { grid: { display: false }, ticks: { font: { size: 11 } } },
            }
        }
    });
}
