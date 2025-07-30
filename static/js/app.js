// Irish Domestic Violence Support Chatbot - Frontend JavaScript
// Trauma-informed interface with safety features

class DVSupportChatbot {
    constructor() {
        this.messageInput = document.getElementById('message-input');
        this.sendBtn = document.getElementById('send-btn');
        this.chatMessages = document.getElementById('chat-messages');
        this.charCount = document.querySelector('.char-count');
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.crisisModal = document.getElementById('crisis-modal');
        
        this.isProcessing = false;
        this.maxMessageLength = 500;
        this.responseLength = 'adaptive';  // Default response length
        
        this.initializeEventListeners();
        this.setupKeyboardShortcuts();
    }
    
    initializeEventListeners() {
        // Send button
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Enter key to send (Shift+Enter for new line)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Character counter
        this.messageInput.addEventListener('input', () => this.updateCharCount());
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => this.autoResizeTextarea());
        
        // Clear on focus (for accessibility)
        this.messageInput.addEventListener('focus', () => {
            if (this.messageInput.value.trim() === '') {
                this.messageInput.style.height = 'auto';
            }
        });
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+L or Cmd+L to clear history
            if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
                e.preventDefault();
                this.clearHistory();
            }
            
            // Escape for quick exit
            if (e.key === 'Escape') {
                e.preventDefault();
                this.showQuickExitConfirm();
            }
        });
    }
    
    updateCharCount() {
        const currentLength = this.messageInput.value.length;
        this.charCount.textContent = `${currentLength}/${this.maxMessageLength}`;
        
        // Update styling based on character count
        if (currentLength > this.maxMessageLength * 0.9) {
            this.charCount.style.color = '#d32f2f';
        } else if (currentLength > this.maxMessageLength * 0.7) {
            this.charCount.style.color = '#f57c00';
        } else {
            this.charCount.style.color = '#666';
        }
        
        // Disable send button if over limit
        this.sendBtn.disabled = currentLength > this.maxMessageLength || currentLength === 0;
    }
    
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || this.isProcessing || message.length > this.maxMessageLength) {
            return;
        }
        
        this.isProcessing = true;
        this.showLoading();
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        this.updateCharCount();
        this.autoResizeTextarea();
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: message,
                    response_length: this.responseLength 
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Add bot response
            this.addMessage(data.message, 'bot', {
                sources: data.sources,
                isCrisis: data.is_crisis,
                ragType: data.rag_type,
                modelUsed: data.model_used
            });
            
            // Show crisis modal if needed
            if (data.is_crisis) {
                this.showCrisisModal();
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage(
                `I'm having trouble responding right now. For immediate support, please contact:

**Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
**Emergency: 999 or 112**

Your safety is the priority.`,
                'bot',
                { isError: true }
            );
        } finally {
            this.hideLoading();
            this.isProcessing = false;
            this.messageInput.focus();
        }
    }
    
    addMessage(content, sender, options = {}) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Apply crisis styling if needed
        if (options.isCrisis) {
            messageContent.classList.add('crisis-message');
        }
        
        // Convert markdown-like formatting to HTML
        const formattedContent = this.formatMessage(content);
        messageContent.innerHTML = formattedContent;
        
        // Add sources if available
        if (options.sources && options.sources.length > 0) {
            const sourcesDiv = this.createSourcesElement(options.sources);
            messageContent.appendChild(sourcesDiv);
        }
        
        // Add timestamp and model info
        const timestamp = document.createElement('div');
        timestamp.className = 'timestamp';
        timestamp.style.fontSize = '0.7em';
        timestamp.style.color = '#999';
        timestamp.style.marginTop = '5px';
        
        let timestampText = new Date().toLocaleTimeString();
        if (sender === 'bot' && options.ragType) {
            const modelInfo = options.ragType === 'full' ? 
                `AI: ${options.modelUsed}` : 'Template Response';
            timestampText += ` • ${modelInfo}`;
        }
        
        timestamp.textContent = timestampText;
        messageContent.appendChild(timestamp);
        
        messageDiv.appendChild(messageContent);
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    formatMessage(content) {
        return content
            // Bold text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Phone number links
            .replace(/(\d{3,4} \d{3} \d{3,4})/g, '<a href="tel:$1">$1</a>')
            // Emergency numbers
            .replace(/\b(999|112)\b/g, '<a href="tel:$1" style="color: #d32f2f; font-weight: bold;">$1</a>')
            // Line breaks
            .replace(/\n/g, '<br>')
            // Lists (simple implementation)
            .replace(/^- (.*$)/gm, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }
    
    createSourcesElement(sources) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'sources';
        
        const sourcesTitle = document.createElement('h5');
        sourcesTitle.textContent = `📚 Sources (${sources.length}):`;
        sourcesDiv.appendChild(sourcesTitle);
        
        sources.slice(0, 3).forEach((source, index) => {
            const sourceItem = document.createElement('div');
            sourceItem.className = 'source-item';
            
            const relevance = Math.round(source.relevance * 100);
            sourceItem.innerHTML = `
                ${index + 1}. [${source.organization}] ${source.content_type} 
                (${source.location || 'National'}) - Relevance: ${relevance}%
            `;
            
            sourcesDiv.appendChild(sourceItem);
        });
        
        return sourcesDiv;
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    showLoading() {
        this.loadingOverlay.style.display = 'flex';
        this.sendBtn.disabled = true;
        this.sendBtn.textContent = 'Sending...';
    }
    
    hideLoading() {
        this.loadingOverlay.style.display = 'none';
        this.sendBtn.disabled = false;
        this.sendBtn.textContent = 'Send';
    }
    
    showCrisisModal() {
        this.crisisModal.style.display = 'flex';
        
        // Focus management for accessibility
        const firstButton = this.crisisModal.querySelector('a');
        if (firstButton) {
            firstButton.focus();
        }
    }
    
    async clearHistory() {
        if (!confirm('Clear chat history? This will remove all messages from this session.')) {
            return;
        }
        
        try {
            const response = await fetch('/api/clear-history', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                // Clear messages except welcome message
                const messages = this.chatMessages.querySelectorAll('.message');
                messages.forEach((message, index) => {
                    if (index > 0) { // Keep first (welcome) message
                        message.remove();
                    }
                });
                
                this.showNotification('Chat history cleared', 'success');
            }
        } catch (error) {
            console.error('Error clearing history:', error);
            this.showNotification('Error clearing history', 'error');
        }
    }
    
    showQuickExitConfirm() {
        if (confirm('Quick Exit will clear your session and take you to Google. Continue?')) {
            quickExit();
        }
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: ${type === 'error' ? '#d32f2f' : '#388e3c'};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1002;
            font-weight: 500;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Global functions
async function quickExit() {
    try {
        // Clear session on server
        await fetch('/api/quick-exit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        // Clear browser data
        if ('serviceWorker' in navigator) {
            const registrations = await navigator.serviceWorker.getRegistrations();
            for (let registration of registrations) {
                registration.unregister();
            }
        }
        
        // Clear localStorage and sessionStorage
        localStorage.clear();
        sessionStorage.clear();
        
        // Replace current page in history and redirect
        window.location.replace('https://www.google.ie');
        
    } catch (error) {
        console.error('Quick exit error:', error);
        // Fallback - direct redirect
        window.location.replace('https://www.google.ie');
    }
}

function closeCrisisModal() {
    document.getElementById('crisis-modal').style.display = 'none';
}

function clearHistory() {
    chatbot.clearHistory();
}

// Global sendMessage function to match HTML onclick
function sendMessage() {
    if (chatbot) {
        chatbot.sendMessage();
    }
}

// Global function to set response length
function setResponseLength(length) {
    if (chatbot) {
        chatbot.responseLength = length;
        
        // Update button styling
        document.querySelectorAll('.length-btn').forEach(btn => btn.classList.remove('active'));
        document.getElementById(`${length}-btn`).classList.add('active');
        
        // Show notification
        const lengthNames = {
            'brief': 'Brief responses',
            'adaptive': 'Balanced responses', 
            'detailed': 'Detailed responses'
        };
        chatbot.showNotification(`Switched to ${lengthNames[length]}`, 'info');
    }
}

// Initialize chatbot when DOM is loaded
let chatbot;
document.addEventListener('DOMContentLoaded', () => {
    chatbot = new DVSupportChatbot();
    
    // Initial character count update
    chatbot.updateCharCount();
    
    // Focus on input
    chatbot.messageInput.focus();
    
    // Add visibility change handler for security
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            // Page is now hidden - could implement additional security measures
            console.log('Page hidden - ensuring privacy');
        } else {
            // Page is now visible
            console.log('Page visible - focus restored');
            if (chatbot.messageInput) {
                chatbot.messageInput.focus();
            }
        }
    });
});

// Prevent accidental navigation
window.addEventListener('beforeunload', (e) => {
    // Only show warning if user has sent messages
    const hasMessages = document.querySelectorAll('.user-message').length > 0;
    if (hasMessages) {
        e.preventDefault();
        e.returnValue = 'Are you sure you want to leave? Your chat history will be lost.';
        return e.returnValue;
    }
});