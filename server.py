import os
import json
import openai
from flask import Flask, request, jsonify
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO

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
        # Get the audio file from the request
        audio_file = request.files.get('audio')
        if not audio_file:
            return jsonify({'error': 'No audio file provided.'}), 400
        
        # Convert audio file to text
        recognizer = sr.Recognizer()
        audio_data = sr.AudioFile(audio_file)
        
        with audio_data as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.record(source)
            user_input = recognizer.recognize_google(audio)
            print(f"You asked: {user_input}")

        # OpenAI API call
        response = openai.Completion.create(
            engine="text-davinci-003",  # Model to use
            prompt=user_input,          # Query from the user
            max_tokens=150              # Limit on response length
        )

        # Extract the text from the OpenAI API response
        ai_reply = response.choices[0].text.strip()
        print(f"AI response: {ai_reply}")

        # Text to speech response
        tts = gTTS(text=f"You asked {user_input}. Thinking... {ai_reply}", lang='en')
        audio_output = BytesIO()
        tts.save(audio_output)
        audio_output.seek(0)

        # Convert to wav format for sending back
        audio_segment = AudioSegment.from_file(audio_output, format="mp3")
        output_io = BytesIO()
        audio_segment.export(output_io, format="wav")
        output_io.seek(0)

        # Return the AI's response as JSON and audio file
        return jsonify({'response': ai_reply}), 200, {
            'Content-Type': 'audio/wav',
            'Content-Disposition': 'attachment; filename="response.wav"'
        }, output_io.getvalue()

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get the port from Render environment variable, default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the app on all available IP addresses ('0.0.0.0') and the selected port
    app.run(host='0.0.0.0', port=port)
