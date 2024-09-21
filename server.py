import os
import openai
from flask import Flask, jsonify, request, send_from_directory

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Store your key in an environment variable for security

# Route to serve the HTML page directly from the current directory
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Route to handle AJAX requests for text generation
@app.route('/ask', methods=['POST'])
def ask_bot():
    try:
        input_data = request.json
        prompt = input_data.get('question', '')

        if not prompt:
            return jsonify({'error': 'No question provided'}), 400

        # Generate text using OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        generated_text = response['choices'][0]['message']['content'].strip()

        return jsonify({'response': generated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Start Flask app
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
