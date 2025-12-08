import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Bio-Compass", layout="wide", page_icon="🧭")
st.title("🧬 TerraNova")

# --- 2. DATA LOAD ---
@st.cache_data
def load_data():
    try:
        # Load the PROCESSED file
        return pd.read_csv('final_hotspots.csv') 
    except:
        return pd.DataFrame()

df = load_data()

# --- 3. GPS SIMULATOR (Sidebar) ---
with st.sidebar:
    st.header("📍 Navigation")
    
    # Determine default start location
    if not df.empty:
        default_lat = df.iloc[0]['lat']
        default_lon = df.iloc[0]['lon']
    else:
        default_lat = 1.3521
        default_lon = 103.8198

    st.info("Simulate walking by adjusting coordinates:")
    user_lat = st.number_input("Latitude", value=default_lat, format="%.5f")
    user_lon = st.number_input("Longitude", value=default_lon - 0.0005, format="%.5f")
    
    st.divider()
    st.subheader("📸 Universal Scanner")
    img_file = st.camera_input("Scan Habitat")

# --- 4. MAP RENDERING ---
col1, col2 = st.columns([3, 1])

with col1:
    # Base Map (Dark Mode)
    m = folium.Map(location=[user_lat, user_lon], zoom_start=18, tiles="CartoDB dark_matter")
    
    # Plot User (Blue Dot)
    folium.Marker(
        [user_lat, user_lon], 
        tooltip="You", 
        icon=folium.Icon(color="blue", icon="user")
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

    st_folium(m, height=500, width="100%")

# --- 5. LOGIC ENGINE (Scanning Analysis) ---
with col2:
    st.subheader("📡 Sensor Log")

    if img_file:
        # --- SIMULATE AI IDENTIFICATION ---
        st.write("Processing visual data...")
        detected_species = "Red Junglefowl" # Placeholder
        confidence = "98%"
        
        st.success(f"**Identified:** {detected_species}")
        
        # --- CALCULATE CONTEXT ---
        nearest_dist = 99999
        nearest_name = "Unknown"
        
        if not df.empty:
            for index, row in df.iterrows():
                dist = geodesic((user_lat, user_lon), (row['lat'], row['lon'])).meters
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest_name = row['common_name']

        st.divider()
        
        # --- DECISION LOGIC ---
        if nearest_dist < 50:
            st.info(f"✅ **HABITAT VERIFIED**")
            st.write(f"Confirmed historical data for **{nearest_name}**.")
            st.metric("Reward", "+50 XP")
        else:
            st.balloons()
            st.warning(f"🚀 **NEW DISCOVERY**")
            st.write("You are mapping a new zone (Terra Incognita).")
            st.metric("Reward", "+200 XP (Pioneer Bonus)")
            
        with st.expander("Field Guide Unlocked"):
            st.write("Ranger: 'Excellent data. Adding to global repository.'")

    else:
        st.write("Waiting for input...")
        if not df.empty:
            nearest_dist = 99999
            for index, row in df.iterrows():
                dist = geodesic((user_lat, user_lon), (row['lat'], row['lon'])).meters
                if dist < nearest_dist:
                    nearest_dist = dist
            
            st.metric("Nearest Outpost", f"{int(nearest_dist)}m")