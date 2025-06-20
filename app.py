# Specialized Chatbot Backend API Template
# Students: This file handles the AI logic - you don't need to change much here!
# Focus on customizing the SYSTEM_PROMPT and BUSINESS_INFO sections

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import json
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to talk to backend

# =============================================================================
# STUDENT CUSTOMIZATION SECTION 1: API SETUP
# =============================================================================
# STEP 1: Replace with your Google API key
GOOGLE_API_KEY = "api"

# Configure Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# =============================================================================
# STUDENT CUSTOMIZATION SECTION 2: BUSINESS INFORMATION
# =============================================================================
# Students: Customize this section for YOUR business idea!
# Replace all the example values below with your own business details

BUSINESS_INFO = {
    "business_name": "Your Business Name Here",
    "business_type": "Type of business (e.g., restaurant, bookstore, tech repair)",
    "products_services": [
        "Product or service 1",
        "Product or service 2",
        "Product or service 3",
        "Product or service 4",
        "Product or service 5"
    ],
    "target_customers": "Who are your ideal customers? (e.g., college students, families, gamers)",
    "business_personality": "How should your business sound? (e.g., professional and helpful, fun and energetic, calm and trustworthy)"
}

# =============================================================================
# STUDENT CUSTOMIZATION SECTION 3: CHATBOT PERSONALITY
# =============================================================================
# Students: This is where you define HOW your chatbot should act!

def create_system_prompt():
    """
    Students: This is where you customize your chatbot's personality and behavior!

    INSTRUCTIONS:
    1. Keep the basic structure below - it works well for most businesses
    2. Add 3-5 specific rules for YOUR business in the "CUSTOM BUSINESS RULES" section
    3. Choose 2-3 emojis that represent your business theme
    4. Write 1-2 sentences about what makes your business special

    Think: How would you want a real employee to talk to your customers?
    """

    prompt = f"""
You are a specialized sales and customer service chatbot for {BUSINESS_INFO['business_name']}.

BUSINESS OVERVIEW:
- Business Type: {BUSINESS_INFO['business_type']}
- Products/Services: {', '.join(BUSINESS_INFO['products_services'])}
- Target Customers: {BUSINESS_INFO['target_customers']}
- Personality: {BUSINESS_INFO['business_personality']}

YOUR CHATBOT'S MAIN JOBS - STUDENTS: Customize this list for your specific chatbot purpose!
1. [What should your chatbot do first when someone talks to it?]
2. [What's the second most important thing it should do?]
3. [What's the third most important thing it should do?]
4. [Add more job responsibilities specific to your business - aim for 5-7 total]
5. [Think: Is this a sales bot? Support bot? Information bot? Schedule bot?]

CONVERSATION RULES - STUDENTS: Replace these with rules that fit YOUR chatbot's purpose!
- [Write your first conversation rule - how should it behave?]
- [Write your second conversation rule - what topics should it focus on?]
- [Write your third conversation rule - how should it handle questions?]
- [Write your fourth conversation rule - any special behaviors?]
- [Add more rules as needed - keep it to 4-6 total rules]

RESPONSE STYLE - STUDENTS: Define how your chatbot should "sound" when it talks!
- [How formal or casual should your chatbot be?]
- [What kind of language should it use? (simple, technical, fun, professional?)]
- [Should it use emojis? If so, which ones fit your business?]
- [How long should responses be? (short and quick, detailed explanations?)]
- [Any other style preferences for your specific business?]

CUSTOM BUSINESS RULES - STUDENTS: Replace these with rules specific to YOUR business!
- [Write your first custom rule here - what should your chatbot always do?]
- [Write your second custom rule here - any special offers or policies?]
- [Write your third custom rule here - any important business information?]
- [Add more rules if needed!]

WHAT MAKES YOUR BUSINESS SPECIAL:
[Students: Write 1-2 sentences about what makes your business unique and exciting]

Remember: You represent {BUSINESS_INFO['business_name']} - make customers excited about your business!
"""
    return prompt

# =============================================================================
# CORE BACKEND LOGIC (Students don't need to modify this much)
# =============================================================================

# Store conversation history for each user (in a real app, use a database)
user_conversations = {}

@app.route('/')
def home():
    """Serve the main webpage"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - receives messages from frontend, sends to AI, returns response
    Students: You usually won't need to modify this function
    """
    try:
        # Get the message from the frontend
        data = request.get_json()
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')  # Simple user tracking

        # Validate input
        if not user_message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Initialize conversation for new users
        if user_id not in user_conversations:
            user_conversations[user_id] = model.start_chat(history=[])
            # Send system prompt as first message
            system_prompt = create_system_prompt()
            user_conversations[user_id].send_message(system_prompt)

        # Get the AI response
        chat_session = user_conversations[user_id]
        response = chat_session.send_message(user_message)
        response.resolve()

        # Return the response to frontend
        return jsonify({
            'response': response.text,
            'business_name': BUSINESS_INFO['business_name']
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Something went wrong. Please try again.'}), 500

@app.route('/api/business-info', methods=['GET'])
def get_business_info():
    """
    Send business information to frontend for customization
    Students: Frontend can use this to display business name, colors, etc.
    """
    return jsonify(BUSINESS_INFO)

@app.route('/api/reset-chat', methods=['POST'])
def reset_chat():
    """Reset conversation for a user"""
    data = request.get_json()
    user_id = data.get('user_id', 'default_user')

    if user_id in user_conversations:
        del user_conversations[user_id]

    return jsonify({'message': 'Chat reset successfully'})

# =============================================================================
# STUDENT CUSTOMIZATION SECTION 4: ADDITIONAL FEATURES (OPTIONAL)
# =============================================================================

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Students: Customize this endpoint to return YOUR product information
    Your frontend can use this to display a product catalog

    INSTRUCTIONS:
    1. Replace the example products below with your actual products/services
    2. Add more products if needed
    3. Include real prices, descriptions, and images/emojis
    4. Consider adding categories, ratings, or availability status
    """
    # Example product data - STUDENTS: Replace with your products!
    products = [
        {
            "id": 1,
            "name": "Your Product Name 1",
            "price": "$XX.XX",
            "description": "Brief description of your first product or service",
            "image": "🎯"  # Choose an emoji that represents your product
        },
        {
            "id": 2,
            "name": "Your Product Name 2",
            "price": "$XX.XX",
            "description": "Brief description of your second product or service",
            "image": "⭐"  # Choose an emoji that represents your product
        },
        {
            "id": 3,
            "name": "Your Product Name 3",
            "price": "$XX.XX",
            "description": "Brief description of your third product or service",
            "image": "🚀"  # Choose an emoji that represents your product
        }
        # Add more products here as needed!
    ]
    return jsonify(products)

# =============================================================================
# STUDENT ASSIGNMENT CHECKLIST
# =============================================================================
"""
BEFORE RUNNING YOUR CHATBOT, COMPLETE THESE STEPS:

✅ STEP 1: Get your Google API Key
   - Go to Google AI Studio (https://makersuite.google.com)
   - Create an account and get your API key
   - Replace "YOUR_API_KEY_HERE" above with your actual key

✅ STEP 2: Customize Your Business Info
   - Change business_name to your business name
   - Update business_type with your type of business
   - List your actual products/services
   - Define your target customers
   - Describe your business personality

✅ STEP 3: Customize Your Chatbot Personality
   - Modify the create_system_prompt() function
   - Add special instructions for your business
   - Choose appropriate emojis for your business theme

✅ STEP 4: Update Your Products (Optional)
   - Customize the get_products() function
   - Add your real products with prices and descriptions

✅ STEP 5: Test Your Chatbot
   - Run this file: python app.py
   - Open your browser to http://localhost:5001
   - Test conversations with your chatbot
   - Make sure it stays on topic and represents your business well

BUSINESS IDEAS FOR INSPIRATION:
- Local coffee shop or bakery
- Video game store
- Fitness/yoga studio
- Tutoring service
- Food truck
- Bookstore
- Hair salon
- Tech repair shop
- Handmade jewelry store
- Pet grooming service
- Photography studio
- Music lessons
- Bike repair shop
- Home cleaning service
- Personal training
- Art supply store
"""

# =============================================================================
# RUN THE SERVER
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print(f"🚀 Starting {BUSINESS_INFO['business_name']} Chatbot Server")
    print("=" * 60)
    print("📝 STUDENT CHECKLIST:")
    print("□ 1. Add your Google API key")
    print("□ 2. Customize BUSINESS_INFO with your business details")
    print("□ 3. Modify create_system_prompt() for your chatbot personality")
    print("□ 4. Update get_products() with your actual products (optional)")
    print("□ 5. Design your frontend in templates/index.html")
    print("□ 6. Test your chatbot thoroughly!")
    print("=" * 60)
    print("💡 Need help? Check the comments and instructions in this file!")
    print("=" * 60)

    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    app.run(debug=True, host='0.0.0.0', port=5001)