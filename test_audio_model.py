import sys
import os
from datetime import datetime
from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer

# --- CONFIGURATION ---
# Use an existing file to test
TEST_FILE = "test_audio.mp3" 

def test_birdnet_ai(file_path):
    print(f"🎧 Loading BirdNET Analyzer...")
    print("(First run will download the ~25MB model automatically)")
    
    try:
        # 1. Load the Analyzer
        # This loads the specialized BirdNET model
        analyzer = Analyzer()

        print(f"🔍 Analyzing file: {file_path}")
        print("   Using Location Filter: Singapore (Lat: 1.35, Lon: 103.8)")
        
        # 2. Create a Recording Object
        # BirdNET needs date + location to filter unlikely birds
        recording = Recording(
            analyzer,
            file_path,
            lat=1.3521,      # Singapore Latitude
            lon=103.8198,    # Singapore Longitude
            date=datetime.now(), # Current date (for seasonal migration checks)
            min_conf=0.3,    # Sensitivity (0.1 = Sensitive, 0.9 = Strict)
        )
        
        # 3. Run Analysis
        recording.analyze()
        
        print("\n" + "="*50)
        print("🦅 BIRDNET PREDICTIONS")
        print("="*50)
        
        # 4. Print Results
        detections = recording.detections
        
        if detections:
            for d in detections:
                name = d['common_name']
                sci_name = d['scientific_name']
                score = d['confidence'] * 100
                
                # Visual Bar
                bar_len = int(score / 2)
                bar = "█" * bar_len
                
                print(f"✅ {name:<20} ({sci_name})")
                print(f"   Confidence: {score:5.1f}% | {bar}")
                print("-" * 50)
        else:
            print("❌ No birds detected above 30% confidence.")
            print("   Try reducing background noise or getting closer.")

    except FileNotFoundError:
        print(f"\n❌ ERROR: Could not find file '{file_path}'")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    # Allow running with specific filename: python test_birdnet.py my_audio.wav
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = TEST_FILE
        
    test_birdnet_ai(target_file)