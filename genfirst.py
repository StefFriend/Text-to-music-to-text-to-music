import argparse
import scipy.io.wavfile
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import warnings

warnings.filterwarnings("ignore")

# Set up argument parsing
parser = argparse.ArgumentParser(description='Generate music based on a textual prompt.')
parser.add_argument('-prompt', type=str, required=True, help='Text prompt for music generation.')


args = parser.parse_args()


# Load model and processor
dataset = "musicgen-small"  # Set API dataset
processor = AutoProcessor.from_pretrained("facebook/" + dataset)
model = MusicgenForConditionalGeneration.from_pretrained("facebook/" + dataset)
#model = model.to('cuda:1')

# Process the input
inputs = processor(text=[args.prompt], padding=True, return_tensors="pt")
#inputs = inputs.to('cuda:1')

# Generate audio
audio_values = model.generate(**inputs, max_new_tokens=128)

# Determine sampling rate from model configuration
sampling_rate = model.config.audio_encoder.sampling_rate

# Create filename using iteration number
filename = f"infinitystem/initial_prompt.wav"  # Ensure 'wav' directory exists

# Save the output to a WAV file in the 'wav' directory
scipy.io.wavfile.write(filename, rate=sampling_rate, data=audio_values[0, 0].numpy())
print(f"Output saved to {filename}")
