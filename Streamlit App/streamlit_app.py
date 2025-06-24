import streamlit as st
import cv2
import numpy as np
from PIL import Image
from transformers import pipeline
import os


# Load the image captioning model
@st.cache_resource
def load_caption_model():
    return pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")


caption_model = load_caption_model()

# Load Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# ✅ TEST: Print out the model path and whether the file exists
model_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
st.text(f"Using face model at: {model_path}")
st.text(f"File exists: {os.path.exists(model_path)}")

st.set_page_config(page_title="AI Photo App", layout="centered")
st.title("📸 Face Detection + Image Captioning")

st.markdown(
    """
Upload any image and this app will:
- Detect faces in the image
- Generate a caption using a pre-trained AI model
"""
)

uploaded_file = st.file_uploader(
    "Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    # Convert image to OpenCV format
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangles
    for x, y, w, h in faces:
        cv2.rectangle(image_np, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show original and detected image
    st.image(image, caption="🖼️ Original Image", use_column_width=True)
    st.image(
        image_np, caption=f"✅ Detected {len(faces)} Face(s)", use_column_width=True
    )

    # Generate image caption
    with st.spinner("Generating caption..."):
        caption_result = caption_model(image)
        caption_text = caption_result[0]["generated_text"]

    st.success("Caption ready!")
    st.markdown(f"**🧠 AI Caption:** {caption_text}")
