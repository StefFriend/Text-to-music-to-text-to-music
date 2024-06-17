import os
import shutil
import subprocess
import csv
import argparse
#from sklearn.preprocessing import LabelEncoder


# Argument parsing setup
parser = argparse.ArgumentParser(description='Run music generation and captioning.')
parser.add_argument('--prompt', type=str, required=True, help='Initial prompt for music generation')
parser.add_argument('--genre', type=str, required=True, help='Target genre')
args = parser.parse_args()

# Using the passed argument
current_prompt = args.prompt
target_genre = args.genre

# Paths setup - CHANGE BASED ON YOUR DIR PATH
base_dir = os.path.dirname(os.path.abspath(__file__))
prompt_directory = r'ABSOLUTE_PATH_TO\infinitystem'
wav_directory = os.path.join(base_dir, 'infinitystem/iterations')
stem_directory = r'ABSOLUTE_PATH_TO\infinitystem\stem'
captioning_directory = r'ABSOLUTE_PATH_TO\music_captioning'
genre_check_directory = r'ABSOLUTE_PATH_TO\gr'
demucs_directory = r'ABSOLUTE_PATH_TO\demucs'

# Envs setup - CHANGE BASED ON YOUR DIR PATH and ENV name
MUSICGEN_ENV_PATH = r'PATH_TO_YOUR_ENV\ENV_NAME\python.exe'
MUSICGEN_SCRIPT_PATH = os.path.join(base_dir, 'musicgen', 'genstem.py')
MUSICGEN2_SCRIPT_PATH = os.path.join(base_dir, 'musicgen', 'genfirst.py')
CAPTIONING_ENV_PATH = r'PATH_TO_YOUR_ENV\ENV_NAME\python.exe'
CAPTIONING_SCRIPT_PATH = os.path.join(captioning_directory, 'captioning2.py')
GENRECHECK_ENV_PATH = r'PATH_TO_YOUR_ENV\ENV_NAME\python.exe'
GENRECHECK_SCRIPT_PATH = os.path.join(genre_check_directory, 'genrecheck2.py')
DEMUCS_ENV_PATH = r'PATH_TO_YOUR_ENV\ENV_NAME\python.exe'
DEMUCS_SCRIPT_PATH = os.path.join(demucs_directory, 'demu.py')

# Initialize the CSV file with headers
csv_filename = os.path.join(prompt_directory, 'prompts.csv')
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Iteration', 'Prompt', f'{target_genre} Confidence', 'Predicted Genre', 'Predicted Genre Confidence'])
    # Log the initial prompt with iteration 0
    writer.writerow(['initial_prompt', current_prompt])

# Function to run music generation
def run_music_generation(env_path, script_path, iteration, prompt, instrument):
    wav_filename = os.path.join(wav_directory, f'{instrument}_{iteration}.wav')
    command = [env_path, script_path, '-prompt', prompt, '-iteration', str(iteration), '-instrument', str(instrument)]
    subprocess.run(command, check=True)
    return wav_filename

# Function to run music generation
def run_first_music_generation(env_path, script_path, prompt):
    wav_filename = os.path.join(prompt_directory, f'initial_prompt.wav')
    command = [env_path, script_path, '-prompt', prompt]
    subprocess.run(command, check=True)
    return wav_filename

# Function to run captioning
def run_captioning(env_path, script_path, audio_path, iteration, instrument):
    # Copy WAV file to the captioning directory
    target_path = os.path.join(captioning_directory, f'{instrument}_{iteration}.wav')
    shutil.copy2(audio_path, target_path)

    # Run the captioning script
    command = [env_path, script_path, '--gpu=0', '--audio_path', target_path]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    output = result.stdout.strip()

    # Delete the copied WAV file
    os.remove(target_path)

    return output

def run_genre_check(env_path, script_path, audio_path, genre, iteration):
    command = [env_path, script_path, '--audio', audio_path, '--genre', genre, '--iteration', str(iteration)]
    try:
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print("Error running genre check:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return "Error"

# Function to run demucs
def run_demucs(env_path, script_path, audio_path):
    command = [env_path, script_path, str(audio_path)]
    try:
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print("Error running demucs:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return "Error"
    


# MAIN

print("Generating music...")
initial_wav = run_first_music_generation(MUSICGEN_ENV_PATH, MUSICGEN2_SCRIPT_PATH, current_prompt)

print("Running genre recognition for initial prompt...")
# Genre checking for initial prompt
run_genre_check(GENRECHECK_ENV_PATH, GENRECHECK_SCRIPT_PATH, initial_wav, target_genre, f"initial_prompt")

print("Separating audio file into stems...")
run_demucs(DEMUCS_ENV_PATH, DEMUCS_SCRIPT_PATH, initial_wav)

print("Iterating stems...")
# Iterate over each file in the specified directory
for file_name in os.listdir(stem_directory):
    if file_name.endswith('.wav'):
        wav_file = os.path.join(stem_directory, file_name)
        filename_without_extension = os.path.splitext(file_name)[0]
        
        # Get the initial prompt for the first iteration based on the current WAV file
        current_prompt = run_captioning(CAPTIONING_ENV_PATH, CAPTIONING_SCRIPT_PATH, wav_file, 0, filename_without_extension)

        # Write the initial prompt to the CSV
        with open(csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)          
            writer.writerow([f"{filename_without_extension}_0", current_prompt])
        
        # Genre checking for first iteration
        run_genre_check(GENRECHECK_ENV_PATH, GENRECHECK_SCRIPT_PATH, wav_file, target_genre, f"{filename_without_extension}_0")


        for iteration in range(1, 11):
            print(f"Running iteration {filename_without_extension}_{iteration}...")
            print(f"Running music generation...")
            wav_file = run_music_generation(MUSICGEN_ENV_PATH, MUSICGEN_SCRIPT_PATH, iteration, current_prompt, filename_without_extension)
            
            print("Running captioning...")
            current_prompt = run_captioning(CAPTIONING_ENV_PATH, CAPTIONING_SCRIPT_PATH, wav_file, iteration, filename_without_extension)

            # Update CSV with the new prompt
            with open(csv_filename, 'a', newline='') as file:
                writer = csv.writer(file)
                # Extract the filename without extension and write the row
                filename_without_extension = os.path.splitext(file_name)[0]
                writer.writerow([f"{filename_without_extension}_{iteration}", current_prompt])
                #writer.writerow([iteration, current_prompt])
            
            print("Running genre recognition...")
            # Genre checking
            run_genre_check(GENRECHECK_ENV_PATH, GENRECHECK_SCRIPT_PATH, wav_file, target_genre, f"{filename_without_extension}_{iteration}")

            
            
            
            #print(f"Iteration {iteration} completed with prompt: {current_prompt}. Confidence in respect to {target_genre}: {target_confidence:.2f}. Predicted genre: {predicted_genre} with {max_confidence:.2f} confidence.")
            print(f"Iteration {filename_without_extension}_{iteration} completed with prompt: {current_prompt}")
            #print(f"Iteration {iteration} completed with prompt: {current_prompt} and confidence in respect to {target_genre}")
