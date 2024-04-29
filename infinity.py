import os
import shutil
import subprocess
import csv
import argparse
from sklearn.preprocessing import LabelEncoder


# Argument parsing setup
parser = argparse.ArgumentParser(description='Run music generation and captioning.')
parser.add_argument('--prompt', type=str, required=True, help='Initial prompt for music generation')
parser.add_argument('--genre', type=str, required=True, help='Target genre')
args = parser.parse_args()

# Using the passed argument
current_prompt = args.prompt
target_genre = args.genre

# Paths setup
base_dir = os.path.dirname(os.path.abspath(__file__))
wav_directory = os.path.join(base_dir, 'wav')
captioning_directory = r'C:\Users\SAA\Documents\Polimi\CAPSTONE\infinityLoop\music_captioning'
genre_check_directory = r'C:\Users\SAA\Documents\Polimi\CAPSTONE\infinityLoop\gr'


MUSICGEN_ENV_PATH = r'C:\Users\SAA\.conda\envs\musicgen\python.exe'
MUSICGEN_SCRIPT_PATH = os.path.join(base_dir, 'musicgen', 'gen.py')
CAPTIONING_ENV_PATH = r'C:\Users\SAA\.conda\envs\lp\python.exe'
CAPTIONING_SCRIPT_PATH = os.path.join(captioning_directory, 'captioning2.py')
GENRECHECK_ENV_PATH = r'C:\Users\SAA\.conda\envs\genre\python.exe'
GENRECHECK_SCRIPT_PATH = os.path.join(genre_check_directory, 'genrecheck.py')

# Initialize the CSV file with headers
csv_filename = os.path.join(base_dir, 'prompts.csv')
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Iteration', 'Prompt', f'{target_genre} Confidence', 'Predicted Genre', 'Predicted Genre Confidence'])
    # Log the initial prompt with iteration 0
    writer.writerow([0, current_prompt])

# Function to run music generation
def run_music_generation(env_path, script_path, iteration, prompt):
    wav_filename = os.path.join(wav_directory, f'iteration_{iteration}.wav')
    command = [env_path, script_path, '-prompt', prompt, '-iteration', str(iteration)]
    subprocess.run(command, check=True)
    return wav_filename

# Function to run captioning
def run_captioning(env_path, script_path, audio_path, iteration):
    # Copy WAV file to the captioning directory
    target_path = os.path.join(captioning_directory, f'iteration_{iteration}.wav')
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

# Main loop
for iteration in range(1, 51):
    print(f"Running iteration {iteration}")
    wav_file = run_music_generation(MUSICGEN_ENV_PATH, MUSICGEN_SCRIPT_PATH, iteration, current_prompt)
    
    current_prompt = run_captioning(CAPTIONING_ENV_PATH, CAPTIONING_SCRIPT_PATH, wav_file, iteration)

    # Update CSV with the new prompt
    with open(csv_filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([iteration, current_prompt])
        #writer.writerow([iteration, current_prompt])

    # Genre checking
    run_genre_check(GENRECHECK_ENV_PATH, GENRECHECK_SCRIPT_PATH, wav_file, target_genre, iteration)

    
    
    
    #print(f"Iteration {iteration} completed with prompt: {current_prompt}. Confidence in respect to {target_genre}: {target_confidence:.2f}. Predicted genre: {predicted_genre} with {max_confidence:.2f} confidence.")
    print(f"Iteration {iteration} completed with prompt: {current_prompt}")
    #print(f"Iteration {iteration} completed with prompt: {current_prompt} and confidence in respect to {target_genre}")
