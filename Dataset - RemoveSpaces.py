import pyaudio
import wave
from pydub import AudioSegment, silence
import multiprocessing
import os
from tqdm import tqdm

# Settings for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
INPUT_FOLDER = f'Dataset/Raw'
OUTPUT_EDIT_FILE = f"Dataset/Edit"

def truncateAudio(audioFile, outputFolder):
    # Load the recorded audio file (supports both mp3 and mp4)
    file_extension = audioFile.split('.')[-1].lower()
    
    if file_extension == "mp3":
        audio_segment = AudioSegment.from_mp3(audioFile)
    elif file_extension == "mp4":
        audio_segment = AudioSegment.from_file(audioFile, format="mp4")
    else:
        print(f"Unsupported file format: {file_extension}")
        return

    # Cut out the first 10 seconds and last 10 seconds
    audio_segment = audio_segment[RATE * 10:-RATE * 10]

    # Detect non-silent parts of the audio
    non_silence_ranges = silence.detect_nonsilent(audio_segment, min_silence_len=700, silence_thresh=-60)

    buffer = 100
    
    # Combine non-silent segments, removing long pauses
    edited_audio = AudioSegment.empty()
    for start, end in non_silence_ranges:
        start = max(0, start - buffer)
        end = min(len(audio_segment), end + buffer)
        edited_audio += audio_segment[start:end]

    os.makedirs(outputFolder, exist_ok=True)
    
    file = audioFile.split("/")[-1][:-4]
    outputFile = f'{outputFolder}/{file}.wav'
    
    # Save the edited audio
    edited_audio.export(outputFile)

def process_folder(folder):
    searchFolder = f"{INPUT_FOLDER}/{folder}"
    outputFolder = f"{OUTPUT_EDIT_FILE}/{folder}"

    # List all the audio files in the folder
    files = [file for file in os.listdir(searchFolder) if file.endswith((".mp3", ".mp4"))]
    
    # Process each file in the folder
    for file in tqdm(files, desc=f"Processing files in {folder}", leave=False):
        truncateAudio(f'{searchFolder}/{file}', outputFolder)

if __name__ == '__main__':
    # Get a list of folders (excluding ".DS_Store")
    folders = [folder for folder in os.listdir(INPUT_FOLDER) if folder != ".DS_Store"]

    # Create a pool of workers
    with multiprocessing.Pool() as pool:
        list(tqdm(pool.imap(process_folder, folders), desc="Processing folders", total=len(folders)))
