import sounddevice as sd
import numpy as np
import wave
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import os
import queue
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from tensorflow.keras.models import load_model
import io
import cv2
import warnings

# Get available devices
# print("Available recording devices:")
# print(sd.query_devices())

# # Ask the user to select a device
# device_id = int(input("Select a device ID for recording: "))
device_id = 5


# Load the saved Keras model
model = load_model('best_model_CNN_1.5_Overlap.keras')

classes = ['3Blue1Brown', 'A Better You Podcast', 'Just Alex Podcast', 'Solo Flight Podcast']

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Parameters
SPECTROGRAM_FOLDER = "Dataset/Spectrogram"
SAMPLE_RATE = 44100
CHUNK_DURATION = 2

def RUN(audio_data, chunk_number, output_dir):
    # Example function to process audio data
    # Saving the audio to a WAV file
    with wave.open('last_two_seconds.wav', 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)  # 2 bytes for int16
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())
    
    process_wav_file('last_two_seconds.wav')
    # Save the spectrogram
    # audio_img = save_spectrogram(audio_data, SAMPLE_RATE, chunk_number, output_dir)
    # print(predict_speaker(audio_img), end="\r")
    
    # Save the audio chunk as MP3
    # save_audio_chunk(audio_data, chunk_number, output_dir)
    

def process_wav_file(file_path, chunk_duration=CHUNK_DURATION, overlap_duration=1.5):
    try:
        y, sr = librosa.load(file_path, sr=None)
    except Exception as e:
        print(f"Couldn't Load: {file_path} - {e}")
        return

    # Skip very short files
    if len(y) < sr * chunk_duration:
        print(f"Skipping short file: {file_path} (length: {len(y)/sr:.2f} seconds)")
        return    

    img = save_spectrogram(y, sr)
    
    print(predict_speaker(img))

def save_spectrogram(y, sr):
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.set_axis_off()
    img = librosa.display.specshow(D, sr=sr, cmap='gray', ax=ax)
    ax.set_aspect('equal')    
    
    # Save the figure to a BytesIO object
    byte_io = io.BytesIO()
    plt.savefig(byte_io, bbox_inches='tight', pad_inches=0, transparent=True)
    
    output_path = f'{SPECTROGRAM_FOLDER}/chunk_.png'
    fig.savefig(output_path, bbox_inches='tight', pad_inches=0, transparent=True)
    
    plt.close(fig)
    
    # Seek to the start of the BytesIO object
    byte_io.seek(0)

    # Convert the BytesIO to a NumPy array (image)
    img_array = np.frombuffer(byte_io.getvalue(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

    return img  # Return the spectrogram for further processing or prediction

def predict_speaker(spectrogram):
    """Predicts the speaker from the spectrogram."""
    spectrogram = np.expand_dims(spectrogram, axis=0)  # Adding batch dimension
    prediction = model.predict(spectrogram, verbose=False)
    
    index = np.argmax(prediction[0])
    
    if np.isnan(prediction[0][0]):
        return "Unknown"
    
    return f'{classes[index]}: {prediction[0][index]*100:.2f}%'


chunk_number = 1
try:
    while True:
        
        # Record audio for 2 seconds
        recording = sd.rec(int(CHUNK_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=2, dtype='int16', device=device_id)
        sd.wait()  # Wait until recording is finished
        
        # Call the RUN function with the recorded audio
        RUN(recording, chunk_number, SPECTROGRAM_FOLDER)
        chunk_number += 1

except KeyboardInterrupt:
    # print("Recording stopped.")
    pass
except Exception as e:
    print(f"An error occurred: {e}")
    
