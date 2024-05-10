from __future__ import print_function

import os
import numpy as np
import librosa
import resampy
import tensorflow.compat.v1 as tf
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import warnings
import argparse
import csv

from vggish import vggish_input, vggish_params, vggish_postprocess, vggish_slim

# Suppress warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

#print('\nStart VGGish\n')

checkpoint_path = 'gr/vggish/vggish_model.ckpt'
pca_params_path = 'gr/vggish/vggish_pca_params.npz'
sr = 16000  # Sample rate for VGGish

# Load the model and label encoder only once
model_genre_recognition = load_model('gr/modello_completo.h5')
genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
label_encoder = LabelEncoder()
label_encoder.fit(genres)

def process_file(file_path):
    try:
        audio, sr_audio = librosa.load(file_path, sr=None)
        if sr_audio != sr:
            audio = resampy.resample(audio, sr_audio, sr)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

    input_batch = vggish_input.waveform_to_examples(audio, sr)
    if input_batch.shape[0] < 31:
        padding = np.zeros((31 - input_batch.shape[0], input_batch.shape[1], input_batch.shape[2]))
        input_batch = np.concatenate((input_batch, padding), axis=0)
    elif input_batch.shape[0] > 31:
        input_batch = input_batch[:31]

    with tf.Graph().as_default(), tf.Session() as sess:
        vggish_slim.define_vggish_slim()
        vggish_slim.load_vggish_slim_checkpoint(sess, checkpoint_path)
        features_tensor = sess.graph.get_tensor_by_name(vggish_params.INPUT_TENSOR_NAME)
        embedding_tensor = sess.graph.get_tensor_by_name(vggish_params.OUTPUT_TENSOR_NAME)
        embedding_batch = sess.run([embedding_tensor], feed_dict={features_tensor: input_batch})
    
    pproc = vggish_postprocess.Postprocessor(pca_params_path)
    return pproc.postprocess(embedding_batch[0])

def genre_rec(embedding, target_genre):
    embedding = embedding.reshape(-1, 31, 128, 1).astype('float32')
    try:
        predictions = model_genre_recognition.predict(embedding)
        predicted_indices = np.argmax(predictions, axis=1)
        predicted_genres = label_encoder.inverse_transform(predicted_indices)
        target_index = label_encoder.transform([target_genre])[0]
        target_confidence = predictions[0][target_index] * 100

        max_index = np.argmax(predictions[0])
        max_confidence = predictions[0][max_index] * 100
        max_genre = label_encoder.inverse_transform([max_index])[0]
        return predicted_genres[0], max_confidence, target_genre, target_confidence
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0.0

def main():
    parser = argparse.ArgumentParser(description="Predict the genre of an audio file.")
    parser.add_argument("--audio", type=str, required=True, help="Path to the audio file.")
    parser.add_argument("--genre", type=str, choices=genres, required=True, help="Target genre to predict confidence for.")
    parser.add_argument("--iteration", type=str, required=True, help="Iteration number for csv writing.")

    args = parser.parse_args()

    embeddings = process_file(args.audio)
    predicted_genre, max_confidence, target_genre, target_confidence = genre_rec(embeddings, args.genre)
    #print(f"Target Genre: {target_genre}, Confidence: {target_confidence:.2f}%")
    #print(f"Predicted Genre: {predicted_genre}, Confidence: {max_confidence:.2f}%")
    print(target_confidence, predicted_genre, max_confidence)

    #print(type(target_confidence), type(predicted_genre), type(max_confidence))


    # Convert target_confidence and max_confidence to formatted strings
    formatted_target_confidence = f"{target_confidence:.2f}%"
    formatted_max_confidence = f"{max_confidence:.2f}%"
    # Path to the CSV file
    csv_filename = 'infinitystem/prompts.csv'  # Assuming the file is in the current directory

    # Temporary list to hold rows
    updated_rows = []

    # Reading the existing data
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if str(row[0]) == args.iteration:  # Check if the iteration matches
                # Update the row with the new data
                row.extend([formatted_target_confidence, predicted_genre, formatted_max_confidence])
            updated_rows.append(row)

    # Writing the updated data back to the CSV
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updated_rows)

    print(f"Updated CSV for iteration {args.iteration} with genre prediction details.")


if __name__ == "__main__":
    main()
