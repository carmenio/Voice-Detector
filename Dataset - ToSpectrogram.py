import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import os
import shutil
from multiprocessing import Pool
from tqdm import tqdm
import warnings
from datetime import datetime

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Set the duration for each spectrogram chunk (in seconds)
CHUNK_DURATION = 2  # Change this value to adjust chunk duration

def save_spectrogram(y, sr, file_name, chunk_number, output_dir):
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.set_axis_off()
    img = librosa.display.specshow(D, sr=sr, cmap='gray', ax=ax)
    ax.set_aspect('equal')
    output_path = os.path.join(output_dir, f'{file_name}_spectrogram_chunk_{chunk_number}.png')
    fig.savefig(output_path, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)

def process_wav_file(file_path, output_dir, chunk_duration=CHUNK_DURATION, overlap_duration=1.5):
    try:
        y, sr = librosa.load(file_path, sr=None)
    except Exception as e:
        print(f"Couldn't Load: {file_path} - {e}")
        return

    # Skip very short files
    if len(y) < sr * chunk_duration:
        print(f"Skipping short file: {file_path} (length: {len(y)/sr:.2f} seconds)")
        return

    os.makedirs(output_dir, exist_ok=True)
    samples_per_chunk = sr * chunk_duration
    overlap_samples = int(sr * overlap_duration)

    # Get the base name for the output files
    base_file_name = os.path.splitext(os.path.basename(file_path))[0]
    chunk_number = 1
    for start in range(0, len(y) - samples_per_chunk + 1, samples_per_chunk - overlap_samples):
        end = start + samples_per_chunk
        chunk = y[start:end]

        if len(chunk) < samples_per_chunk:
            break

        save_spectrogram(chunk, sr, base_file_name, chunk_number, output_dir)
        chunk_number += 1

def remove_folder(folder_path):
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' has been removed successfully.")
        except Exception as e:
            print(f"Error occurred while removing the folder: {e}")
    else:
        print(f"Folder '{folder_path}' does not exist.")

def process_file(file_info):
    file_path, output_dir = file_info
    process_wav_file(file_path, output_dir)

if __name__ == "__main__":
    OUTPUT_EDIT_FILE = "Dataset/Edit"
    SPECTROGRAM_FOLDER = "Dataset/Spectrogram2"

    remove_folder(SPECTROGRAM_FOLDER)

    file_info_list = []
    
    for folder in os.listdir(OUTPUT_EDIT_FILE):
        if folder != ".DS_Store":
            search_folder = os.path.join(OUTPUT_EDIT_FILE, folder)
            output_folder = os.path.join(SPECTROGRAM_FOLDER, folder)
            
            for file in os.listdir(search_folder):
                if file.endswith(".wav"):
                    file_info_list.append((os.path.join(search_folder, file), output_folder))

    with Pool() as pool:
        list(tqdm(pool.imap(process_file, file_info_list), total=len(file_info_list)))
