import sys
from transformers import pipeline
from PIL import Image

# --- CONFIGURATION ---
# The Generalist Google Model
MODEL_ID = "google/vit-base-patch16-224"
DEFAULT_IMAGE = "test_image2.jpg"

def test_raw_vision(image_path):
    print(f"👁️  Loading Raw Model: {MODEL_ID}...")
    
    try:
        # 1. Load Model
        pipe = pipeline("image-classification", model=MODEL_ID)
        
        print(f"📸 Analyzing image: {image_path}")
        try:
            image = Image.open(image_path)
        except Exception as e:
            print(f"❌ ERROR: Could not open image. {e}")
            return

        # 2. Get Raw Predictions (Top 5)
        predictions = pipe(image, top_k=5)
        
        print("\n" + "="*50)
        print("🤖 RAW AI OUTPUT (No Filters)")
        print("="*50)
        
        # 3. Print exactly what the model sees
        for i, p in enumerate(predictions, 1):
            label = p['label']
            score = p['score'] * 100
            
            # Visual bar
            bar = "█" * int(score / 2)
            
            print(f"{i}. {label:<25} {score:5.1f}% | {bar}")
            
        print("="*50)
        print("💡 TIP: If you see 'cock', 'hen', or 'rooster' here,")
        print("        it confirms that the model recognizes the bird,")
        print("        but uses farm terminology.")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = DEFAULT_IMAGE
        
    test_raw_vision(target_file)