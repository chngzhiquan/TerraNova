import streamlit as st
from datetime import datetime
from streamlit_js_eval import get_geolocation

# Import helpers and models
import utils
from audio_processor import identify_bird_sound, load_audio_model
from image_processor import identify_bird_image, load_image_model

st.set_page_config(page_title="Identify Species", page_icon="🔍")

# --- SECURITY CHECK ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("Please login on the Home page first.")
    st.stop()

# Load Models
with st.spinner("Loading AI Models..."):
    load_audio_model()
    load_image_model()

# Get Location for saving data later
loc = get_geolocation()
user_lat = loc['coords']['latitude'] if loc else 1.3521
user_lon = loc['coords']['longitude'] if loc else 103.8198

st.title("🔍 Identify Species")

# Create Tabs for cleaner mobile UI
tab1, tab2 = st.tabs(["📸 Visual Scanner", "🎙️ Audio Scanner"])

# --- VISUAL SCANNER TAB ---
with tab1:
    st.header("Visual Scanner")
    img_file = st.camera_input("Take a photo")

    if img_file:
        st.write("Processing...")
        try:
            results = identify_bird_image(img_file)
            top_match = results[0]
            common_name = top_match['name']
            confidence = top_match['score']

            if confidence >= 50:
                st.success(f"**Identified:** {common_name} ({confidence:.1f}%)")
                
                # Big button for mobile ease
                if st.button("✅ Confirm & Upload", use_container_width=True, key="save_img"):
                    date = datetime.now().strftime("%d/%m/%Y")
                    time = datetime.now().strftime("%H:%M:%S")
                    utils.save_new_sighting(date, time, user_lat, user_lon, common_name)
                    st.balloons()
            else:
                st.warning(f"Unsure. Best guess: {common_name}")
        except Exception as e:
            st.error(f"Error: {e}")

# --- AUDIO SCANNER TAB ---
with tab2:
    st.header("Bio-Acoustics")
    audio_value = st.audio_input("Record Sound")

    if audio_value:
        st.audio(audio_value)
        temp_filename = "temp_recording.wav"
        with open(temp_filename, "wb") as f:
            f.write(audio_value.read())       
        try:
            matches = identify_bird_sound(temp_filename)
            if matches:
                st.success(f"**{len(matches)} Species Detected**")
                for bird in matches:
                    st.info(f"🐦 {bird['name']} ({bird['score']:.0f}%)")
            else:
                st.warning("No clear bird calls detected.")
        except Exception as e:
            st.error(f"Error: {e}")