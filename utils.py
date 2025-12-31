import streamlit as st
import pandas as pd
import pandas as np
import io
import os

# --- 1. DATA PIPELINE (Formerly mapping_hotspots.py) ---
def update_hotspots():
    # This runs the logic to aggregate raw sightings into grid squares
    print("🔄 Processing raw data...")
    try:
        df = pd.read_csv('sightings.csv') 
        print(f"   - Found {len(df)} raw sightings.")

        # GRID ALGORITHM: Rounding to 3 decimal places (approx 110m)
        df['lat_grid'] = df['latitude'].round(3)
        df['lon_grid'] = df['longitude'].round(3)

        # AGGREGATE: Group by Species + Grid
        hotspots = df.groupby(
            ['common_name', 'lat_grid', 'lon_grid']
        ).size().reset_index(name='sighting_count')

        # FILTER: Only keep verified hotspots (>= 3 sightings)
        verified_hotspots = hotspots[hotspots['sighting_count'] >= 3].copy()
        
        # FORMAT: Rename back to lat/lon for the map
        verified_hotspots.rename(columns={'lat_grid': 'lat', 'lon_grid': 'lon'}, inplace=True)

        # SAVE
        output_file = 'final_hotspots.csv'
        verified_hotspots.to_csv(output_file, index=False)  
        print(f"✅ Hotspots updated! ({len(verified_hotspots)} verified locations)")
        return True
        
    except FileNotFoundError:
        print("⚠️ No sightings.csv found yet.")
        return False
    except Exception as e:
        print(f"❌ Pipeline Error: {e}")
        return False

# --- 2. CSS STYLING ---
def make_map_responsive():
    st.markdown("""
        <style>
            .block-container { padding: 0rem !important; margin: 0px !important; max-width: 100% !important; }
            header[data-testid="stHeader"] { background-color: transparent !important; z-index: 1; }
            footer {visibility: hidden;}
            iframe { width: 100% !important; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE MANAGEMENT ---
def save_new_sighting(date, time, lat, lon, common_name,username):
    master_db_file = 'sightings.csv'
    new_id = 1
    
    # Check existing ID to increment
    if os.path.exists(master_db_file):
        try:
            existing_df = pd.read_csv(master_db_file)
            if not existing_df.empty:
                new_id = existing_df['id'].max() + 1
        except:
            pass

    # Prepare new row
    new_data = pd.DataFrame({
        'id': [new_id], 'date_observed': [date], 'time_observed': [time],
        'latitude': [lat], 'longitude': [lon], 'common_name': [common_name], 'username':[username]
    })

    # Append to CSV
    if os.path.exists(master_db_file):
        new_data.to_csv(master_db_file, mode='a', header=False, index=False)
    else:
        new_data.to_csv(master_db_file, mode='w', header=True, index=False)

    # TRIGGER THE PIPELINE IMMEDIATELY
    st.toast("Processing new hotspot data...")
    try:
        success = update_hotspots() # Calling the function directly
        if success:
            st.success("Map Updated!")
        else:
            st.warning("Data saved, but map update skipped (no data yet).")
    except Exception as e:
        st.error(f"Pipeline Error: {e}")

# --- 4. LOGIN LOGIC ---
def check_login(username, password):
    try:
        users_df = pd.read_csv('users.csv')
        user_match = users_df[users_df['username'] == username]
        if not user_match.empty:
            stored_password = str(user_match.iloc[0]['password'])
            if str(password) == stored_password:
                return True
        return False
    except FileNotFoundError:
        st.error("System Error: users.csv not found.")
        return False

# --- 5. ENTROPY ---
def calculate_entropy(df):
    """Returns the entropy (uncertainty) of the current list of birds."""
    if len(df) == 0: return 0
    probs = df['Species'].value_counts() / len(df)
    return -np.sum(probs * np.log2(probs))

def get_best_question(df, considered_features):
    """
    Finds the specific Question (Feature + Value) that best splits the data 50/50.
    Example: 'Is Primary_Color == White?' might split the data 4 vs 7.
    """
    base_entropy = calculate_entropy(df)
    best_info_gain = -1
    best_question = None # Will store tuple: (Feature_Column, Value_To_Ask)

    # Columns we can ask about (exclude Species and Special_Feature usually)
    askable_columns = [col for col in df.columns if col not in ['Species', 'Special_Feature'] and col not in considered_features]

    for col in askable_columns:
        unique_values = df[col].unique()
        
        for val in unique_values:
            # Simulate the split: What if user says YES? What if user says NO?
            yes_subset = df[df[col] == val]
            no_subset = df[df[col] != val]
            
            # Calculate Weighted Entropy of this split
            weight_yes = len(yes_subset) / len(df)
            weight_no = len(no_subset) / len(df)
            
            new_entropy = (weight_yes * calculate_entropy(yes_subset)) + \
                          (weight_no * calculate_entropy(no_subset))
            
            info_gain = base_entropy - new_entropy
            
            # We prefer splits that are balanced (close to 0.5/0.5 probability)
            # This logic finds the highest information gain
            if info_gain > best_info_gain:
                best_info_gain = info_gain
                best_question = (col, val)

    return best_question

# Allow running this file directly to fix the map manually
if __name__ == "__main__":
    update_hotspots()