import sys
from transformers import pipeline
from PIL import Image

# --- CONFIGURATION ---
# The specialist model we want to test
MODEL_ID = "dennisjooo/Birds-Classifier-EfficientNetB2"

# Default test image (Change this to a real filename you have!)
DEFAULT_IMAGE = "test_image2.jpg" 

def test_visual_ai(image_path):
    print(f"👁️  Loading Vision Model: {MODEL_ID}...")
    print("   (First run downloads ~400MB)")

    try:
        # 1. Load the AI Pipeline
        # We don't specify framework="tf" here to let it auto-detect the best available engine
        pipe = pipeline("image-classification", model=MODEL_ID)
        
        print(f"📸 Analyzing image: {image_path}")
        
        # 2. Load the Image
        try:
            image = Image.open(image_path)
        except Exception as e:
            print(f"❌ ERROR: Could not open image file. {e}")
            return

        # 3. Run Prediction (Get Top 5)
        predictions = pipe(image, top_k=5)
        
        print("\n" + "="*50)
        print("🦅 VISUAL AI PREDICTIONS")
        print("="*50)
        
        # 4. Print Results
        for i, p in enumerate(predictions, 1):
            label = p['label']
            score = p['score'] * 100
            
            # Visual bar
            bar_len = int(score / 2) 
            bar = "█" * bar_len
            
            print(f"{i}. {label:<30} {score:5.1f}% | {bar}")
            
        print("="*50)
        
        # 5. TEST "SINGAPORE MAPPING" LOGIC
        # See if it catches our specific target keywords
        targets = ["Junglefowl", "Koel", "Myna", "Chicken", "Rooster"]
        
        print(f"\n🎯 Checking against Singapore keywords: {targets}")
        
        found_match = False
        for p in predictions:
            for t in targets:
                if t.lower() in p['label'].lower():
                    print(f"✅ MATCH FOUND: '{p['label']}' (Would map to local species)")
                    found_match = True
        
        if not found_match:
            print("❌ No local keywords detected in top results.")

    except OSError as e:
        print(f"\n❌ ERROR: Model loading failed.\n{e}")
        if "torch" in str(e) or "tensorflow" in str(e):
            print("💡 TIP: This model might require 'torch' or 'tensorflow' to be installed.")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = DEFAULT_IMAGE
        
    test_visual_ai(target_file)