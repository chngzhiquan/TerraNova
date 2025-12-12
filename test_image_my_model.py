import sys
from transformers import pipeline
from PIL import Image

# --- CONFIGURATION ---
MODEL_ID = "zhiquanchng/singapore-bird-classifier"

# Default image to test if none provided
DEFAULT_IMAGE = "test_image2.jpg" 

def clean_label(label):
    # Mimics the logic in your app (removes underscores, capitalizes)
    return label.replace("_", " ").title()

def test_custom_ai(image_path):
    print(f"⬇️  Downloading/Loading Model from Hugging Face: {MODEL_ID}...")
    print("   (This might take a moment on the first run)")

    try:
        # 1. Load the Model
        # We don't specify framework="tf" because your custom model is likely PyTorch
        pipe = pipeline("image-classification", model=MODEL_ID)
        
        print(f"📸 Analyzing image: {image_path}")
        try:
            image = Image.open(image_path)
        except Exception as e:
            print(f"❌ ERROR: Could not open image file. {e}")
            return

        # 2. Run Prediction (Top 5)
        predictions = pipe(image, top_k=5)
        
        print("\n" + "="*50)
        print("🦅 CUSTOM MODEL PREDICTIONS")
        print("="*50)
        
        # 3. Print Results
        for i, p in enumerate(predictions, 1):
            raw_label = p['label']
            pretty_name = clean_label(raw_label)
            score = p['score'] * 100
            
            # Visual bar
            bar = "█" * int(score / 2)
            
            print(f"{i}. {pretty_name:<25} {score:5.1f}% | {bar}")
            
        print("="*50)

    except OSError:
        print(f"\n❌ ERROR: Could not find model '{MODEL_ID}' on Hugging Face.")
        print("   - Did you make the repository PUBLIC?")
        print("   - Did you type the username/model-name correctly?")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = DEFAULT_IMAGE
        
    test_custom_ai(target_file)