import numpy as np
import streamlit as st
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from datetime import datetime

# 1. CACHED MODEL LOADING
# We use st.cache_resource so we don't download the 500MB AI model every time you click record
@st.cache_resource(show_spinner=False)
def load_audio_model():
    # This initializes the BirdNet Analyzer
    analyzer = Analyzer()
    return analyzer

# 2. IDENTIFY SPECIES (BirdNET)
def identify_bird_sound(audio_file):
    # Retrieve the cached analyzer
    analyzer = load_audio_model()
    
    # This is BirdNET's "Superpower": It filters out non-native birds automatically.
    recording = Recording(
        analyzer,
        audio_file,
        lat=1.3521,       # Singapore Latitude
        lon=103.8198,     # Singapore Longitude
        date=datetime.now(), # Helps filter migratory birds based on season
        min_conf=0.5,     # Sensitivity (0.5 is a good balance)
    )
    
    # Run the analysis
    recording.analyze()
    
    # Format results for the App
    # We convert BirdNET's format to our standard list: [{'name': 'Koel', 'score': 95.0}, ...]
    valid_matches = []
    
    if recording.detections:
        for d in recording.detections:
            # BirdNET returns confidence as 0.0-1.0, we convert to 0-100
            score_pct = d['confidence'] * 100
            
            valid_matches.append({
                'name': d['common_name'],
                'score': score_pct
            })
            
    # Sort by highest confidence first
    valid_matches.sort(key=lambda x: x['score'], reverse=True)
            
    return valid_matches