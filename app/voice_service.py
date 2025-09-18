# # app/voice_service.py

# import whisper
# import sounddevice as sd
# import numpy as np
# import tempfile
# import os
# import wave
# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
# import io

# load_dotenv()

# class VoiceService:
#     def __init__(self):
#         print("⏳ Loading Whisper model...")
#         self.stt_model = whisper.load_model("base")
#         self.api_key = os.getenv("GOOGLE_API_KEY")
#         if not self.api_key:
#             raise ValueError("GOOGLE_API_KEY not found in environment variables")
#         self.client = genai.Client()
    
#     def transcribe_audio(self, audio_data: bytes) -> str:
#         """
#         Transcribe audio bytes to text using Whisper
#         """
#         try:
#             # Save audio to temporary file
#             with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
#                 temp_file.write(audio_data)
#                 temp_file_path = temp_file.name
            
#             # Transcribe with Whisper
#             result = self.stt_model.transcribe(temp_file_path, fp16=False)
#             transcript = result["text"]
            
#             # Clean up temp file
#             os.unlink(temp_file_path)
            
#             return transcript
            
#         except Exception as e:
#             print(f"Error in transcription: {e}")
#             raise
    
#     def text_to_speech(self, text: str, voice_name: str = "Kore") -> bytes:
#         """
#         Convert text to speech using Gemini TTS
#         """
#         try:
#             response = self.client.models.generate_content(
#                 model="gemini-2.5-flash-preview-tts",
#                 contents=text,
#                 config=types.GenerateContentConfig(
#                     response_modalities=["AUDIO"],
#                     speech_config=types.SpeechConfig(
#                         voice_config=types.VoiceConfig(
#                             prebuilt_voice_config=types.PrebuiltVoiceConfig(
#                                 voice_name=voice_name
#                             )
#                         )
#                     ),
#                 ),
#             )
            
#             # Extract audio data
#             audio_data = response.candidates[0].content.parts[0].inline_data.data
#             return audio_data
            
#         except Exception as e:
#             print(f"Error in TTS: {e}")
#             raise

# # Global instance
# voice_service = VoiceService()



# # app\voice_service.py
# from google import genai
# from google.genai import types
# import wave
# import whisper
# import sounddevice as sd
# import numpy as np
# import keyboard
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# # ---------- Helper ----------
# def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
#     with wave.open(filename, "wb") as wf:
#         wf.setnchannels(channels)
#         wf.setsampwidth(sample_width)
#         wf.setframerate(rate)
#         wf.writeframes(pcm)


# # ---------- STT (Whisper) ----------
# def speech_to_text() -> str:
#     """Record from mic until 'q' pressed, return transcript"""
#     print("⏳ Loading Whisper model...")
#     stt_model = whisper.load_model("base")

#     samplerate = 16000
#     channels = 1
#     recording = []

#     print("🎤 Speak now... Press 'q' to stop recording.")

#     with sd.InputStream(samplerate=samplerate, channels=channels, dtype='float32') as stream:
#         while True:
#             data, _ = stream.read(1024)
#             recording.append(data.copy())

#             if keyboard.is_pressed("q"):
#                 print("\n🛑 Stopped recording.")
#                 break

#     audio = np.concatenate(recording, axis=0).flatten()

#     print("⏳ Transcribing...")
#     result = stt_model.transcribe(audio, fp16=False)
#     transcript = result["text"]

#     print("\n📝 Final Transcript:")
#     print(transcript)

#     return transcript


# # ---------- TTS (Gemini) ----------
# def text_to_speech(text: str, filename: str = "out.wav") -> str:
#     """Convert text into speech using Gemini TTS and save to .wav"""
#     print("🗣️ Generating speech with Gemini...")

#     api_key = os.getenv("GOOGLE_API_KEY")
#     client = genai.Client()

#     response = client.models.generate_content(
#         model="gemini-2.5-flash-preview-tts",
#         contents=text,
#         config=types.GenerateContentConfig(
#             response_modalities=["AUDIO"],
#             speech_config=types.SpeechConfig(
#                 voice_config=types.VoiceConfig(
#                     prebuilt_voice_config=types.PrebuiltVoiceConfig(
#                         voice_name="Kore",
#                     )
#                 )
#             ),
#         ),
#     )

#     data = response.candidates[0].content.parts[0].inline_data.data
#     wave_file(filename, data)

#     print(f"✅ Saved TTS audio to {filename}")
#     return filename




from google import genai
from google.genai import types
import wave
import whisper
import sounddevice as sd
import numpy as np
import keyboard
from dotenv import load_dotenv
import os
import tempfile
import uuid

# Load environment variables from .env file
load_dotenv()

# Global Whisper model instance for reuse
_whisper_model = None

def get_whisper_model():
    """Get or load Whisper model (singleton pattern for efficiency)"""
    global _whisper_model
    if _whisper_model is None:
        print("⏳ Loading Whisper model...")
        _whisper_model = whisper.load_model("base")
    return _whisper_model

# ---------- Helper ----------
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Create a wave file from PCM data"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


# ---------- STT Functions ----------
def speech_to_text() -> str:
    """Record from mic until 'q' pressed, return transcript (for CLI usage)"""
    stt_model = get_whisper_model()

    samplerate = 16000
    channels = 1
    recording = []

    print("🎤 Speak now... Press 'q' to stop recording.")

    with sd.InputStream(samplerate=samplerate, channels=channels, dtype='float32') as stream:
        while True:
            data, _ = stream.read(1024)
            recording.append(data.copy())

            if keyboard.is_pressed("q"):
                print("\n🛑 Stopped recording.")
                break

    audio = np.concatenate(recording, axis=0).flatten()

    print("⏳ Transcribing...")
    result = stt_model.transcribe(audio, fp16=False)
    transcript = result["text"]

    print("\n📝 Final Transcript:")
    print(transcript)

    return transcript


def transcribe_audio_file(audio_file_path: str) -> str:
    """Transcribe audio from a file path"""
    stt_model = get_whisper_model()
    
    print("⏳ Transcribing audio file...")
    result = stt_model.transcribe(audio_file_path, fp16=False)
    transcript = result["text"]
    
    print(f"📝 Transcript: {transcript}")
    return transcript


def transcribe_audio_data(audio_data: bytes, file_extension: str = ".wav") -> str:
    """Transcribe audio from raw bytes data"""
    stt_model = get_whisper_model()
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(audio_data)
        tmp_file.flush()
        
        # Transcribe
        result = stt_model.transcribe(tmp_file.name, fp16=False)
        transcript = result["text"]
        
        # Clean up
        os.unlink(tmp_file.name)
    
    return transcript


# ---------- TTS Functions ----------
def text_to_speech(text: str, filename: str = None) -> str:
    """Convert text into speech using Gemini TTS and save to .wav"""
    if filename is None:
        filename = f"tts_output_{uuid.uuid4()}.wav"
    
    print("🗣️ Generating speech with Gemini...")

    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",  # Updated model name
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Kore",
                        )
                    )
                ),
            ),
        )

        data = response.candidates[0].content.parts[0].inline_data.data
        wave_file(filename, data)

        print(f"✅ Saved TTS audio to {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        raise


def text_to_speech_stream(text: str) -> bytes:
    """Convert text to speech and return audio data as bytes"""
    print("🗣️ Generating speech with Gemini (streaming)...")

    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Kore",
                        )
                    )
                ),
            ),
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data
        print("✅ Generated TTS audio data")
        return audio_data
        
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        raise


# ---------- Combined Voice Functions ----------
def voice_to_voice_response(user_speech_file: str, process_function, **kwargs) -> tuple[str, str]:
    """
    Complete voice-to-voice pipeline:
    1. Transcribe user speech
    2. Process with given function
    3. Generate TTS response
    
    Returns: (transcript, audio_filename)
    """
    # Step 1: STT
    transcript = transcribe_audio_file(user_speech_file)
    
    # Step 2: Process with provided function
    text_response = process_function(user_input=transcript, **kwargs)
    
    # Step 3: TTS
    audio_filename = f"voice_response_{uuid.uuid4()}.wav"
    text_to_speech(text_response, audio_filename)
    
    return transcript, audio_filename, text_response


# ---------- Utility Functions ----------
def cleanup_audio_files(max_age_hours: int = 24):
    """Clean up old audio files to prevent storage bloat"""
    import time
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    # Clean up TTS output files
    for filename in os.listdir('.'):
        if filename.startswith(('tts_output_', 'voice_response_', 'hr_response_', 'tech_response_', 'project_response_')) and filename.endswith('.wav'):
            file_age = current_time - os.path.getctime(filename)
            if file_age > max_age_seconds:
                try:
                    os.remove(filename)
                    print(f"🗑️ Cleaned up old audio file: {filename}")
                except OSError:
                    pass


if __name__ == "__main__":
    # Test the functions
    print("Testing voice service...")
    
    # Test TTS
    test_text = "Hello, this is a test of the text-to-speech functionality."
    audio_file = text_to_speech(test_text, "test_output.wav")
    print(f"Created test audio: {audio_file}")
    
    # Test STT (if you have a test audio file)
    # transcript = transcribe_audio_file("test_output.wav")
    # print(f"Transcription: {transcript}")