import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from transformers import pipeline

# 1. CACHED MODEL LOADING
# We use st.cache_resource so we don't download the 500MB AI model every time you click record
@st.cache_resource
def load_audio_model():
    # This downloads a specific model trained on bird sounds
    # You can swap this string for other huggingface models
    model_id = "dima806/bird_species_classification" 
    pipe = pipeline("audio-classification", model=model_id)
    return pipe

# 2. GENERATE SPECTROGRAM
def create_spectrogram(audio_file):
    # Load audio (Librosa automatically converts to mono and correct sample rate)
    y, sr = librosa.load(audio_file)
    
    # Create the Mel Spectrogram (The "Image" of sound)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB_mel = librosa.power_to_db(S, ref=np.max)
    
    # Plot it using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 4))
    img = librosa.display.specshow(S_dB_mel, x_axis='time', y_axis='mel', sr=sr, ax=ax, cmap='inferno')
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set_title('Audio Spectrogram')
    plt.tight_layout()
    
    return fig

# 3. IDENTIFY SPECIES
def identify_bird_sound(audio_file):
    pipe = load_audio_model()
    target_species = ["Red Junglefowl", "Common Myna", "Asian Glossy Starling"]
    raw_predictions = pipe(audio_file, top_k=10)
    valid_matches = []
    
    for p in raw_predictions:
        score_pct = p['score'] * 100
        for target in target_species:
            if target.lower() in p['label'].lower():
                valid_matches.append({
                    'name': p['label'],
                    'score': score_pct
                })
                break                     
    return valid_matches