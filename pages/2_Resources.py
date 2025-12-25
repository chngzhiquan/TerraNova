import streamlit as st

st.set_page_config(page_title="Species Library", page_icon="📖")

# 1. GET THE SPECIES NAME FROM THE LINK
# This looks for ?species=Name in the URL
query_params = st.query_params
target_species = query_params.get("species", None)

st.title("📖 Species Library")

# 2. DICTIONARY OF INFO (In reality, you might load this from a CSV)
species_db = {
    "Black Naped Oriole": {
        "desc": "A bright yellow bird with a distinct black mask. Known for its distinct fluty whistle.",
        "habitat": "Parks, gardens, and mangroves.",
        "diet": "Fruits, nectar, and insects.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Black-naped_Oriole_%28Oriolus_chinensis%29_-_Flickr_-_Lip_Kee.jpg/640px-Black-naped_Oriole_%28Oriolus_chinensis%29_-_Flickr_-_Lip_Kee.jpg"
    },
    "Javan Myna": {
        "desc": "A pervasive greyish-black bird. Highly adaptable and often found in urban centers.",
        "habitat": "Urban areas and open country.",
        "diet": "Omnivorous scavengers.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Acridotheres_javanicus_%28Singapore%29.jpg/640px-Acridotheres_javanicus_%28Singapore%29.jpg"
    }
}

# 3. DISPLAY LOGIC
if target_species and target_species in species_db:
    # --- A. SHOW SPECIFIC CARD ---
    info = species_db[target_species]
    
    st.image(info['img'], use_container_width=True)
    st.header(target_species)
    
    with st.container(border=True):
        st.markdown(f"**📝 Description:** {info['desc']}")
        st.markdown(f"**🏡 Habitat:** {info['habitat']}")
        st.markdown(f"**🦗 Diet:** {info['diet']}")
        
    if st.button("⬅️ Back to Library"):
        # Clear the search param to show full list
        st.query_params.clear()
        st.rerun()

else:
    # --- B. SHOW FULL LIST (Default View) ---
    if target_species: 
        st.warning(f"No entry found for '{target_species}'. Showing all species.")

    st.subheader("All Species")
    for name in species_db.keys():
        with st.container(border=True):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write("🐦") # Placeholder icon
            with col2:
                # This button links to THIS same page but adds the parameter
                if st.button(f"View {name}", use_container_width=True):
                    st.query_params["species"] = name
                    st.rerun()