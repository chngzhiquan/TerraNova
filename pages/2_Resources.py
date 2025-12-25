import streamlit as st

st.set_page_config(page_title="Field Guide", page_icon="🌿")

# 1. GET SPECIES FROM URL
query_params = st.query_params
target_species = query_params.get("species", None)

st.title("🌿 Singapore Field Guide")

# 2. DATA
species_db = {
    "Asian Glossy Starling": {
        "scientific": "Aplonis panayensis",
        "status": "Native",
        "status_class": "badge-native",
        "key_feature": "Bright red eyes. Look for the metallic green sheen in sunlight.",
        "desc": "A highly social bird that moves in noisy groups.",
        "spotting_tip": "Look up! They love congregating on **fruiting palm trees** or figs. If you hear a loud, sharp whistling noise from a tree, scan the branches for glossy black shapes.",
        "call": "A sharp, metallic, piping whistle.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Asian_Glossy_Starling_%28Aplonis_panayensis%29_-_Flickr_-_Lip_Kee.jpg/640px-Asian_Glossy_Starling_%28Aplonis_panayensis%29_-_Flickr_-_Lip_Kee.jpg"
    },
    "Asian Koel": {
        "scientific": "Eudynamys scolopaceus",
        "status": "Native",
        "status_class": "badge-native",
        "key_feature": "Males are glossy black; Females are brown/spotted.",
        "desc": "A large cuckoo that is a brood parasite (lays eggs in crow nests).",
        "spotting_tip": "Very hard to see! They are shy and hide in **dense foliage** high up in trees. Your best bet is to wait until you hear the loud 'Ko-el' call, then scan the dense leaves where the sound is coming from. They rarely come to the ground.",
        "call": "Loud, escalating 'Ko-el' or 'U-wu' repeated 5-6 times.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Asian_Koel_Male_%28Eudynamys_scolopaceus%29_-_Flickr_-_Lip_Kee.jpg/640px-Asian_Koel_Male_%28Eudynamys_scolopaceus%29_-_Flickr_-_Lip_Kee.jpg"
    },
    "Javan Myna": {
        "scientific": "Acridotheres javanicus",
        "status": "Introduced",
        "status_class": "badge-introduced",
        "key_feature": "Grey-black body with a small crest above the beak.",
        "desc": "Singapore's most common bird. Highly adaptable and bold.",
        "spotting_tip": "Look down. They are almost always **on the ground** or on tables at hawker centres scavenging for food. They hop rather than walk.",
        "call": "Harsh, creaky chattering.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Acridotheres_javanicus_%28Singapore%29.jpg/640px-Acridotheres_javanicus_%28Singapore%29.jpg"
    },
    "Red Junglefowl": {
        "scientific": "Gallus gallus",
        "status": "Native (Endangered)",
        "status_class": "badge-native",
        "key_feature": "White ear patch and grey legs (Distinguishes them from domestic chickens).",
        "desc": "The wild ancestor of the chicken. Males are vibrant gold/red.",
        "spotting_tip": "Visit parks near forest edges (like Sin Ming or Pasir Ris) in the **early morning (7-9 AM)**. Listen for rustling in the leaf litter under bushes. They are ground dwellers but can fly up into trees to sleep at night.",
        "call": "Truncated 'Cock-a-doodle-doo'.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Red_Junglefowl_%28Gallus_gallus%29_-_Flickr_-_Lip_Kee.jpg/640px-Red_Junglefowl_%28Gallus_gallus%29_-_Flickr_-_Lip_Kee.jpg"
    },
    "Common Myna": {
        "scientific": "Acridotheres tristis",
        "status": "Introduced",
        "status_class": "badge-introduced",
        "key_feature": "Brown body + Yellow skin patch BEHIND the eye.",
        "desc": "Once dominant, now pushed out by the Javan Myna.",
        "spotting_tip": "Look for them in **open grass patches** or beach fringes (like East Coast Park). They are usually found in pairs. If you see a myna that looks 'brownish' instead of black, check for the yellow eye patch.",
        "call": "Varied whistling and clicking.",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Common_Myna_%28Acridotheres_tristis%29_-_Flickr_-_Lip_Kee.jpg/640px-Common_Myna_%28Acridotheres_tristis%29_-_Flickr_-_Lip_Kee.jpg"
    }
}

# 3. DISPLAY LOGIC
if target_species and target_species in species_db:
    # --- A. FIELD GUIDE DETAIL VIEW ---
    info = species_db[target_species]
    
    if st.button("⬅️ Back to Library"):
        st.query_params.clear()
        st.rerun()

    st.image(info['img'], use_container_width=True)
    
    st.markdown(f"## {target_species}")
    st.markdown(f"*{info['scientific']}* <span class='{info['status_class']}'>{info['status']}</span>", unsafe_allow_html=True)
    
    st.divider()

    st.info(f"**👁️ ID Key:** {info['key_feature']}")

    with st.container(border=True):
        # ✅ RENAMED TAB 2
        tab1, tab2, tab3 = st.tabs(["📝 Overview", "🕵️ Where to Spot", "🔊 Sound"])
        
        with tab1:
            st.write(info['desc'])
            
        with tab2:
            # ✅ NEW SPOTTING TIPS
            st.write(info['spotting_tip'])
            
        with tab3:
            st.write(f"**Call Description:** {info['call']}")
            st.caption("Audio player would go here.")

else:
    # --- B. GRID VIEW (Library) ---
    if target_species: 
        st.warning(f"No entry found for '{target_species}'. Showing all species.")

    # CSS for 3-column Mobile Grid
    st.markdown("""
        <style>
            [data-testid="column"] {
                width: 33.33% !important;
                flex: 1 1 33.33% !important;
                min-width: 0px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    species_list = list(species_db.keys())
    
    for i in range(0, len(species_list), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(species_list):
                name = species_list[i+j]
                with cols[j]:
                    with st.container(border=True):
                        st.image(species_db[name]['img'], use_container_width=True)
                        if st.button(name, key=f"btn_{name}"):
                            st.query_params["species"] = name
                            st.rerun()