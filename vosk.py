from gtts import gTTS
from pydub import AudioSegment

# Step 1: Generate mp3 from text
text = "Hello, this is a sample audio to test Vosk speech recognition."
tts = gTTS(text)
tts.save("temp.mp3")

# Step 2: Convert mp3 to wav (mono, 16kHz)
sound = AudioSegment.from_mp3("temp.mp3")
sound = sound.set_channels(1)       # mono
sound = sound.set_frame_rate(16000) # 16kHz
sound.export("output.wav", format="wav")

print("Audio saved as output.wav")

ffmpeg -i input_audio.mp3 -ar 16000 -ac 1 -acodec pcm_s16le output.wav



from vosk import Model, KaldiRecognizer
import wave

# Load the model
model = Model("vosk-model-small-en-us-0.15")
wf = wave.open("recorded.wav", "rb")

# Check format
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
    print("Audio file must be WAV format PCM mono, 16-bit, 16000 Hz")
    exit()

rec = KaldiRecognizer(model, wf.getframerate())

# Process the audio
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())

# Final result
print(rec.FinalResult())



pip install vosk sounddevice scipy
