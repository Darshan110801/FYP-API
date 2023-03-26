import os
from django.apps import AppConfig
import tensorflow as tf
from sentence_transformers import SentenceTransformer


class RestApisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'REST_APIS'
    sentence_transformer = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    this_dir = os.path.dirname(__file__)
    cnn_model = tf.keras.models.load_model(f"{this_dir}/models/sbert_cnn.h5")

