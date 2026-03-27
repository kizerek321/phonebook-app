// ===== DOM References =====
const contactsBody = document.getElementById('contacts-body');
const contactsTable = document.getElementById('contacts-table');
const emptyState = document.getElementById('empty-state');
const contactCount = document.getElementById('contact-count');
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

// ===== Contacts =====

async function loadContacts() {
    try {
        const res = await fetch('/contacts');
        const contacts = await res.json();
        renderContacts(contacts);
    } catch (err) {
        console.error('Failed to load contacts:', err);
    }
}

function renderContacts(contacts) {
    contactCount.textContent = contacts.length;

    if (contacts.length === 0) {
        contactsTable.classList.add('hidden');
        emptyState.classList.remove('hidden');
        return;
    }

    emptyState.classList.add('hidden');
    contactsTable.classList.remove('hidden');

    contactsBody.innerHTML = '';
    contacts.forEach(contact => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${escapeHtml(contact.name)}</td>
            <td>${escapeHtml(contact.phone)}</td>
        `;
        contactsBody.appendChild(tr);
    });
}

// ===== Chat =====

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = chatInput.value.trim();
    if (!prompt) return;

    addMessage(prompt, 'user');
    chatInput.value = '';
    setSending(true);

    // Show loading indicator
    const loadingEl = addLoading();

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });
        const data = await res.json();
        removeLoading(loadingEl);

        const reply = formatResponse(data);
        if (reply && reply.disambiguation) {
            addDisambiguationMessage(reply);
        } else {
            addMessage(reply, 'bot');
        }

        // Refresh contacts after every chat action
        await loadContacts();
    } catch (err) {
        removeLoading(loadingEl);
        addMessage('Something went wrong. Please try again.', 'bot');
        console.error('Chat error:', err);
    } finally {
        setSending(false);
        chatInput.focus();
    }
});

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `message ${sender}-message`;
    div.innerHTML = `<div class="message-bubble"><p>${text}</p></div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addLoading() {
    const div = document.createElement('div');
    div.className = 'message bot-message loading-message';
    div.innerHTML = `
        <div class="message-bubble">
            <div class="loading-dots">
                <span></span><span></span><span></span>
            </div>
        </div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div;
}

function removeLoading(el) {
    if (el && el.parentNode) el.parentNode.removeChild(el);
}

function setSending(isSending) {
    sendBtn.disabled = isSending;
    chatInput.disabled = isSending;
}

function formatResponse(data) {
    // Handle disambiguation response
    if (data.disambiguation) {
        return data;  // handled specially in chat submit handler
    }

    // Handle different response shapes from the backend
    if (data.message) return escapeHtml(data.message);
    if (data.error) return `${escapeHtml(data.error)}`;

    // Single contact returned
    if (data.name && data.phone) {
        return `<strong>${escapeHtml(data.name)}</strong>: ${escapeHtml(data.phone)}`;
    }

    // Array of contacts
    if (Array.isArray(data)) {
        if (data.length === 0) return 'The phonebook is empty.';
        const rows = data.map(c => `• <strong>${escapeHtml(c.name)}</strong>: ${escapeHtml(c.phone)}`);
        return rows.join('<br>');
    }

    return escapeHtml(JSON.stringify(data));
}

function addDisambiguationMessage(data) {
    const div = document.createElement('div');
    div.className = 'message bot-message';

    const actionLabels = {
        get: 'Pokaż',
        delete: 'Usuń',
        update: 'Edytuj'
    };
    const actionLabel = actionLabels[data.action] || data.action;

    const updateArgs = data.update_args || {};

    let buttonsHtml = data.contacts.map(c =>
        `<button class="disambig-btn" data-action="${escapeHtml(data.action)}" data-id="${c.id}">` +
        `<strong>${escapeHtml(c.name)}</strong> — ${escapeHtml(c.phone)} <span class="disambig-id">(id: ${c.id})</span>` +
        `</button>`
    ).join('');

    div.innerHTML = `
        <div class="message-bubble">
            <p>${escapeHtml(data.message)}</p>
            <div class="disambig-buttons">${buttonsHtml}</div>
        </div>`;

    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Attach click handlers
    div.querySelectorAll('.disambig-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            const id = btn.dataset.id;
            let prompt;
            if (action === 'get') {
                prompt = `Show contact with id ${id}`;
            } else if (action === 'delete') {
                prompt = `Delete contact with id ${id}`;
            } else {
                // Build update prompt with the original update details
                const parts = [];
                if (updateArgs.new_name) parts.push(`name to ${updateArgs.new_name}`);
                if (updateArgs.new_phone) parts.push(`phone to ${updateArgs.new_phone}`);
                const details = parts.length > 0 ? `, change ${parts.join(' and ')}` : '';
                prompt = `Update contact with id ${id}${details}`;
            }
            // Disable all buttons after selection
            div.querySelectorAll('.disambig-btn').forEach(b => b.disabled = true);
            sendFollowUp(prompt);
        });
    });
}

async function sendFollowUp(prompt) {
    addMessage(prompt, 'user');
    setSending(true);
    const loadingEl = addLoading();

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });
        const data = await res.json();
        removeLoading(loadingEl);

        const reply = formatResponse(data);
        if (reply && reply.disambiguation) {
            addDisambiguationMessage(reply);
        } else {
            addMessage(reply, 'bot');
        }
        await loadContacts();
    } catch (err) {
        removeLoading(loadingEl);
        addMessage('Something went wrong. Please try again.', 'bot');
        console.error('Chat error:', err);
    } finally {
        setSending(false);
        chatInput.focus();
    }
}

// ===== Utilities =====

function escapeHtml(str) {
    if (typeof str !== 'string') return str;
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ===== Init =====
loadContacts();
