import os
import numpy as np

# Get the base directory
basedir = os.getcwd()
dirname = basedir+ "/Data/genres_original"

# Create lists for audio paths and labels
audio_paths = []
audio_label = []
# Print all the files in different directories
for root, dirs, files in os.walk(dirname, topdown=False):
    for filenames in files:
        if filenames.find('.wav') != -1:

            audio_paths.append(os.path.join(root, filenames))
            filenames = filenames.split('.', 1)
            filenames = filenames[0]
            audio_label.append(filenames)
audio_paths = np.array(audio_paths)
audio_label = np.array(audio_label)