import demucs.api
import sys
import os

# Set default destination folder
default_destination_folder = 'infinitystem/stem'

if len(sys.argv) < 2:
    print("Usage: python demu.py <audio_file_path> [destination_folder]")
    sys.exit(1)

audio_file_path = sys.argv[1]  # Get the audio file path from command line arguments

# Check if a destination folder was provided, otherwise use default
if len(sys.argv) >= 3:
    destination_folder = sys.argv[2]
else:
    destination_folder = default_destination_folder

# Initialize with default parameters:
separator = demucs.api.Separator()

# Use another model and segment:
separator = demucs.api.Separator(model="mdx_extra", segment=12)

# Separating an audio file
origin, separated = separator.separate_audio_file(audio_file_path)

for stem, source in separated.items():
    # Ensure the destination directory exists or create it
    os.makedirs(destination_folder, exist_ok=True)
    
    # Save as WAV with encoding specified
    dest_path = os.path.join(destination_folder, f"{stem}.wav")
    demucs.api.save_audio(source, dest_path, samplerate=separator.samplerate, bits_per_sample=16)
