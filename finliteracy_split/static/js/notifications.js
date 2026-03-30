/**
 * FinLiteracy – Notification & Modal System
 * Shared by: all app pages (dashboard, scenario, mentor, invest, etc.)
 */

// ─── Toast Notification System ────────────────────────────────────────────────

function showToast(type, icon, title, subtitle, duration = 4000) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <div class="toast-text">
            <strong>${title}</strong>
            ${subtitle ? `<span>${subtitle}</span>` : ''}
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
    `;
    container.appendChild(toast);
    setTimeout(() => { if (toast.parentElement) toast.remove(); }, duration);
}

function showBadgeToast(badge) {
    showToast('badge', badge.icon, `🏅 Badge Earned: ${badge.name}`, badge.desc, 5000);
}

function showLevelUpModal(newLevel) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
        <div class="modal-card" style="position:relative;overflow:hidden;">
            <div class="modal-emoji">🏆</div>
            <div class="modal-title">Level Up!</div>
            <div class="modal-subtitle">You've reached <strong>Level ${newLevel}</strong>!<br>Keep learning to unlock more rewards.</div>
            <button class="btn btn-primary btn-full" onclick="this.closest('.modal-overlay').remove()">
                Keep Going 🚀
            </button>
        </div>
    `;
    document.body.appendChild(overlay);
    spawnConfetti(overlay.querySelector('.modal-card'));
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
}

function spawnConfetti(parent) {
    const colors = ['#00c875','#00d4ff','#f5c842','#ff7e2d','#ff4d6a'];
    for (let i = 0; i < 18; i++) {
        const piece = document.createElement('div');
        piece.className = 'confetti-piece';
        piece.style.cssText = `
            background:${colors[i % colors.length]};
            left:${Math.random() * 100}%;
            top:${Math.random() * 30}%;
            animation-delay:${Math.random() * 0.6}s;
            animation-duration:${0.8 + Math.random() * 0.6}s;
        `;
        parent.appendChild(piece);
    }
}
