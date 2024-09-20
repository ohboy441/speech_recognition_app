import os
import openai
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO
import threading
import pygame  # Use pygame for audio playback

# Initialize Flask app
openai.api_key = os.getenv("OPENAI_API_KEY")

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        
        self.start_button = tk.Button(root, text="Start Listening", command=self.start_listening)
        self.start_button.pack(pady=20)

        self.status_label = tk.Label(root, text="Status: Idle")
        self.status_label.pack(pady=20)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False  # Flag to manage microphone access

        # Initialize pygame
        pygame.mixer.init()

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.status_label.config(text="Status: Listening...")
            threading.Thread(target=self.listen).start()

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            while self.listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5)  # Listen for audio
                    user_input = self.recognizer.recognize_google(audio)
                    print(f"You asked: {user_input}")
                    self.process_query(user_input)
                except sr.WaitTimeoutError:
                    continue  # Timeout waiting for audio, just keep listening
                except sr.UnknownValueError:
                    continue  # Ignore unrecognized speech
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    break

    def process_query(self, user_input):
        try:
            # OpenAI API call
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_input,
                max_tokens=150
            )

            # Extract the text from the OpenAI API response
            ai_reply = response.choices[0].text.strip()
            print(f"AI response: {ai_reply}")

            # Text to speech response
            tts = gTTS(text=f"You asked {user_input}. Thinking... {ai_reply}", lang='en')
            audio_output = BytesIO()
            tts.save(audio_output)
            audio_output.seek(0)

            # Convert to wav format for playback
            audio_segment = AudioSegment.from_file(audio_output, format="mp3")
            output_io = BytesIO()
            audio_segment.export(output_io, format="wav")
            output_io.seek(0)

            # Play the response using pygame
            pygame.mixer.music.load(output_io)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Wait for playback to finish
                continue

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
