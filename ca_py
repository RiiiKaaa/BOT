# continuous_assistant.py
from faster_whisper import WhisperModel
import pyaudio
import tempfile
import wave
import pyttsx3

# Load the model
model = WhisperModel("base", device="cpu")

# Initialize text-to-speech
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 0.9)

# Your existing get_response function
def get_response(text):
    import string
    clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower().strip()

    if "hi" in clean_text:
        return "Hello! How are you doing?"
    elif "hello" in clean_text:
        return "Hi there! Nice to meet you!"
    elif "how are you" in clean_text:
        return "I'm doing great, thank you for asking!"
    elif "what is your name" in clean_text:
        return "I'm your voice assistant!"
    elif "goodbye" in clean_text or "bye" in clean_text:
        return "Goodbye! Have a wonderful day!"
    elif "thank you" in clean_text or "thanks" in clean_text:
        return "You're very welcome!"
    elif "what time" in clean_text or "time" in clean_text:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%I:%M %p')}"
    elif "what date" in clean_text or "date" in clean_text or "today" in clean_text:
        from datetime import datetime
        return f"Today's date is {datetime.now().strftime('%B %d, %Y')}"
    elif "help" in clean_text:
        return "I'm here to help! You can ask me about time, say hello, or just chat with me."
    else:
        return f"I heard you say: '{text}'. I'm still learning, but I'm here to help!"

# Function to record audio
def record_audio(duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Say something...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        wf = wave.open(tmp_file.name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return tmp_file.name

# 🔁 Continuous loop
def start_assistant():
    print("Assistant is now listening. Say 'stop conversation' to exit.\n")

    while True:
        audio_file = record_audio(duration=5)
        segments, info = model.transcribe(audio_file)

        text = "".join(segment.text for segment in segments).strip()

        if text:
            print("You said:", text)

            if "stop conversation" in text.lower():
                print("Assistant: Goodbye! Conversation ended.")
                tts_engine.say("Goodbye! Conversation ended.")
                tts_engine.runAndWait()
                break

            response = get_response(text)
            print("Assistant:", response)
            tts_engine.say(response)
            tts_engine.runAndWait()
        else:
            print("No speech detected. Listening again...\n")

# Start the assistant when script is run directly
if __name__ == "__main__":
    start_assistant()
