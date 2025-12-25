import streamlit as st

st.set_page_config(page_title="Species Library", page_icon="📖")

# 1. GET SPECIES FROM URL
query_params = st.query_params
target_species = query_params.get("species", None)

st.title("📖 Species Library")

# 2. DATA: Populated with your requested Singaporean birds
species_db = {
    "Asian Glossy Starling": {
        "desc": "A bird with glossy black-green plumage and bright red eyes. Often seen in large, noisy flocks congregating on trees.",
        "habitat": "Urban areas, parks, and gardens.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Asian_Glossy_Starling_%28Aplonis_panayensis%29_-_Flickr_-_Lip_Kee.jpg/640px-Asian_Glossy_Starling_%28Aplonis_panayensis%29_-_Flickr_-_Lip_Kee.jpg",
        "call": "Sharp, metallic whistle"
    },
    "Asian Koel": {
        "desc": "A large cuckoo. Males are glossy black; females are brown with spots. Known for their very loud, escalating call.",
        "habitat": "Woodlands, parks, and residential areas.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Asian_Koel_Male_%28Eudynamys_scolopaceus%29_-_Flickr_-_Lip_Kee.jpg/640px-Asian_Koel_Male_%28Eudynamys_scolopaceus%29_-_Flickr_-_Lip_Kee.jpg",
        "call": "Loud 'Ko-el' repeated"
    },
    "Javan Myna": {
        "desc": "Singapore's most common bird. Greyish-black with a yellow beak and feet. Highly adaptable scavenger.",
        "habitat": "Everywhere (Urban centers to hawker centres).",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Acridotheres_javanicus_%28Singapore%29.jpg/640px-Acridotheres_javanicus_%28Singapore%29.jpg",
        "call": "Harsh, creaky chattering"
    },
    "Red Junglefowl": {
        "desc": "The wild ancestor of the domestic chicken. Males have vibrant gold and red feathers with a white ear patch.",
        "habitat": "Forest edges, parks (e.g., Sin Ming, Pasir Ris).",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Red_Junglefowl_%28Gallus_gallus%29_-_Flickr_-_Lip_Kee.jpg/640px-Red_Junglefowl_%28Gallus_gallus%29_-_Flickr_-_Lip_Kee.jpg",
        "call": "Distinct 'Cock-a-doodle-doo'"
    },
    "Common Myna": {
        "desc": "Brown body with a black head and distinct yellow patch behind the eye. Less common now than the Javan Myna.",
        "habitat": "Open country and urban fringes.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Common_Myna_%28Acridotheres_tristis%29_-_Flickr_-_Lip_Kee.jpg/640px-Common_Myna_%28Acridotheres_tristis%29_-_Flickr_-_Lip_Kee.jpg",
        "call": "Varied whistling and croaking"
    }
}

# 3. DISPLAY LOGIC
if target_species and target_species in species_db:
    # --- A. DETAIL VIEW (Full Info) ---
    info = species_db[target_species]
    
    if st.button("⬅️ Back to Library"):
        st.query_params.clear()
        st.rerun()

    st.image(info['img'], use_container_width=True)
    st.header(target_species)
    
    with st.container(border=True):
        st.markdown(f"**📝 Description:** {info['desc']}")
        st.markdown(f"**🏡 Habitat:** {info['habitat']}")
        st.markdown(f"**🔊 Call:** {info['call']}")

else:
    # --- B. GRID VIEW (3 Columns) ---
    if target_species: 
        st.warning(f"No entry found for '{target_species}'. Showing all species.")

    # Convert keys to list
    species_list = list(species_db.keys())
    
    # Loop through list in steps of 3 (0, 3, 6, 9...)
    for i in range(0, len(species_list), 3):
        cols = st.columns(3) # Create 3 columns
        
        # --- CARD 1 (Left) ---
        name_1 = species_list[i]
        with cols[0]:
            with st.container(border=True):
                st.image(species_db[name_1]['img'], use_container_width=True)
                if st.button(name_1, use_container_width=True, key=f"btn_{name_1}"):
                    st.query_params["species"] = name_1
                    st.rerun()

        # --- CARD 2 (Middle) ---
        if i + 1 < len(species_list):
            name_2 = species_list[i+1]
            with cols[1]:
                with st.container(border=True):
                    st.image(species_db[name_2]['img'], use_container_width=True)
                    if st.button(name_2, use_container_width=True, key=f"btn_{name_2}"):
                        st.query_params["species"] = name_2
                        st.rerun()

        # --- CARD 3 (Right) ---
        if i + 2 < len(species_list):
            name_3 = species_list[i+2]
            with cols[2]:
                with st.container(border=True):
                    st.image(species_db[name_3]['img'], use_container_width=True)
                    if st.button(name_3, use_container_width=True, key=f"btn_{name_3}"):
                        st.query_params["species"] = name_3
                        st.rerun()