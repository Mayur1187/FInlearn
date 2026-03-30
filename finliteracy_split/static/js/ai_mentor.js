/**
 * FinLiteracy – AI Mentor Chat
 * Used by: ai_mentor.html
 * Depends on: (standalone - no toast calls needed here)
 */

// ─── AI Mentor Chat ───────────────────────────────────────────────────────────

function sendMessage() {
    const input    = document.getElementById('chat-input');
    const messages = document.getElementById('chat-messages');
    const typing   = document.getElementById('typing');

    const text = input.value.trim();
    if (!text) return;

    appendMessage(messages, text, 'user');
    input.value = '';
    if (typing) typing.classList.remove('hidden');
    scrollChat(messages);

    fetch('/mentor/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    })
    .then(r => r.json())
    .then(data => {
        if (typing) typing.classList.add('hidden');
        appendMessage(messages, data.reply || data.error, 'bot');
        scrollChat(messages);
    })
    .catch(() => {
        if (typing) typing.classList.add('hidden');
        appendMessage(messages, "Sorry, I'm having trouble connecting. Please try again! 🤖", 'bot');
        scrollChat(messages);
    });
}

function appendMessage(container, text, role) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message message-${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'bot' ? '🤖' : '👤';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    // Allow simple markdown bold (**text**)
    const html = escapeHtml(text).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    bubble.innerHTML = `<p>${html}</p>`;

    msgDiv.appendChild(avatar);
    msgDiv.appendChild(bubble);
    msgDiv.style.animation = 'fadeInUp 0.3s ease';
    container.appendChild(msgDiv);
}

function scrollChat(container) {
    setTimeout(() => { container.scrollTop = container.scrollHeight; }, 50);
}

function handleEnter(event) {
    if (event.key === 'Enter') sendMessage();
}

function quickAsk(question) {
    const input = document.getElementById('chat-input');
    if (input) { input.value = question; sendMessage(); }
}

function escapeHtml(text) {
    return (text || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// Auto-scroll to bottom on page load
document.addEventListener('DOMContentLoaded', function () {
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) scrollChat(chatMessages);
});
