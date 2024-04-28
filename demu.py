import demucs.api

# Initialize with default parameters:
separator = demucs.api.Separator()

# Use another model and segment:
separator = demucs.api.Separator(model="mdx_extra", segment=12)

# Separating an audio file
origin, separated = separator.separate_audio_file("modern pop ballad.wav")

# Separating a loaded audio
#origin, separated = separator.separate_tensor(origin)

# If you encounter an error like CUDA out of memory, you can use this to change parameters like `segment`:
#separator.update_parameter(segment=smaller_segment)

print(separated)
type(separated)

for stem, source in separated.items():
    # Save as WAV with encoding specified
    demucs.api.save_audio(source, f"{stem}_prova.wav", samplerate=separator.samplerate, bits_per_sample=16)
 