# Text-to-music-to-text-to-music

Code repository for Polimi MAE Capstone - Project L-14 

## Description
This project explores the capabilities of artificial intelligence (AI) in the domains of music generation and audio captioning. We focus on two primary objectives:
- Analyzing the ability of AI systems to maintain both semantic and musical coherence across multiple iterations of content generation.
- Exploring the transformations and variations in musical and textual content through an iterative process.

The project is based on:

1. Music Generation
   We utilized MusicGen, a state-of-the-art AI model developed by Meta (formerly Facebook), to generate high-quality music from textual descriptions. MusicGen's multi-head attention mechanism allows it to align generated      music closely with the semantic content of textual prompts. For this project, we employed the facebook/musicgen-medium model, which consists of a 1.5B parameter model for text-to-music conversion.

2. Music Separation
   Demucs, a U-Net architecture model, was used for music source separation. It features an encoder and decoder with convolutional layers to downsample and upsample the input waveform, producing separate waveforms for each    source. We utilized the model with model=mdx_extra pre-trained weights and a segment parameter set to 12, enhancing the model's capability in source separation.

3. Music Captioning
   LP-Music Caps, an AI model specialized in creating textual descriptions of audio content, was employed for music captioning. It leverages a transformer-based framework to capture complex temporal dynamics and patterns      within musical compositions, producing detailed and contextually relevant captions.

4. Genre Recognition
   For genre recognition, we utilized a convolutional neural network (CNN) composed of various layers designed to transform and reduce the dimensions of embeddings. This CNN was trained using the public GTZAN dataset,         organized into 10 musical genres.

5. Iterative Process
   Each initial prompt stem underwent ten iterations through a cycle of captioning, regeneration, classification, and data collection. This iterative process aimed to assess the stability and accuracy of genre recognition     in AI-generated music.

We obtained three [results](https://steffriend.github.io/Text-to-music-to-text-to-music/):
- Prompt 1: Blues - The generated music was coherent with the blues genre, though genre recognition confidence was low.
- Prompt 2: Classical - The generated music was coherent, with a high confidence score in genre recognition.
- Prompt 3: Reggae - The generated music was coherent, with a high confidence score in genre recognition.


The project successfully demonstrated the cyclic process of generating music from text and vice versa, emphasizing both the potential and challenges of iterative generative models. The iterative cycles introduced variations that highlighted the creative potential of these models, while also indicating the need for improved consistency and genre recognition. The observed genre-specific instability suggests varying levels of AI model adaptability to different musical styles, highlighting critical areas for future research and refinement.

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
