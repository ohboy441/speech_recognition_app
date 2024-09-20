import os
from flask import Flask, request, jsonify
import openai

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Speech Recognition AI is Running!"

@app.route('/ask', methods=['POST'])
def ask_openai():
    try:
        # Get the query from the request data
        data = request.json
        user_input = data.get('query', '')

        if not user_input:
            return jsonify({'error': 'No query provided.'}), 400

        # OpenAI API call
        response = openai.Completion.create(
            engine="text-davinci-003",  # Model to use
            prompt=user_input,          # Query from the user
            max_tokens=150              # Limit on response length
        )

        # Extract the text from the OpenAI API response
        ai_reply = response.choices[0].text.strip()

        # Return the AI's response as JSON
        return jsonify({'response': ai_reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get the port from Render environment variable, default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the app on all available IP addresses ('0.0.0.0') and the selected port
    app.run(host='0.0.0.0', port=port)
