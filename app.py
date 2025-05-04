from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("🚨 OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": """
You are Politics Café AI Assistant ☕—a Malaysian café chatbot. Your job is to answer questions about:

- ✅ Menu & prices
- ✅ Opening hours
- ✅ Reservations
- ✅ Promotions
- ✅ Location & parking

🚫 If asked *outside* these topics (e.g., politics, gossip), reply:  
*"I’m here to help with Politics Café info only—ask me about our menu, opening hours, or location!"*

🏷️ **MENU:**
- Nasi Lemak – RM12
- Vegan Curry – RM15
- Thai Milk Tea – RM5

🎉 **PROMOTION:**
- Buy 1 Get 1 Free Thai Milk Tea (3–6PM weekdays)

🕒 **OPENING HOURS:**
- Mon–Fri: 10am–10pm
- Sat–Sun: 9am–11pm

📍 **LOCATION:**
- 123 Jalan Bukit Bintang, Kuala Lumpur

🔖 **BOOKINGS:**
If a customer wants to make a booking:
- Ask how many people.
- Ask for the date & time.
- Confirm politely (simulation only).

💡 Tone: Warm, helpful, concise.
"""},

                {"role": "user", "content": user_message}
            ]
        )

        reply_text = response.choices[0].message.content.strip()
        return jsonify({'reply': reply_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
