/**
 * FinLiteracy – Progress Bar Animations & Countdown Timer
 * Shared by: dashboard.html, learning_path.html, achievements.html
 */

// ─── Progress Bar Animations ──────────────────────────────────────────────────

function animateBars() {
    // XP bar
    const xpFill = document.querySelector('.xp-fill');
    if (xpFill) {
        const target = xpFill.style.width;
        xpFill.style.width = '0%';
        xpFill.style.transition = 'none';
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                xpFill.style.transition = 'width 1.2s cubic-bezier(0.4,0,0.2,1)';
                xpFill.style.width = target;
            });
        });
    }

    // Chart bars (dashboard financial health)
    document.querySelectorAll('.chart-bar-fill').forEach(bar => {
        const target = bar.style.width;
        bar.style.width = '0%';
        bar.style.transition = 'none';
        setTimeout(() => {
            bar.style.transition = 'width 1.4s cubic-bezier(0.4,0,0.2,1)';
            bar.style.width = target;
        }, 300);
    });

    // Learning path big progress bar
    const bigFill = document.querySelector('.big-progress-fill');
    if (bigFill) {
        const target = bigFill.style.width;
        bigFill.style.width = '0%';
        setTimeout(() => { bigFill.style.width = target; }, 200);
    }

    // Achievement progress bar
    const apFill = document.querySelector('.ap-bar-fill');
    if (apFill) {
        const target = apFill.style.width;
        apFill.style.width = '0%';
        setTimeout(() => { apFill.style.width = target; }, 300);
    }
}


// ─── Countdown Timer ──────────────────────────────────────────────────────────

function startCountdown() {
    const timerEls = document.querySelectorAll('.challenge-timer');
    if (!timerEls.length) return;

    const midnight = new Date();
    midnight.setHours(24, 0, 0, 0);
    let remaining  = Math.floor((midnight - new Date()) / 1000);

    function updateTimer() {
        if (remaining <= 0) { timerEls.forEach(el => el.textContent = '⏰ Resetting…'); return; }
        const h = String(Math.floor(remaining / 3600)).padStart(2, '0');
        const m = String(Math.floor((remaining % 3600) / 60)).padStart(2, '0');
        const s = String(remaining % 60).padStart(2, '0');
        timerEls.forEach(el => el.textContent = `⏰ ${h}:${m}:${s} left`);
        remaining--;
    }
    updateTimer();
    setInterval(updateTimer, 1000);
}


// ─── DOMContentLoaded ─────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', function () {
    animateBars();
    startCountdown();
    console.log('🚀 FinLiteracy loaded successfully!');
});
