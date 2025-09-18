# whisper\STT.py

import whisper
import sounddevice as sd
import numpy as np
import keyboard  # pip install keyboard

# Load Whisper model (tiny, base, small, medium, large)
model = whisper.load_model("base")

# Recording settings
samplerate = 16000
channels = 1

print("🎤 Listening... Press 'q' to stop recording.")

recording = []

# Record until 'q' is pressed
with sd.InputStream(samplerate=samplerate, channels=channels, dtype='float32') as stream:
    while True:
        data, _ = stream.read(1024)
        recording.append(data.copy())

        if keyboard.is_pressed('q'):
            print("\n🛑 Stopped recording.")
            break

# Convert to numpy array
audio = np.concatenate(recording, axis=0)

# Whisper expects 1D float32 array
audio = audio.flatten()

# Transcribe once at the end
print("⏳ Transcribing...")
result = model.transcribe(audio, fp16=False)

print("\n📝 Final Transcript:")
print(result["text"])


# whisper/STT.py
# import whisper
# import sounddevice as sd
# import numpy as np
# import keyboard

# def record_and_transcribe(model_name="base"):
#     """
#     Records audio from microphone until 'q' is pressed,
#     then transcribes using Whisper.
#     """
#     model = whisper.load_model(model_name)
#     samplerate = 16000
#     channels = 1

#     print("🎤 Listening... Press 'q' to stop recording.")

#     recording = []
#     with sd.InputStream(samplerate=samplerate, channels=channels, dtype='float32') as stream:
#         while True:
#             data, _ = stream.read(1024)
#             recording.append(data.copy())

#             if keyboard.is_pressed('q'):
#                 print("\n🛑 Stopped recording.")
#                 break

#     # Convert to numpy array
#     audio = np.concatenate(recording, axis=0).flatten()

#     # Transcribe
#     print("⏳ Transcribing...")
#     result = model.transcribe(audio, fp16=False)

#     return result["text"]
