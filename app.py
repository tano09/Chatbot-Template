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
    "business_name": "Paws & Shine Dog Grooming",
    "business_type": "Dog grooming service",
    "phone": "(555) 123-PAWS",
    "email": "info@pawsandshine.com",
    "address": "123 Dog Street, Pet City, PC 12345",
    "products_services": [
        "Basic grooming package",
        "Deluxe grooming package",
        "Nail trimming",
        "Ear cleaning",
        "Teeth brushing"
    ],
    "target_customers": "Dog owners who want their pets to look and feel their best, but can also work with cats",
    "business_personality": "Friendly, caring, and professional with a touch of fun"
}

# =============================================================================
# STUDENT CUSTOMIZATION SECTION 3: CHATBOT PERSONALITY
# =============================================================================
# Students: This is where you define HOW your chatbot should act!

def create_system_prompt():
    """
    Customizes the chatbot's personality and behavior for a dog grooming business.
    """

    prompt = f"""
You are a specialized sales and customer service chatbot for {BUSINESS_INFO['business_name']}.

BUSINESS OVERVIEW:
- Business Type: {BUSINESS_INFO['business_type']}
- Products/Services: {', '.join(BUSINESS_INFO['products_services'])}
- Target Customers: {BUSINESS_INFO['target_customers']}
- Personality: {BUSINESS_INFO['business_personality']}

YOUR CHATBOT'S MAIN JOBS:
1. Greet customers warmly and ask how you can assist them.
2. Provide detailed information about grooming packages and services.
3. Answer questions about pricing, appointment scheduling, and pet care tips.
4. Promote special offers or discounts for loyal customers.
5. Ensure customers feel confident and excited about bringing their pets to {BUSINESS_INFO['business_name']}.

CONVERSATION RULES:
- Always be friendly and empathetic, as if you're talking to a fellow dog lover.
- Focus on dog grooming topics and avoid unrelated subjects.
- Provide clear and concise answers to questions.
- Use emojis like 🐾, 🐶, and ✂️ to make responses more engaging.
- Offer helpful tips for dog care when appropriate.

RESPONSE STYLE:
- Casual and approachable, but professional.
- Use simple language that is easy for all customers to understand.
- Include emojis to add a playful tone (e.g., 🐾, 🐶, ✂️).
- Keep responses concise but informative.

CUSTOM BUSINESS RULES:
- Always highlight the importance of regular grooming for a dog's health and happiness.
- Mention any seasonal promotions or discounts.
- Provide reassurance about the safety and comfort of pets during grooming sessions.

WHAT MAKES YOUR BUSINESS SPECIAL:
At {BUSINESS_INFO['business_name']}, we treat every dog like family. Our experienced groomers ensure your furry friends look and feel their best, all while enjoying a stress-free grooming experience. 🐾
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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# =============================================================================
# STUDENT CUSTOMIZATION SECTION 4: ADDITIONAL FEATURES (OPTIONAL)
# =============================================================================

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Returns product information for the dog grooming business.
    """
    products = [
        {
            "id": 1,
            "name": "Basic Grooming Package",
            "price": "$25.00",
            "description": "Includes a bath, brushing, and nail trimming for your pup.",
            "image": "🛁"  # Represents grooming services
        },
        {
            "id": 2,
            "name": "Deluxe Grooming Package",
            "price": "$50.00",
            "description": "Includes a bath, brushing, nail trimming, ear cleaning, and teeth brushing.",
            "image": "✨"  # Represents deluxe services
        },
        {
            "id": 3,
            "name": "Nail Trimming",
            "price": "$10.00",
            "description": "Professional nail trimming to keep your dog's paws healthy.",
            "image": "✂️"  # Represents nail trimming
        },
        {
            "id": 4,
            "name": "Ear Cleaning",
            "price": "$15.00",
            "description": "Gentle ear cleaning to prevent infections and discomfort.",
            "image": "👂"  # Represents ear cleaning
        },
        {
            "id": 5,
            "name": "Teeth Brushing",
            "price": "$20.00",
            "description": "Keep your dog's teeth clean and healthy with our brushing service.",
            "image": "🦷"  # Represents teeth brushing
        }
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

✅ STEP 3: Customize Your Chatbot PersonalityPersonality
   - Modify the create_system_prompt() function
   - Add special instructions for your businessness
   - Choose appropriate emojis for your business theme

✅ STEP 4: Update Your Products (Optional)al)
   - Customize the get_products() function
   - Add your real products with prices and descriptionsions

✅ STEP 5: Test Your Chatbot
   - Run this file: python app.py
   - Open your browser to http://localhost:5001   - Open your browser to http://localhost:5001
   - Test conversations with your chatbot
   - Make sure it stays on topic and represents your business well your business well

BUSINESS IDEAS FOR INSPIRATION:
- Local coffee shop or bakery- Local coffee shop or bakery
- Video game store
- Fitness/yoga studio
- Tutoring service
- Food truck- Food truck
- Bookstore
- Hair salon
- Tech repair shop
- Handmade jewelry store
- Pet grooming service
- Photography studio- Photography studio
- Music lessons
- Bike repair shop
- Home cleaning servicervice
- Personal training
- Art supply store
"""

# ================================================================================================================================================
# RUN THE SERVER
# ====================================================================================================================================

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