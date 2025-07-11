# MADE WITH AI
# 🚀 Specialized Business Chatbot - Full Stack Project

## 📋 Project Overview
Create your own specialized business chatbot! Students will design both the backend AI logic and frontend interface for their unique business idea.

## 🎯 Learning Objectives
* **Backend Development**: Python Flask API, AI integration
* **Frontend Development**: HTML, CSS, JavaScript
* **Business Planning**: Define target customers, products, personality
* **Full-Stack Communication**: API design and frontend-backend integration

## 🛠️ Setup Instructions

### Step 1: Install Python Dependencies
```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Get Google AI API Key
1. Go to [Google AI Studio](https://makersuite.google.com)
2. Create a new API key
3. Copy your API key

### Step 3: Add Your API Key
In `app.py`, replace:
```python
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
```
With your actual API key.

### Step 4: Run Your Chatbot
```bash
python app.py
```
Visit: http://localhost:5001

## 🎨 Student Customization Guide

### 1. Define Your Business (app.py)
**Edit the BUSINESS_INFO section:**
```python
BUSINESS_INFO = {
    "business_name": "Your Awesome Business",
    "business_type": "What type of business (e.g., pet store, restaurant, bookstore)",
    "products_services": [
        "Product 1",
        "Product 2", 
        "Service 1"
    ],
    "target_customers": "Who are your customers?",
    "business_personality": "How should your chatbot act? (friendly, professional, funny, etc.)"
}
```

**Examples of Business Ideas:**
* 🐕 Pet Store: "Paws & Claws Pet Emporium"
* 🍕 Pizza Restaurant: "Tony's Authentic Italian Pizza"
* 📚 Bookstore: "The Reading Nook"
* 🎮 Gaming Store: "Level Up Games"
* 👕 Clothing: "Trendy Threads Boutique"
* 🎵 Music Store: "Melody Makers Music Shop"

### 2. Customize Chatbot Personality (app.py)
**Edit the `create_system_prompt()` function:**
* Change how your chatbot greets customers
* Add specific knowledge about your products
* Define conversation rules
* Set the tone (formal, casual, enthusiastic, etc.)

### 3. Design Your Frontend (templates/index.html)
**Change Colors & Theme:**
```css
:root {
    --primary-color: #your-color;      /* Main brand color */
    --secondary-color: #darker-shade;   /* Hover effects */
    --accent-color: #highlight-color;   /* Special elements */
    --background-color: #page-bg;       /* Page background */
}
```

**Update Business Logo & Header:**
* Change the emoji in business-logo
* Modify header text and descriptions
* Add your business slogan

**Customize Quick Buttons:**
```html
<button class="quick-button" onclick="sendQuickMessage('Your question here')">
    Button Text 🔥
</button>
```

## 🏗️ Project Structure
```
chatbot-project/
├── app.py                 # Backend Python code (Flask API)
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates folder
│   └── index.html        # Main webpage structure
├── static/                # Static files (CSS, JS, images)
│   ├── style.css         # All styling and colors
│   └── script.js         # All JavaScript functionality
└── venv/                  # Virtual environment (auto-created)
```

## 🎓 Student Assignment Ideas

### Beginner Level
- [ ] Set up the basic chatbot with your business information
- [ ] Change colors and business name
- [ ] Add 3-5 products/services to your business
- [ ] Test conversations and make sure chatbot stays on topic

### Intermediate Level
- [ ] Create custom quick-start buttons for common questions
- [ ] Add business hours and location information
- [ ] Implement a product catalog display
- [ ] Add special promotions or offers to your chatbot

### Advanced Level
- [ ] Create multiple conversation flows (sales, support, information)
- [ ] Add conversation memory and user preferences
- [ ] Implement appointment booking or order processing
- [ ] Add analytics to track popular questions
- [ ] Create mobile-responsive design improvements

## 📁 File Descriptions

### `app.py` - Backend Server
- **Main Flask application** that handles all server logic
- **AI Integration** using Google's Gemini AI
- **API Endpoints** for chat, business info, and products
- **Conversation Management** with memory for each user

### `templates/index.html` - Frontend Structure
- **Main webpage** that users interact with
- **Chat interface** with message bubbles and input
- **Business branding** area with logo and description
- **Quick action buttons** for common questions

### `requirements.txt` - Dependencies
```
flask==2.3.2
flask-cors==4.0.0
google-generativeai==0.3.0
```

## 🚨 Common Issues & Solutions

### "Module not found" Error
```bash
# Make sure you activated your virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### API Key Issues
- Make sure you copied the entire API key (no extra spaces)
- Check that your Google AI Studio account is active
- Try generating a new API key if the current one doesn't work

### Port Already in Use
If port 5001 is busy, change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Use a different port
```

## 🎉 Demo Your Project
1. **Business Pitch**: Explain your business idea and target customers
2. **Chatbot Demo**: Show conversations that highlight your chatbot's personality
3. **Design Showcase**: Walk through your color choices and branding
4. **Technical Explanation**: Explain one customization you made and why

## 🤝 Contributing
This is a student project template. Feel free to:
* Submit improvements to the template
* Share creative business ideas
* Report bugs or issues
* Add new features for other students to use

## 📄 License
This project is for educational purposes. Students are free to use and modify for learning.

---

**Need help?** Check the comments in the code files - they contain detailed instructions for each section you need to customize!
