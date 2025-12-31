import streamlit as st
import pandas as pd
import os
import utils

st.set_page_config(page_title="The Game", page_icon="🎮")

st.title("🎮 Guess The Bird")

# --- Load Data ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
csv_path = os.path.join(parent_dir, 'herons.csv')
df = pd.read_csv(csv_path)

# --- Session State Management ---
if 'data' not in st.session_state:
    st.session_state.data = utils.load_data()
    st.session_state.df_remaining = st.session_state.data.copy()
    st.session_state.asked_features = []
    st.session_state.game_over = False
    st.session_state.final_guess = None

def reset_game():
    st.session_state.df_remaining = st.session_state.data.copy()
    st.session_state.asked_features = []
    st.session_state.game_over = False
    st.session_state.final_guess = None

# --- Game Interface ---
if not st.session_state.game_over:
    
    # Check if solved
    if len(st.session_state.df_remaining) == 1:
        st.session_state.final_guess = st.session_state.df_remaining.iloc[0]
        st.session_state.game_over = True
        st.rerun()
    
    # Check if failed
    elif len(st.session_state.df_remaining) == 0:
        st.error("No bird matches that description.")
        if st.button("Try Again"):
            reset_game()
            st.rerun()
        st.stop()

    # Ask Question
    else:
        # Progress Bar (Visual Flair)
        total_birds = len(st.session_state.data)
        current_birds = len(st.session_state.df_remaining)
        confidence = 1.0 - (current_birds / total_birds)
        st.progress(confidence, text=f"Confidence: {int(confidence*100)}%")

        # Get best question from utils
        question = utils.get_best_question(st.session_state.df_remaining, st.session_state.asked_features)

        if question:
            feature, value = question
            display_feature = feature.replace('_', ' ')
            display_value = value.replace('_', ' ')
            
            st.markdown(f"### Does the **{display_feature}** look **{display_value}**?")
            
            c1, c2 = st.columns(2)
            if c1.button("✅ Yes", use_container_width=True):
                st.session_state.df_remaining = st.session_state.df_remaining[
                    st.session_state.df_remaining[feature] == value
                ]
                st.rerun()
                
            if c2.button("❌ No", use_container_width=True):
                st.session_state.df_remaining = st.session_state.df_remaining[
                    st.session_state.df_remaining[feature] != value
                ]
                st.rerun()
        else:
            st.warning("I can't tell the difference between the remaining birds!")
            st.dataframe(st.session_state.df_remaining)
            if st.button("Restart"): reset_game()

# --- Result Screen ---
else:
    bird = st.session_state.final_guess
    st.balloons()
    st.success(f"It's a **{bird['Species']}**!")
    
    # Display Details
    c1, c2 = st.columns(2)
    c1.info(f"**Habitat:** {bird['Habitat_Context']}")
    c2.info(f"**Key Feature:** {bird['Special_Feature']}")
    
    if st.button("Play Again", type="primary"):
        reset_game()
        st.rerun()