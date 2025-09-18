# whisper\STT-TTS.py

from google import genai
from google.genai import types
import wave
import whisper
import sounddevice as sd
import numpy as np
import keyboard
from dotenv import load_dotenv
import os
import google
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Function to save wave file
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


# Initialize Whisper (STT)
print("⏳ Loading Whisper model...")
stt_model = whisper.load_model("base")

# Recording settings
samplerate = 16000
channels = 1

print("🎤 Speak now... Press 'q' to stop recording.")

recording = []

# Record until 'q' is pressed
with sd.InputStream(samplerate=samplerate, channels=channels, dtype='float32') as stream:
    while True:
        data, _ = stream.read(1024)
        recording.append(data.copy())

        if keyboard.is_pressed("q"):
            print("\n🛑 Stopped recording.")
            break

# Convert to numpy array
audio = np.concatenate(recording, axis=0)

# Flatten for Whisper
audio = audio.flatten()

# Transcribe speech
print("⏳ Transcribing...")
result = stt_model.transcribe(audio, fp16=False)
transcript = result["text"]

print("\n📝 Final Transcript:")
print(transcript)


# ---------- GEMINI TTS ----------
print("🗣️ Generating speech with Gemini...")


api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents=transcript,   # 👈 Feed Whisper transcript into Gemini
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Kore",   # Change voice if needed
                )
            )
        ),
    ),
)

# Extract audio data
data = response.candidates[0].content.parts[0].inline_data.data

# Save audio
file_name = "out.wav"
wave_file(file_name, data)
print(f"✅ Saved TTS audio to {file_name}")



# whisper\STT-TTS.py

# from google import genai
# from google.genai import types
# import wave
# import whisper
# import sounddevice as sd
# import numpy as np
# import keyboard
# from dotenv import load_dotenv
# import os
# from langchain_groq import ChatGroq

# # Load environment variables from .env file
# load_dotenv()

# # Function to save wave file
# def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
#     with wave.open(filename, "wb") as wf:
#         wf.setnchannels(channels)
#         wf.setsampwidth(sample_width)
#         wf.setframerate(rate)
#         wf.writeframes(pcm)


# # Initialize Whisper (STT)
# print("⏳ Loading Whisper model...")
# stt_model = whisper.load_model("base")

# # Recording settings
# samplerate = 16000
# channels = 1

# print("🎤 Speak now... Press 'q' to stop recording.")

# recording = []

# # Record until 'q' is pressed
# with sd.InputStream(samplerate=samplerate, channels=channels, dtype='float32') as stream:
#     while True:
#         data, _ = stream.read(1024)
#         recording.append(data.copy())

#         if keyboard.is_pressed("q"):
#             print("\n🛑 Stopped recording.")
#             break

# # Convert to numpy array
# audio = np.concatenate(recording, axis=0)

# # Flatten for Whisper
# audio = audio.flatten()

# # Transcribe speech
# print("⏳ Transcribing...")
# result = stt_model.transcribe(audio, fp16=False)
# transcript = result["text"]

# print("\n📝 Final Transcript:")
# print(transcript)


# # ---------- SEND TO LLM ----------
# print("🤖 Sending transcript to LLM...")

# llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

# response = llm.invoke(f"User said: {transcript}. Give a helpful response.")
# llm_output = response.content if hasattr(response, "content") else str(response)

# print("\n💬 LLM Response:")
# print(llm_output)


# # ---------- GEMINI TTS ----------
# print("🗣️ Generating speech with Gemini...")

# api_key = os.getenv("GOOGLE_API_KEY")
# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-2.5-flash-preview-tts",
#     contents=llm_output,   # 👈 Use LLM output instead of raw transcript
#     config=types.GenerateContentConfig(
#         response_modalities=["AUDIO"],
#         speech_config=types.SpeechConfig(
#             voice_config=types.VoiceConfig(
#                 prebuilt_voice_config=types.PrebuiltVoiceConfig(
#                     voice_name="Kore",   # Change voice if needed
#                 )
#             )
#         ),
#     ),
# )

# # Extract audio data
# data = response.candidates[0].content.parts[0].inline_data.data

# # Save audio
# file_name = "out.wav"
# wave_file(file_name, data)
# print(f"✅ Saved TTS audio to {file_name}")
