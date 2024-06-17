# Text-to-music-to-text-to-music

Code repository for Polimi MAE Capstone - Project L-14 


## Requirements

To install the required Python packages, run:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone this repository.
2. Ensure the following directory paths are correctly set in the script:
   - `prompt_directory`
   - `wav_directory`
   - `stem_directory`
   - `captioning_directory`
   - `genre_check_directory`
   - `demucs_directory`

3. Set the paths to your Python environments and scripts:
   - `MUSICGEN_ENV_PATH`
   - `MUSICGEN_SCRIPT_PATH`
   - `MUSICGEN2_SCRIPT_PATH`
   - `CAPTIONING_ENV_PATH`
   - `CAPTIONING_SCRIPT_PATH`
   - `GENRECHECK_ENV_PATH`
   - `GENRECHECK_SCRIPT_PATH`
   - `DEMUCS_ENV_PATH`
   - `DEMUCS_SCRIPT_PATH`

## Usage

Run the script with the following arguments:

```bash
python script_name.py --prompt "your prompt" --genre "target genre"
```

### Arguments

- `--prompt`: Initial prompt for music generation.
- `--genre`: Target genre for the generated music.

## Script Workflow

1. **Generate Music**: Creates an initial music piece based on the prompt.
2. **Genre Recognition**: Checks the genre of the initial music.
3. **Demucs Separation**: Splits the music into individual stems.
4. **Iterate Stems**: Generates new music for each stem and iterates the process, updating the prompts and checking genres.

## CSV Logging

The script logs all prompts and genre recognition results in `prompts.csv` within the `prompt_directory`.

## Notes

- Ensure all required directories and environment paths are correctly configured.
- Modify the script paths and environment paths based on your setup.
