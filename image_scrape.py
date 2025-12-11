import os
import requests
from pyinaturalist import get_observations

# --- CONFIGURATION ---
OUTPUT_DIR = r"F:\pokedex app data\bird_images_dataset"
BIRDS = [
    "Red Junglefowl", 
    "Common Myna", 
    "Asian Koel", 
    "Javan Myna",
    "Asian Glossy Starling"
]
MAX_IMAGES = 60 
PLACE_ID = 6734 # Singapore

def download_bird_data(species_name):
    print(f"\n🦅 Searching iNaturalist for: {species_name}...")
    
    # This function behaves exactly like the "Explore" tab
    observations = get_observations(
        taxon_name=species_name,
        place_id=PLACE_ID,
        quality_grade="research",
        photos=True,
        per_page=MAX_IMAGES
    )
    
    results = observations['results']
    print(f"   Found {len(results)} verified observations.")
    
    # Create Folder
    folder_name = species_name.lower().replace(" ", "_")
    save_path = os.path.join(OUTPUT_DIR, folder_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    # Download Images
    count = 0
    for obs in results:
        if count >= MAX_IMAGES: break
        
        if obs['photos']:
            # We grab 'large' to get better AI training data than standard thumbnails
            photo_url = obs['photos'][0]['url'].replace("square", "large")
            obs_id = obs['id']
            
            try:
                img_data = requests.get(photo_url, timeout=10).content
                filename = f"{folder_name}_{obs_id}.jpg"
                file_path = os.path.join(save_path, filename)
                
                with open(file_path, 'wb') as f:
                    f.write(img_data)
                
                count += 1
                if count % 10 == 0:
                    print(f"   Downloaded {count} images...")
                    
            except Exception as e:
                print(f"   Skipped: {e}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for bird in BIRDS:
        download_bird_data(bird)
        
    print("\n✅ Download Complete!")