from transformers import pipeline
from PIL import Image
import streamlit as st

# 1. LOAD YOUR CUSTOM MODEL FROM HUGGING FACE
@st.cache_resource(show_spinner=False)
def load_image_model():
    model_path = "zhiquanchng/singapore-bird-classifier"
    
    return pipeline("image-classification", model=model_path)

# 2. LABEL CLEANER
def clean_label(label):
    return label.replace("_", " ").title()

# 3. IDENTIFY IMAGE
def identify_bird_image(image_file):
    pipe = load_image_model()
    img = Image.open(image_file)
    
    # Get Top 3 predictions
    predictions = pipe(img, top_k=3)
    
    results = []
    for p in predictions:
        # Clean up the label
        clean_name = clean_label(p['label'])
        score_pct = p['score'] * 100
        
        results.append({
            'name': clean_name,
            'score': score_pct,
            'raw_label': p['label']
        })
        
    return results