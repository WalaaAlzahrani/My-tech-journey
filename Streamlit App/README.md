# 🧠 AI Photo App – Face Detection & Image Captioning

This is a simple and beginner-friendly AI web app I built using Streamlit.  
It allows users to upload any image and the app will:

- 🔍 Detect human faces in the image using OpenCV
- 🧠 Generate a smart caption using a pre-trained AI model (BLIP from Hugging Face)
- 🖼️ Show both the original and annotated images in a clean web interface

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Programming language |
| **Streamlit** | For building the web interface |
| **OpenCV** | For detecting faces and drawing rectangles |
| **Transformers** | To use the BLIP image captioning model |
| **Pillow + NumPy** | For handling image formats and arrays |

---

## 🤖 Models Used

- **Face Detection:**  
  `Haar Cascade Frontal Face Classifier` from OpenCV  
  File: `haarcascade_frontalface_default.xml`  

- **Image Captioning:**  
  `Salesforce/blip-image-captioning-base` from Hugging Face  
  Used via `transformers.pipeline("image-to-text")`

---

## 🚀 How to Run the App

### 1. Clone the project or download the folder

### 2. (Optional) Create a virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
```

### 3. Install required packages
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app
```bash
streamlit run streamlit_app.py
```

Then open your browser at `http://localhost:8501`

---

## 💡 What I Learned

This was my first time using Streamlit and image captioning models.  
While working on this app, I learned how to:
- Combine multiple Python libraries together
- Troubleshoot face detection issues
- Run an AI model that generates captions from images
- Build and deploy a small, real-world app on my own

I also dealt with some real setup issues on Windows (script execution policies, model loading errors), and now I understand how to debug those better too.

---

## 🧠 Features

- Upload `.jpg`, `.jpeg`, or `.png` image files  
- Detect and count all visible faces  
- Generate an AI caption using BLIP  
- Display both original and processed images  

---

## 📂 Files

| File                           | Description                              |
|--------------------------------|------------------------------------------|
| `streamlit_app.py`             | The app logic and layout                 |
| `haarcascade_frontalface_default.xml` | Face detection model used by OpenCV |
| `requirements.txt`             | Python libraries required                |
| `README.md`                    | You're reading it now 😊                |

---
