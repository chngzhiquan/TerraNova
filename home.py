import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import LocateControl
from streamlit_js_eval import get_geolocation

# Import our new helper file
import utils 

# --- CONFIG ---
st.set_page_config(page_title="TerraNova", layout="wide", page_icon="🌏")
utils.make_map_responsive()

# --- SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user'] = None

# --- LOGIN SCREEN ---
if not st.session_state['logged_in']:
    st.markdown("""
                <style>
                    [data-testid="stSidebar"] { display: none; }
                </style>
                """, unsafe_allow_html=True)
    st.title("🌏 TerraNova Login")
    with st.form("login_form"):
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if utils.check_login(user, pwd):
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.rerun()
            else:
                st.error("Invalid credentials.")
    st.stop()

# --- MAIN MAP LOGIC ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv('final_hotspots.csv') 
    except:
        return pd.DataFrame()

df = load_data()

# GPS Handling
loc = get_geolocation()
user_lat = 1.3521
user_lon = 103.8198
if loc:
    user_lat = loc['coords']['latitude']
    user_lon = loc['coords']['longitude']

# Draw Map
m = folium.Map(location=[user_lat, user_lon], zoom_start=18, tiles="CartoDB dark_matter")
LocateControl(auto_start=True, strings={"title": "My Location"}, flyTo=True).add_to(m)

if not df.empty:
    for index, row in df.iterrows():
        name = str(row['common_name'])
        # Simple icon logic
        icon_color = "red" if "Junglefowl" in name else "purple" if "Myna" in name else "green"
        
        folium.Circle(
            [row['lat'], row['lon']], radius=50, color=icon_color, 
            fill=True, fill_opacity=0.2, weight=1, popup=name
        ).add_to(m)
        
        if row.get('sighting_count', 0) >= 3: 
            folium.Marker(
                [row['lat'], row['lon']],
                icon=folium.Icon(color=icon_color, icon="leaf"),
                tooltip=f"{name}"
            ).add_to(m)

st_folium(m, height=700, width="100%")