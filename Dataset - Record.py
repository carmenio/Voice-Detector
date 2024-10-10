import pyaudio
import wave
from pydub import AudioSegment, silence
import threading
import time
import os


name = "Chris"

# Settings for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILE = f"Dataset/Raw/{name}"
OUTPUT_EDIT_FILE = f"Dataset/Edit/{name}"

os.makedirs(OUTPUT_FILE, exist_ok=True)
os.makedirs(OUTPUT_EDIT_FILE, exist_ok=True)

# Get a list of all files in the directory
files = [f for f in os.listdir(OUTPUT_FILE) if os.path.isfile(os.path.join(OUTPUT_FILE, f))]

# Get the number of files
num_files = len(files)

# Flag to control the recording loop
recording = True

# Function to handle stopping the recording
def stop_recording():
    global recording
    input("Press 'Enter' to stop recording...\n")
    recording = False

# Start the stop_recording function in a separate thread
stop_thread = threading.Thread(target=stop_recording)
stop_thread.start()

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording... Press 'Enter' to stop.")
frames = []

# Start recording
start_time = time.time()  # To track recording time

try:
    while recording:
        try:
            # Read audio data from the stream
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

            # Display elapsed time in seconds
            elapsed_time = int(time.time() - start_time)
            print(f"Recording Time: {elapsed_time} seconds", end='\r')

        except IOError as e:
            print(f"Error reading audio stream: {e}")
            continue

except KeyboardInterrupt:
    print("\nRecording stopped by keyboard interrupt.")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded audio as a WAV file
with wave.open(f'{OUTPUT_FILE}/output_{num_files:04d}.wav', 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

# Load the recorded audio file
audio_segment = AudioSegment.from_wav(f'{OUTPUT_FILE}/output_{num_files:04d}.wav')

# Detect non-silent parts of the audio
non_silence_ranges = silence.detect_nonsilent(audio_segment, min_silence_len=500, silence_thresh=-40)

# Combine non-silent segments, removing long pauses
edited_audio = AudioSegment.empty()
for start, end in non_silence_ranges:
    edited_audio += audio_segment[start:end]

# Save the edited audio
edited_audio.export(f'{OUTPUT_EDIT_FILE}/output_{num_files:04d}.wav', format="wav")

print(f"Edited audio saved as {OUTPUT_EDIT_FILE}")

