import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
import librosa
import cv2

# -----------------------
# Load model ONCE
# -----------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model.keras")

model = load_model()

# -----------------------
# Streamlit Config
# -----------------------
st.set_page_config(page_title="Fire Detection UI", layout="centered")

st.title("🔥 Multi-Modal Fire Detection")
st.write("Upload **Image, Audio, or Video** to get predictions with confidence score")

st.divider()

# -----------------------
# Upload Inputs
# -----------------------
image_file = st.file_uploader("📷 Upload Image", type=["jpg", "jpeg", "png"])
audio_file = st.file_uploader("🎧 Upload Audio", type=["wav", "mp3"])
video_file = st.file_uploader("🎥 Upload Video", type=["mp4", "avi", "mov"])

st.divider()

# -----------------------
# Prediction Logic
# -----------------------
def show_prediction(pred):
    confidence = float(np.max(pred))
    label = int(np.argmax(pred))

    st.subheader("Prediction")
    st.success(f"Class: **{label}**")
    st.write(f"Confidence: **{confidence*100:.2f}%**")

# -----------------------
# IMAGE
# -----------------------
if image_file:
    image = Image.open(image_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # 🔁 PREPROCESS (edit if needed)
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)
    show_prediction(pred)

# -----------------------
# AUDIO
# -----------------------
elif audio_file:
    st.audio(audio_file)

    # 🔁 PREPROCESS (edit if needed)
    y, sr = librosa.load(audio_file, sr=22050)
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    mel = librosa.power_to_db(mel, ref=np.max)
    mel = np.resize(mel, (128, 128))
    mel = mel / np.max(mel)
    mel = np.expand_dims(mel, axis=(0, -1))

    pred = model.predict(mel)
    show_prediction(pred)

# -----------------------
# VIDEO
# -----------------------
elif video_file:
    st.video(video_file)

    # 🔁 PREPROCESS (first frame only – edit if needed)
    tfile = open("temp.mp4", "wb")
    tfile.write(video_file.read())
    tfile.close()

    cap = cv2.VideoCapture("temp.mp4")
    ret, frame = cap.read()
    cap.release()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (224, 224))
    frame = frame / 255.0
    frame = np.expand_dims(frame, axis=0)

    pred = model.predict(frame)
    show_prediction(pred)
