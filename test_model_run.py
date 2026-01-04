import tensorflow as tf
import os

model_path = './models/audio_forest_69.keras'

print("="*60)
print(f"Checking: {model_path}")
print("="*60)

if not os.path.exists(model_path):
    print("❌ FILE DOES NOT EXIST!")
    exit(1)

# File size
size_mb = os.path.getsize(model_path) / (1024 * 1024)
print(f"File size: {size_mb:.2f} MB")

# File modification time
import datetime
mtime = os.path.getmtime(model_path)
mod_time = datetime.datetime.fromtimestamp(mtime)
print(f"Last modified: {mod_time}")

# Try to load
try:
    model = tf.keras.models.load_model(model_path, compile=False)
    print(f"\n✅ Model loaded")
    print(f"Input shape: {model.input_shape}")
    
    if model.input_shape == (None, 128, 1000, 3):
        print("✅ CORRECT!")
    else:
        print("❌ WRONG! This is an OLD file!")
        print("\nThe file you downloaded is NOT from the latest Kaggle run.")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nThis file is corrupted or has wrong architecture!")

print("="*60)