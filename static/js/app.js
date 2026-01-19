// AAA Generator Tool - JavaScript

// DOM Elements
const form = document.getElementById('generatorForm');
const outputArea = document.getElementById('outputArea');
const loadingIndicator = document.getElementById('loadingIndicator');
const copyBtn = document.getElementById('copyBtn');
const loadExampleBtn = document.getElementById('loadExampleBtn');
const exampleModal = document.getElementById('exampleModal');
const closeModalBtn = document.getElementById('closeModal');
const exampleList = document.getElementById('exampleList');

// Form submission handler
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const activityId = document.getElementById('activityId').value;
    const activityName = document.getElementById('activityName').value;
    const documentation = document.getElementById('documentation').value;
    
    // Show loading, hide output
    outputArea.style.display = 'none';
    loadingIndicator.style.display = 'block';
    copyBtn.style.display = 'none';
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                activity_id: activityId,
                activity_name: activityName,
                documentation: documentation
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResult(data.result);
        } else {
            displayError(data.error || 'An error occurred');
        }
    } catch (error) {
        displayError('Failed to connect to server: ' + error.message);
    } finally {
        loadingIndicator.style.display = 'none';
        outputArea.style.display = 'block';
    }
});

// Display successful result
function displayResult(markdown) {
    outputArea.innerHTML = `<div id="outputContent">${markdownToHtml(markdown)}</div>`;
    copyBtn.style.display = 'inline-flex';
    
    // Store the markdown for copying
    copyBtn.dataset.markdown = markdown;
}

// Display error message
function displayError(message) {
    outputArea.innerHTML = `
        <div class="empty-state" style="color: var(--danger-color);">
            <i class="fas fa-exclamation-circle"></i>
            <p><strong>Error:</strong> ${message}</p>
        </div>
    `;
}

// Simple markdown to HTML converter
function markdownToHtml(markdown) {
    let html = markdown;
    
    // Headers
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    
    // Bold
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    // Italic/Emphasis
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    
    // Lists - ordered
    html = html.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ol>$&</ol>');
    
    // Lists - unordered
    html = html.replace(/^[-*]\s+(.+)$/gm, '<li>$1</li>');
    
    // Paragraphs
    html = html.split('\n\n').map(para => {
        if (!para.match(/^<[^>]+>/)) {
            return '<p>' + para.replace(/\n/g, '<br>') + '</p>';
        }
        return para;
    }).join('\n');
    
    return html;
}

// Copy to clipboard functionality
copyBtn.addEventListener('click', async () => {
    const markdown = copyBtn.dataset.markdown;
    
    try {
        await navigator.clipboard.writeText(markdown);
        showSuccessMessage('Copied to clipboard!');
        
        // Change button text temporarily
        const originalHTML = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        copyBtn.style.background = 'var(--success-color)';
        
        setTimeout(() => {
            copyBtn.innerHTML = originalHTML;
            copyBtn.style.background = '';
        }, 2000);
    } catch (error) {
        showSuccessMessage('Failed to copy: ' + error.message, true);
    }
});

// Show success/error message
function showSuccessMessage(message, isError = false) {
    const existingMsg = document.querySelector('.success-message');
    if (existingMsg) {
        existingMsg.remove();
    }
    
    const msg = document.createElement('div');
    msg.className = 'success-message';
    if (isError) {
        msg.style.background = 'var(--danger-color)';
    }
    msg.innerHTML = `<i class="fas fa-${isError ? 'exclamation-circle' : 'check-circle'}"></i> ${message}`;
    msg.style.display = 'flex';
    
    copyBtn.parentElement.appendChild(msg);
    
    setTimeout(() => {
        msg.style.opacity = '0';
        setTimeout(() => msg.remove(), 300);
    }, 3000);
}

// Load examples
loadExampleBtn.addEventListener('click', async () => {
    exampleModal.style.display = 'block';
    
    try {
        const response = await fetch('/api/examples');
        const data = await response.json();
        
        if (data.success) {
            displayExamples(data.examples);
        } else {
            exampleList.innerHTML = '<p>Failed to load examples</p>';
        }
    } catch (error) {
        exampleList.innerHTML = '<p>Failed to load examples: ' + error.message + '</p>';
    }
});

// Display examples in modal
function displayExamples(examples) {
    exampleList.innerHTML = examples.map((example, index) => `
        <div class="example-item" data-index="${index}">
            <h4><i class="fas fa-file-alt"></i> ${example.name}</h4>
            <p><span class="example-id">ID:</span> ${example.activity_id}</p>
            <p><span class="example-id">Name:</span> ${example.activity_name}</p>
        </div>
    `).join('');
    
    // Add click handlers to examples
    document.querySelectorAll('.example-item').forEach(item => {
        item.addEventListener('click', () => {
            const index = parseInt(item.dataset.index);
            loadExample(examples[index]);
        });
    });
}

// Load example into form
function loadExample(example) {
    document.getElementById('activityId').value = example.activity_id;
    document.getElementById('activityName').value = example.activity_name;
    document.getElementById('documentation').value = example.documentation;
    
    exampleModal.style.display = 'none';
    
    // Show a hint
    showSuccessMessage('Example loaded! Click "Generate AAA Block" to see the result.');
}

// Close modal
closeModalBtn.addEventListener('click', () => {
    exampleModal.style.display = 'none';
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === exampleModal) {
        exampleModal.style.display = 'none';
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        form.dispatchEvent(new Event('submit'));
    }
    
    // Escape to close modal
    if (e.key === 'Escape' && exampleModal.style.display === 'block') {
        exampleModal.style.display = 'none';
    }
});

// Auto-resize textarea
const textarea = document.getElementById('documentation');
textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.max(200, this.scrollHeight) + 'px';
});

console.log('AAA Generator Tool loaded successfully!');
