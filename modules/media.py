import requests
from io import BytesIO
from pydub import AudioSegment
import os

# AI Image generation using HuggingFace API
HF_API_KEY = os.getenv("HF_API_KEY")  # Free HuggingFace API key
HF_IMAGE_URL = "https://api-inference.huggingface.co/models/gsdf/Counterfeit-V2.5"

def generate_image(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}
    response = requests.post(HF_IMAGE_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return BytesIO(response.content)
    return None

# TTS: using gTTS (Google Text-to-Speech)
from gtts import gTTS

def text_to_speech(text):
    tts = gTTS(text)
    file_path = "speech.mp3"
    tts.save(file_path)
    return file_path

# STT: converting voice to text using SpeechRecognition
import speech_recognition as sr

def speech_to_text(file_path):
    r = sr.Recognizer()
    audio = sr.AudioFile(file_path)
    with audio as source:
        audio_data = r.record(source)
    try:
        text = r.recognize_google(audio_data)
        return text
    except:
        return "⚠️ Could not recognize speech."
