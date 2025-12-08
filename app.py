import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from audio_recorder_streamlit import audio_recorder
from folium.plugins import LocateControl
from mapping_hotspots import update_hotspots
import os
from datetime import datetime

def save_new_sighting(date, time, lat, lon, scientific_name, common_name):
    master_db_file = 'sightings.csv'
    new_id = 1
    if os.path.exists(master_db_file):
        try:
            existing_df = pd.read_csv(master_db_file)
            if not existing_df.empty:
                new_id = existing_df['id'].max() + 1
        except ValueError:
            pass  # File exists but is empty or malformed
        except pd.errors.EmptyDataError:
            pass  # File exists but is empty

    # 1. Prepare the new row
    new_data = pd.DataFrame({
        'id': [new_id],
        'date_observed': [date],
        'time_observed': [time],
        'latitude': [lat],
        'longitude': [lon],
        'scientific_name': [scientific_name],
        'common_name': [common_name]
    })

    # 2. Append to CSV
    # mode='a' means append
    # header=False means don't write the column names again if file exists
    if os.path.exists(master_db_file):
        new_data.to_csv(master_db_file, mode='a', header=False, index=False)
    else:
        # If file doesn't exist, create it with headers
        new_data.to_csv(master_db_file, mode='w', header=True, index=False)

    # 3. Trigger the Pipeline
    st.toast("Processing new hotspot data...")
    try:
        update_hotspots() # Runs the external script
        st.success("Map Updated!")
    except Exception as e:
        st.error(f"Pipeline Error: {e}")

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TerraNova", layout="wide", page_icon="🌏")
st.title("🌏 TerraNova")

# --- 2. DATA LOAD ---
@st.cache_data
def load_data():
    try:
        # Load the PROCESSED file
        return pd.read_csv('final_hotspots.csv') 
    except:
        return pd.DataFrame()

df = load_data()

# --- 3. GPS data ---
loc = get_geolocation()

# Default to Singapore (or your data center) if GPS hasn't loaded yet
user_lat = 1.3521
user_lon = 103.8198

# Overwrite if we have real GPS data (from streamlit_js_eval)
if loc:
    user_lat = loc['coords']['latitude']
    user_lon = loc['coords']['longitude']

with st.sidebar:
    st.header("📍 Navigation")
    
    # GPS Status Indicator
    if loc:
        st.success(f"Signal Locked\nLat: {user_lat:.4f}\nLon: {user_lon:.4f}")
    else:
        st.warning("Signal Searching... (Allow Location)")

    st.divider()
    st.subheader("🎙️ Bio-Acoustics")
    st.write("Record surrounding calls:")
    audio_bytes = audio_recorder(pause_threshold=2.0, icon_size="2x")
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.info("Analyzing frequency...")
        # (Placeholder for Audio AI Logic)
        st.write("Potential Match: **Asian Koel** (80%)")

    st.divider()
    st.subheader("📸 Visual Scanner")
    img_file = st.camera_input("Scan Animal")

    if img_file:
        st.write("Processing visual data...")
            
        # (Placeholder for your AI model)
        common_name = "Red Junglefowl" 
            
        st.success(f"**Identified:**\n### {common_name}")
            
        # -- SAVE BUTTON --
        # Only appears after a photo is taken
        if st.button("Confirm & Upload Data", use_container_width=True):
            date = datetime.now().strftime("%d/%m/%Y")
            time = datetime.now().strftime("%H:%M:%S")
            #save_new_sighting(date, time, lat, lon, scientific_name, common_name) # (Placeholder for save function)
            st.balloons()
            st.toast(f"Saved {common_name} to database!")
            st.rerun()

# --- 4. MAP RENDERING ---
# Base Map (Dark Mode)
m = folium.Map(location=[user_lat, user_lon], zoom_start=18, tiles="CartoDB dark_matter")
    
# This enables the "Google Maps" style blue dot to track the user
LocateControl(
    auto_start=True,
    strings={"title": "My Location"},
    flyTo=True
).add_to(m)
    
# Plot Data
if not df.empty:
    for index, row in df.iterrows():
            
    # --- CUSTOM ICON LOGIC ---
        name = str(row['common_name'])
            
        if "Junglefowl" in name:
            icon_name = "fire"       # Represents the Red comb / ground bird
            icon_color = "red"
        elif "Myna" in name:
            icon_name = "volume-up"  # Represents a noisy bird
            icon_color = "purple"
        elif "Starling" in name:
            icon_name = "star"       # Pun on "Star"-ling
            icon_color = "green"
        else:
            icon_name = "leaf"       # Default for others
            icon_color = "gray"

        # --- 1. FIXED RADIUS (No longer dynamic) ---
        radius = 50
            
        # --- 2. DRAW HOME RANGE ---
        folium.Circle(
            [row['lat'], row['lon']],
            radius=radius,
            color=icon_color,
            fill=True,
            fill_opacity=0.2,
            weight=1,
            popup=name
        ).add_to(m)
            
        # --- 3. DRAW OBSERVATION POST (PIN) ---
        sightings = row.get('sighting_count', 0)
            
        # Only show pin if verified (>= 3 sightings)
        if sightings >= 3: 
            folium.Marker(
                [row['lat'], row['lon']],
                icon=folium.Icon(color=icon_color, icon=icon_name), # Custom Icon
                tooltip=f"{name} ({sightings} sightings)"
            ).add_to(m)

st_folium(m, height=700, width="100%")