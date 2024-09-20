import os
import openai
from flask import Flask, request, jsonify, send_from_directory
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import tempfile
from pydub import AudioSegment
from pydub.utils import which

# Set the path to the ffmpeg executable
ffmpeg_path = "C:\\Users\\Abhishek Patel\\Documents\\Work\\Speech Recognition AI_Online\\OBOT!!!\\ffmpeg-2024-09-19-git-0d5b68c27c-full_build\\bin\\ffmpeg.exe"
AudioSegment.converter = ffmpeg_path
AudioSegment.ffmpeg = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("Osk-EWQURQAdp6lloBfb8uQly3bvqbOPuC3sHKyWPEgtQXT3BlbkFJByap3wtDbVLu2MuhO7ttCakmzGmISlp2TAJDIcMEoA")

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/ask', methods=['POST'])
def ask_openai():
    try:
        # Get the audio file from the request
        audio_file = request.files.get('audio')
        if not audio_file:
            return jsonify({'error': 'No audio file provided.'}), 400

        # Use NamedTemporaryFile with delete=False to avoid permission issues
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            temp_file.write(audio_file.read())
            temp_file_path = temp_file.name

        # Convert WebM to WAV
        wav_file_path = f"{temp_file_path}.wav"
        AudioSegment.from_file(temp_file_path, format="webm").export(wav_file_path, format="wav")

        # Recognize audio using Google Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)
            user_input = recognizer.recognize_google(audio)
            print(f"You asked: {user_input}")  # Print recognized speech

        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )

        # Extract the text from the OpenAI API response
        ai_reply = response['choices'][0]['message']['content']
        print(f"AI response: {ai_reply}")

        # Text to speech response using gTTS
        tts = gTTS(text=ai_reply, lang='en')
        audio_output = BytesIO()
        tts.save(audio_output)
        audio_output.seek(0)

        # Clean up temporary files
        os.remove(temp_file_path)
        os.remove(wav_file_path)

        # Return the AI's response as JSON and send audio back
        return jsonify({'response': ai_reply, 'audio': audio_output.getvalue()}), 200

    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand the audio.'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f"Could not request results from Google Speech Recognition service; {e}"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
