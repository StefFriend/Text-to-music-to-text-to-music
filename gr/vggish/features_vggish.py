import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import vggish_slim
import vggish_params
import vggish_input
import vggish_postprocess


# Path ai file necessari
checkpoint_path = 'vggish_model.ckpt'
pca_params_path = 'vggish_pca_params.npz'


def extract_features(audio_path):
    # Crea un'istanza del modello VGGish.
    with tf.Graph().as_default(), tf.Session() as sess:
        vggish_slim.define_vggish_slim()
        vggish_slim.load_vggish_slim_checkpoint(sess, checkpoint_path)

        # Crea il postprocessore per trasformare gli embeddings.
        postprocessor = vggish_postprocess.Postprocessor(pca_params_path)

        # Estrai le caratteristiche dal file audio.
        features = vggish_input.wavfile_to_examples(audio_path)
        [embedding_batch] = sess.run([vggish_params.EMBEDDING_LAYER_NAME],
                                     feed_dict={vggish_params.INPUT_TENSOR_NAME: features})

        # Postprocessa gli embeddings.
        postprocessed_batch = postprocessor.postprocess(embedding_batch)

    return postprocessed_batch