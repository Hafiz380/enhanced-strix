
const socket = new WebSocket(`ws://${window.location.host}/ws`);
const consoleOutput = document.getElementById('console-output');
const commandInput = document.getElementById('command-input');
const thinkingContent = document.getElementById('thinking-content');
const actionContent = document.getElementById('action-content');
const vulnList = document.getElementById('vuln-list');
const statusIndicator = document.getElementById('status-indicator');
const agentActivity = document.getElementById('agent-activity');
const scanHistory = document.getElementById('scan-history');

// Modal Elements
const modal = document.getElementById('vuln-modal');
const modalTitle = document.getElementById('modal-title');
const modalSeverity = document.getElementById('modal-severity');
const modalTarget = document.getElementById('modal-target');
const modalDescription = document.getElementById('modal-description');
const modalRemediation = document.getElementById('modal-remediation');
const closeModal = document.querySelector('.close-modal');

let history = [];
let historyIndex = -1;

// Initial Load
window.addEventListener('load', () => {
    fetchHistory();
});

async function fetchHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        renderHistory(data);
    } catch (err) {
        console.error('Failed to fetch history:', err);
    }
}

function renderHistory(data) {
    if (!data || data.length === 0) return;
    scanHistory.innerHTML = '';
    data.reverse().forEach(item => {
        const div = document.createElement('div');
        div.classList.add('history-item');
        div.innerHTML = `
            <span class="status ${item.status === 'Completed' ? 'status-completed' : 'status-failed'}">●</span>
            <div class="time">${item.timestamp}</div>
            <div class="instr">${item.instruction.substring(0, 30)}...</div>
        `;
        scanHistory.appendChild(div);
    });
}

socket.onopen = () => {
    statusIndicator.textContent = 'Connected (Online)';
    statusIndicator.style.color = '#22c55e';
    appendConsole('Enhanced Strix AI Security Auditor Initialized', 'green bold');
    appendConsole('Ready to assist with security tasks and vulnerability assessments.', 'dim');
};

socket.onclose = () => {
    statusIndicator.textContent = 'Offline (Server Disconnected)';
    statusIndicator.style.color = '#ef4444';
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'console':
            appendConsole(data.content, data.style);
            break;
        case 'thinking':
            thinkingContent.textContent = data.content;
            thinkingContent.parentElement.scrollTop = thinkingContent.parentElement.scrollHeight;
            break;
        case 'action':
            actionContent.textContent = data.content;
            break;
        case 'vulnerability':
            addVulnerability(data);
            break;
        case 'tool_usage':
            addToolUsage(data);
            break;
    }
};

function addToolUsage(data) {
    if (agentActivity.querySelector('.activity-item')?.textContent.includes('Waiting')) {
        agentActivity.innerHTML = '';
    }
    const div = document.createElement('div');
    div.classList.add('activity-item');
    div.innerHTML = `AI using <span class="tool">${data.tool}</span>: ${data.logic}`;
    agentActivity.prepend(div);
    if (agentActivity.children.length > 10) agentActivity.lastChild.remove();
}

// Global Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        consoleOutput.innerHTML = '';
        appendConsole('Console cleared.', 'dim');
    }
    if (!['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
        if (e.key.length === 1 || e.key === 'Backspace') {
            commandInput.focus();
        }
    }
});

commandInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const command = commandInput.value.trim();
        if (command) {
            socket.send(JSON.stringify({ type: 'command', content: command }));
            appendConsole(`Executing Task: ${command}`, 'yellow bold');
            history.push(command);
            historyIndex = -1;
            commandInput.value = '';
            // Clear current vulnerabilities for new scan
            vulnList.innerHTML = '';
            agentActivity.innerHTML = '<div class="activity-item">New session started...</div>';
        }
    } else if (e.key === 'ArrowUp') {
        if (history.length > 0) {
            e.preventDefault();
            historyIndex = Math.min(historyIndex + 1, history.length - 1);
            commandInput.value = history[history.length - 1 - historyIndex];
        }
    } else if (e.key === 'ArrowDown') {
        if (historyIndex > 0) {
            e.preventDefault();
            historyIndex--;
            commandInput.value = history[history.length - 1 - historyIndex];
        } else if (historyIndex === 0) {
            e.preventDefault();
            historyIndex = -1;
            commandInput.value = '';
        }
    }
});

function appendConsole(text, style = '') {
    const div = document.createElement('div');
    div.textContent = text;
    if (style) {
        style.split(' ').forEach(s => div.classList.add(s));
    }
    consoleOutput.appendChild(div);
    consoleOutput.scrollTo({
        top: consoleOutput.scrollHeight,
        behavior: 'smooth'
    });
}

function addVulnerability(vuln) {
    const div = document.createElement('div');
    div.classList.add('vuln-item');
    div.dataset.id = vuln.id;
    div.innerHTML = `
        <div class="severity-high bold">● ${vuln.title}</div>
        <div class="dim">${vuln.target}</div>
    `;
    div.onclick = () => showVulnDetail(vuln.id);
    vulnList.appendChild(div);
    vulnList.scrollTop = vulnList.scrollHeight;
}

async function showVulnDetail(id) {
    try {
        const response = await fetch(`/api/vulnerability/${id}`);
        const data = await response.json();
        
        modalTitle.textContent = data.title;
        modalSeverity.textContent = data.severity;
        modalTarget.textContent = data.target || 'N/A';
        modalDescription.textContent = data.description || 'No detailed description available.';
        modalRemediation.textContent = data.remediation || 'Automated remediation steps are being analyzed...';
        
        modal.style.display = 'block';
    } catch (err) {
        console.error('Failed to fetch vulnerability details:', err);
    }
}

closeModal.onclick = () => modal.style.display = 'none';
window.onclick = (e) => { if (e.target == modal) modal.style.display = 'none'; };
