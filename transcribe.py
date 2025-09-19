import sounddevice as sd
import numpy as np
import whisper
from pynput.keyboard import Controller
import tempfile
import soundfile as sf
import os
from playsound3 import playsound

# --- Configuration ---
SAMPLE_RATE = 16000  # Whisper requires 16kHz
CHANNELS = 1
SILENCE_THRESHOLD = 0.01  # Adjust as needed
SILENCE_DURATION = 2  # Seconds of silence to stop recording
MODEL = "medium"
# ---------------------

def is_silent(data):
    """Returns 'True' if the audio data is silent."""
    return np.max(np.abs(data)) < SILENCE_THRESHOLD

def play_sound(file_path="speak.mp3"):
    try:
        playsound(file_path)
    except FileNotFoundError:
        print(f"Warning: Notification sound file not found at {file_path}")
    except Exception as e:
        print(f"Error playing notification sound: {e}")

def record_until_silence():
    """Records from the default microphone until a period of silence is detected."""
    play_sound("speak.mp3")  # Start recording sound
    print("Recording... Speak now.")
    recorded_frames = []
    silent_frames = 0
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS) as stream:
        while True:
            data, overflowed = stream.read(SAMPLE_RATE)  # Read 1 second of audio
            if overflowed:
                print("Warning: Audio buffer overflowed")
            
            recorded_frames.append(data)
            
            if is_silent(data):
                silent_frames += 1
            else:
                silent_frames = 0
            
            if silent_frames >= SILENCE_DURATION:
                print("Silence detected. Stopping recording.")
                break
    
    play_sound("transcribing.mp3")  # Stop recording sound
    return np.concatenate(recorded_frames, axis=0)

def transcribe_audio(audio_data):
    """Transcribes audio data using Whisper."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        sf.write(tmp_file.name, audio_data, SAMPLE_RATE)
        tmp_file_name = tmp_file.name

    try:
        print("Transcribing...")
        model = whisper.load_model(MODEL)  # Or choose another model size
        result = model.transcribe(tmp_file_name)
        return result["text"]
    finally:
        os.remove(tmp_file_name)

def type_text(text, keyboard):
    """Types out the given text using pynput."""
    print(f"Typing: {text}")
    for char in text:
        keyboard.type(char)

if __name__ == "__main__":
    keyboard = Controller()
    try:
        audio = record_until_silence()
        transcribed_text = transcribe_audio(audio)
        if transcribed_text:
            type_text(transcribed_text, keyboard)
    finally:
        print("Done.")
