import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.plugins import LocateControl, MarkerCluster, HeatMap
from streamlit_js_eval import get_geolocation
import os

# Import your helper file
import utils 

# --- CONFIG ---
st.set_page_config(page_title="TerraNova", layout="wide", page_icon="🌏")
utils.make_map_responsive()

# --- SESSION STATE & LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user'] = None

if not st.session_state['logged_in']:
    st.markdown("""<style>[data-testid="stSidebar"] { display: none; }</style>""", unsafe_allow_html=True)
    st.title("🌏 TerraNova Login")
    with st.form("login_form"):
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if utils.check_login(user, pwd):
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.rerun()
            else:
                st.error("Invalid credentials.")
    st.stop()

# --- GEOSPATIAL LOGIC ---
@st.cache_data
def load_geodata():
    """
    1. Loads raw bird sightings.
    2. Loads park boundaries.
    3. Keeps only birds found INSIDE parks.
    """
    # 1. Load Raw Bird Data
    if not os.path.exists('sightings.csv'):
        return pd.DataFrame(), None # Return empty if missing
        
    df = pd.read_csv('sightings.csv')
    
    # Convert to GeoDataFrame (Points)
    gdf_birds = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326"
    )

    # 2. Load Park Boundaries (Polygon)
    park_path = os.path.join("data", "parks.geojson")
    
    if os.path.exists(park_path):
        try:
            gdf_parks = gpd.read_file(park_path) 
            # Ensure Coordinate System matches
            if gdf_parks.crs != "EPSG:4326":
                gdf_parks = gdf_parks.to_crs("EPSG:4326")
            
            # 3. Spatial Join: Filter birds strictly inside parks
            # 'inner' join drops birds on roads/buildings
            birds_in_parks = gpd.sjoin(gdf_birds, gdf_parks, how="inner", predicate="within")
            return birds_in_parks, gdf_parks
        except Exception as e:
            st.warning(f"Error reading park file: {e}. Showing all birds.")
            return gdf_birds, None
    else:
        # Fallback: If no park file exists yet, just return all birds
        return gdf_birds, None

# Load Data
gdf_birds, gdf_parks = load_geodata()

# --- SIDEBAR CONTROLS ---
st.sidebar.title(f"Welcome, {st.session_state['user']}")
st.sidebar.markdown("---")
st.sidebar.header("🗺️ Map Filters")

# Filter 1: Species (Crucial for raw data)
if not gdf_birds.empty:
    # Get top 20 most common birds to prevent a massive list
    top_birds = gdf_birds['common_name'].value_counts().head(20).index.tolist()
    all_species = sorted(gdf_birds['common_name'].unique())
    
    selected_species = st.sidebar.multiselect(
        "Select Species", 
        all_species, 
        default=top_birds[:3] # Default to top 3 common birds
    )
    
    if selected_species:
        filtered_birds = gdf_birds[gdf_birds['common_name'].isin(selected_species)]
    else:
        filtered_birds = gdf_birds
else:
    filtered_birds = pd.DataFrame()

# Filter 2: Visualization Style
viz_type = st.sidebar.radio("Visualization Style", ["Heatmap (Density)", "Clusters (Grouped)", "Raw Points"])

# Filter 3: Toggle Parks
if gdf_parks is not None:
    show_parks = st.sidebar.checkbox("Show Park Boundaries", value=True)
else:
    show_parks = False

# --- MAP RENDERING ---

# GPS Handling
loc = get_geolocation()
user_lat, user_lon = 1.3521, 103.8198 # Default Singapore Center
if loc:
    user_lat = loc['coords']['latitude']
    user_lon = loc['coords']['longitude']

# Create Map
m = folium.Map(location=[user_lat, user_lon], zoom_start=14, tiles="CartoDB dark_matter")
LocateControl(auto_start=True, strings={"title": "Me"}).add_to(m)

# Layer 1: Parks
if show_parks and gdf_parks is not None:
    folium.GeoJson(
        gdf_parks,
        name="Parks",
        style_function=lambda x: {
            'fillColor': '#228B22', 
            'color': '#006400',
            'weight': 1,
            'fillOpacity': 0.3,
        },
        # Adjust 'name' if your shapefile uses a different column header (e.g. 'LU_DESC')
        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Park:']) 
    ).add_to(m)

# Layer 2: Birds
if not filtered_birds.empty:
    
    # STYLE A: HEATMAP (Best for spotting trends)
    if viz_type == "Heatmap (Density)":
        heat_data = [[row['latitude'], row['longitude']] for index, row in filtered_birds.iterrows()]
        HeatMap(heat_data, radius=15, blur=10, min_opacity=0.4).add_to(m)

    # STYLE B: CLUSTERS (Best for data exploration)
    elif viz_type == "Clusters (Grouped)":
        marker_cluster = MarkerCluster().add_to(m)
        for index, row in filtered_birds.iterrows():
            name = row['common_name']
            # Dynamic Icon Color based on species name
            color = "red" if "Junglefowl" in name else "purple" if "Myna" in name else "green"
            
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=name,
                icon=folium.Icon(color=color, icon="leaf"),
            ).add_to(marker_cluster)

    # STYLE C: RAW POINTS (Best for precision)
    else:
        for index, row in filtered_birds.iterrows():
            name = row['common_name']
            color = "red" if "Junglefowl" in name else "purple" if "Myna" in name else "green"
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=4,
                color=color,
                fill=True,
                fill_opacity=0.8,
                popup=name
            ).add_to(m)

# Render Map
st_folium(m, height=700, width="100%")

# Stats Footer
st.markdown(f"**Total Sightings Displayed:** {len(filtered_birds)}")