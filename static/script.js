// =================================================================
// STUDENT CUSTOMIZATION SECTION 1: JAVASCRIPT VARIABLES
// Students: Modify these variables for your business
// =================================================================

let businessInfo = {};
const userId = 'user_' + Math.random().toString(36).substr(2, 9); // Simple user ID

// Students: Customize these messages for your business
const welcomeMessages = [
    "Welcome! How can I help you today?",
    "Add your own messages!",
];

// Students: Customize loading messages
const loadingMessages = [
    "Let me think about that...",
    "Add your own messages!",
];

// =================================================================
// INITIALIZATION - RUNS WHEN PAGE LOADS
// =================================================================

window.onload = function() {
    console.log("🚀 Chatbot starting up...");
    loadBusinessInfo();
    addWelcomeMessage();
    setupEnterKeyListener();
    setupInputValidation();
};

// =================================================================
// BUSINESS INFORMATION LOADING
// =================================================================

// Load business information from backend
async function loadBusinessInfo() {
    try {
        console.log("📊 Loading business information...");
        const response = await fetch('/api/business-info');
        businessInfo = await response.json();

        // Update page with business info
        document.getElementById('businessName').textContent = businessInfo.business_name;
        document.getElementById('businessDescription').textContent = businessInfo.business_type;

        // Students: Customize the logo emoji based on business type
        const logoEmojis = {
            'pet': '🐦',
            'food': '🍕',
            'Add your own!': 'Emoji goes here!',
            'default': '🏪'
        };

        // Auto-detect emoji based on business type
        let logoEmoji = logoEmojis.default;
        const businessType = businessInfo.business_type.toLowerCase();

        for (const [key, emoji] of Object.entries(logoEmojis)) {
            if (businessType.includes(key)) {
                logoEmoji = emoji;
                break;
            }
        }

        document.getElementById('businessLogo').textContent = logoEmoji;

        // Update page title
        document.title = `${businessInfo.business_name} - AI Assistant`;

        console.log("✅ Business information loaded successfully!");

    } catch (error) {
        console.error('❌ Error loading business info:', error);
        // Fallback if API fails
        document.getElementById('businessName').textContent = 'Your Business Chatbot';
        document.getElementById('businessDescription').textContent = 'AI-powered customer service';
    }
}

// =================================================================
// WELCOME MESSAGE HANDLING
// =================================================================

// Add welcome message when page loads
function addWelcomeMessage() {
    const randomWelcome = welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)];
    setTimeout(() => {
        addMessage('bot', randomWelcome);
    }, 500); // Small delay for better UX
}

// =================================================================
// CORE CHAT FUNCTIONS
// =================================================================

// Send message to backend and display response
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    // Validate input
    if (!message) {
        highlightEmptyInput();
        return;
    }

    // Disable send button and show user message
    setSendButtonState(false);
    addMessage('user', message);
    input.value = '';

    // Show typing indicator
    showTypingIndicator(true);

    try {
        console.log("📤 Sending message to backend:", message);

        // Send to backend API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                user_id: userId
            })
        });

        const data = await response.json();

        if (response.ok) {
            console.log("📥 Received response from backend");
            // Add bot response with typing effect
            await addMessageWithTypingEffect('bot', data.response);
        } else {
            console.error("❌ Backend error:", data.error);
            addMessage('bot', 'Sorry, I encountered an error. Please try again! 😅');
        }

    } catch (error) {
        console.error('❌ Network error:', error);
        addMessage('bot', 'Sorry, I had trouble connecting. Please check your internet and try again! 🌐');
    } finally {
        showTypingIndicator(false);
        setSendButtonState(true);
        input.focus(); // Return focus to input for better UX
    }
}

// Quick message buttons
function sendQuickMessage(message) {
    const input = document.getElementById('messageInput');
    input.value = message;
    sendMessage();
}

// =================================================================
// MESSAGE DISPLAY FUNCTIONS
// =================================================================

// Add message to chat with animation
function addMessage(sender, text) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const avatar = sender === 'user' ? '👤' : '🤖';

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">${formatMessage(text)}</div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add message with typing effect (makes bot seem more natural)
async function addMessageWithTypingEffect(sender, text) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const avatar = sender === 'user' ? '👤' : '🤖';

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content"></div>
    `;

    chatMessages.appendChild(messageDiv);
    const contentDiv = messageDiv.querySelector('.message-content');

    // Type out the message character by character
    const formattedText = formatMessage(text);
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = formattedText;
    const plainText = tempDiv.textContent || tempDiv.innerText || '';

    for (let i = 0; i <= plainText.length; i++) {
        contentDiv.textContent = plainText.substring(0, i);
        scrollToBottom();
        await new Promise(resolve => setTimeout(resolve, 20)); // Typing speed
    }

    // Set final formatted content
    contentDiv.innerHTML = formattedText;
    scrollToBottom();
}

// =================================================================
// MESSAGE FORMATTING
// =================================================================

// Format message text (add emojis, links, etc.)
function formatMessage(text) {
    // Students: Add custom formatting rules here

    // Make URLs clickable
    text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');

    // Make email addresses clickable
    text = text.replace(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/g, '<a href="mailto:$1">$1</a>');

    // Make phone numbers clickable
    text = text.replace(/(\d{3}-\d{3}-\d{4})/g, '<a href="tel:$1">$1</a>');

    // Convert newlines to line breaks
    text = text.replace(/\n/g, '<br>');

    return text;
}

// =================================================================
// UTILITY FUNCTIONS
// =================================================================

function setSendButtonState(enabled) {
    const button = document.getElementById('sendButton');
    button.disabled = !enabled;
    button.textContent = enabled ? 'Send 🚀' : 'Sending...';
}

function showTypingIndicator(show) {
    const indicator = document.getElementById('typingIndicator');
    indicator.style.display = show ? 'block' : 'none';

    if (show) {
        scrollToBottom();
    }
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function setupEnterKeyListener() {
    document.getElementById('messageInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

function setupInputValidation() {
    const input = document.getElementById('messageInput');

    // Remove error highlighting when user starts typing
    input.addEventListener('input', function() {
        input.classList.remove('error');
    });
}

function highlightEmptyInput() {
    const input = document.getElementById('messageInput');
    input.classList.add('error');
    input.focus();

    // Add error style if not already defined
    if (!document.querySelector('.error-style')) {
        const style = document.createElement('style');
        style.className = 'error-style';
        style.textContent = `
            .error {
                border-color: #ff4444 !important;
                box-shadow: 0 0 0 3px rgba(255, 68, 68, 0.1) !important;
                animation: shake 0.5s ease-in-out;
            }
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-5px); }
                75% { transform: translateX(5px); }
            }
        `;
        document.head.appendChild(style);
    }
}

// =================================================================
// STUDENT CUSTOMIZATION SECTION 2: ADD YOUR OWN FUNCTIONS HERE!
// =================================================================

// Students: Add your custom JavaScript functions below this line

// Example: Function to show business hours
function showBusinessHours() {
    const hours = {
        'Monday': '9:00 AM - 8:00 PM',
        'Tuesday': 'Fill in!',
        'Wednesday': 'Fill in!',
        'Thursday': 'Fill in!',
        'Friday': 'Fill in!',
        'Saturday': 'Fill in!',
        'Sunday': 'Fill in!'
    };

    let hoursText = "Our business hours:\n";
    for (const [day, time] of Object.entries(hours)) {
        hoursText += `${day}: ${time}\n`;
    }

    addMessage('bot', hoursText);
}

// Example: Function to show product catalog
function showProductCatalog() {
    // Students: Customize this for your business
    const products = [
        "🐦 Colorful Parakeets - $25",
        "🏠 Add your own! - $Fill in!",
    ];

    let catalogText = "Here are our featured products:\n\n";
    products.forEach(product => {
        catalogText += product + "\n";
    });

    addMessage('bot', catalogText);
}

// Example: Function to handle special keywords
function handleSpecialKeywords(message) {
    const lowerMessage = message.toLowerCase();

    if (lowerMessage.includes('hours') || lowerMessage.includes('open')) {
        showBusinessHours();
        return true;
    }

    if (lowerMessage.includes('catalog') || lowerMessage.includes('products')) {
        showProductCatalog();
        return true;
    }

    return false;
}

// Example: Function to change chat theme
function changeTheme(themeName) {
    const root = document.documentElement;

    const themes = {
        'dark': {
            '--primary-color': '#2c3e50',
            '--secondary-color': '#34495e',
            '--background-color': '#1a1a1a',
            '--chat-bg': '#2c2c2c',
            '--text-color': '#ffffff'
        },
        'ocean': {
            '--primary-color': '#3498db',
            '--secondary-color': '#2980b9',
            '--background-color': '#e8f4f8',
            '--chat-bg': '#ffffff',
            '--text-color': '#2c3e50'
        },
        'forest': {
            '--primary-color': '#27ae60',
            '--secondary-color': '#229954',
            '--background-color': '#e8f5e8',
            '--chat-bg': '#ffffff',
            '--text-color': '#2c3e50'
        }
    };

    if (themes[themeName]) {
        for (const [property, value] of Object.entries(themes[themeName])) {
            root.style.setProperty(property, value);
        }
    }
}

// =================================================================
// ADVANCED FEATURES (OPTIONAL)
// =================================================================

// Function to save chat history (uses local storage)
function saveChatHistory() {
    const messages = Array.from(document.querySelectorAll('.message')).map(msg => ({
        sender: msg.classList.contains('user') ? 'user' : 'bot',
        content: msg.querySelector('.message-content').textContent,
        timestamp: new Date().toISOString()
    }));

    localStorage.setItem('chatHistory', JSON.stringify(messages));
}

// Function to load chat history
function loadChatHistory() {
    const history = localStorage.getItem('chatHistory');
    if (history) {
        const messages = JSON.parse(history);
        messages.forEach(msg => {
            addMessage(msg.sender, msg.content);
        });
    }
}

// Function to clear chat
function clearChat() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = '';
    localStorage.removeItem('chatHistory');
    addWelcomeMessage();
}

// Function to export chat as text
function exportChat() {
    const messages = Array.from(document.querySelectorAll('.message')).map(msg => {
        const sender = msg.classList.contains('user') ? 'You' : businessInfo.business_name || 'Bot';
        const content = msg.querySelector('.message-content').textContent;
        return `${sender}: ${content}`;
    });

    const chatText = messages.join('\n\n');
    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'chat-history.txt';
    a.click();
    URL.revokeObjectURL(url);
}

console.log("✅ Chatbot JavaScript loaded successfully!");