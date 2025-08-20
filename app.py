import os
import requests
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
API_KEY = "AIzaSyCVAM4Gcdd_s3lQpzX-jX7DYE0tY0plFD8"

@app.route('/')
def home():
    """
    Renders the home page, which is our chatbot's front end.
    """
    return render_template('index.html')

@app.route('/medical-chat', methods=['POST'])
def medical_chat():
    """
    This is the API endpoint that the chatbot's frontend will call.
    It receives the user's message, sends it to the Gemini API,
    and returns the generated response.
    """
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"You are a helpful and professional medical AI assistant. You are not a replacement for a doctor. Always advise the user to consult a healthcare professional for diagnosis and treatment. Respond to the following medical query: {user_message}"
                        }
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload)
        response.raise_for_status() 

        result = response.json()
        
        bot_response = result["candidates"][0]["content"]["parts"][0]["text"]
        
        return jsonify({"response": bot_response})

    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return jsonify({"error": "An error occurred while connecting to the AI service."}), 500
    except (KeyError, IndexError) as e:
        print(f"Error parsing API response: {e}")
        return jsonify({"error": "Could not understand the AI's response."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
