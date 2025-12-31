import streamlit as st
import pandas as pd
import numpy as np
import io
import os

# --- CSS STYLING ---
def make_map_responsive():
    st.markdown("""
        <style>
            .block-container { padding: 0rem !important; margin: 0px !important; max-width: 100% !important; }
            header[data-testid="stHeader"] { background-color: transparent !important; z-index: 1; }
            footer {visibility: hidden;}
            iframe { width: 100% !important; }
        </style>
    """, unsafe_allow_html=True)

# --- DATABASE MANAGEMENT ---
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

# ---  LOGIN LOGIC ---
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

# --- ENTROPY CALCULATION ---
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