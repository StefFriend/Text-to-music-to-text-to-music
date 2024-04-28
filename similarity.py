import os
import librosa
import soundfile as sf

from audio_similarity import AudioSimilarity

def resample_audio_files(directory, target_sr):
    processed_files = []  # List to store names of processed files
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            audio, sr = librosa.load(file_path, sr=None)  # native sampling rate of the file
            if sr != target_sr:
                print(f"Resampling {filename} from {sr} Hz to {target_sr} Hz.")
                audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
                sf.write(file_path, audio_resampled, target_sr)
            processed_files.append(filename)  # Append filename to list
    return processed_files


# Paths to the original and comparison audio files/folders
original_path = 'audio/'
compare_path = 'audio2/'

# Count files in each directory
original_count = len([name for name in os.listdir(original_path) if os.path.isfile(os.path.join(original_path, name))])
compare_count = len([name for name in os.listdir(compare_path) if os.path.isfile(os.path.join(compare_path, name))])

print(f"Original files count: {original_count}")
print(f"Comparison files count: {compare_count}")


# Set the target sample rate
target_sample_rate = 44100

# Resample audio files and capture file names
original_files = resample_audio_files(original_path, target_sample_rate)
compare_files = resample_audio_files(compare_path, target_sample_rate)

# Output file names
print(f"Processed original files: {original_files}")
print(f"Processed comparison files: {compare_files}")


weights = {
    'zcr_similarity': 0.2,
    'rhythm_similarity': 0.2,
    'chroma_similarity': 0.2,
    'energy_envelope_similarity': 0.1,
    'spectral_contrast_similarity': 0.1,
    'perceptual_similarity': 0.2
}

# Use the minimum of the counts or a default sample size
sample_size = min(original_count, compare_count, 20)  # As previously set to 20

verbose = True # Show logs

# Create an instance of the AudioSimilarity class

audio_similarity = AudioSimilarity(original_path, compare_path, target_sample_rate, weights, verbose=verbose, sample_size=sample_size)

# Calculate a single metric

#zcr_similarity = audio_similarity.zcr_similarity()

# Calculate the Stent Weighted Audio Similarity

similarity_score = audio_similarity.stent_weighted_audio_similarity(metrics='all') # You can select all metrics or just the 'swass' metric

print(f"Stent Weighted Audio Similarity: {similarity_score}")

audio_similarity.plot(metrics=None,
                      option='all',
                      figsize=(14, 7),
                      color1='red',
                      color2='green',
                      dpi=100,
                      savefig=False,
                      fontsize=6,
                      label_fontsize=8,
                      title_fontsize=12, 
                      alpha=0.5, 
                      title=f'Audio Similarity Metrics {original_files} and {compare_files}')