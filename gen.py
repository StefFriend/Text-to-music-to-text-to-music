# Import necessary libraries
import scipy.io.wavfile
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from IPython.display import Audio

# Function to read prompt text from file
def read_prompt_from_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

# Load model and processor
dataset = "musicgen-medium" # Set API dataset
processor = AutoProcessor.from_pretrained("facebook/" + dataset)
model = MusicgenForConditionalGeneration.from_pretrained("facebook/" + dataset)

# Retrieve the input from the text file
prompt_text = read_prompt_from_file('prompt.txt')

# Process the input
inputs = processor(text=[prompt_text], padding=True, return_tensors="pt")

# Generate audio
audio_values = model.generate(**inputs, max_new_tokens=64)

# Listen to generated music (This part will only work in an IPython environment)
sampling_rate = model.config.audio_encoder.sampling_rate
print("Generated Music:")
Audio(audio_values[0].numpy(), rate=sampling_rate)

# Save output to wav file
formatted_prompt = prompt_text.replace(" ", "_")[:50]
filename = f"{formatted_prompt} - {dataset}.wav"
scipy.io.wavfile.write(filename, rate=sampling_rate, data=audio_values[0, 0].numpy())
print(f"Output saved to {filename}")
