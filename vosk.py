import sounddevice as sd
from scipy.io.wavfile import write

fs = 16000  # 16kHz sample rate
duration = 5  # seconds
print("Recording...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
write("recorded.wav", fs, recording)
print("Recording saved.")



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
