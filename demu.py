import demucs.api
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python demu.py <audio_file_path>")
    sys.exit(1)

audio_file_path = sys.argv[1]  # Get the audio file path from command line arguments

# Initialize with default parameters:
separator = demucs.api.Separator()

# Use another model and segment:
separator = demucs.api.Separator(model="mdx_extra", segment=12)

# Separating an audio file
origin, separated = separator.separate_audio_file(audio_file_path)

for stem, source in separated.items():
    # Ensure the 'stems' directory exists or create it
    os.makedirs('../stems', exist_ok=True)
    
    # Save as WAV with encoding specified
    demucs.api.save_audio(source, f"../stems/{stem}.wav", samplerate=separator.samplerate, bits_per_sample=16)
 