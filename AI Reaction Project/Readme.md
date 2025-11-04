# AI Reaction App

An interactive AI app that detects your **facial expressions** and **hand gestures** in real time using your webcam — and reacts instantly with matching memes!

Built with **OpenCV**, **MediaPipe**, and **Python**, this project uses computer vision to recognize smiles, eye closures, raised hands, and more.

---

## 🚀 Features
- Detects and reacts to:
  - Smiling
  - Closed eyes
  - Hands up
  - Hands covering face
  - Shush / thinking gesture
  - Idea / excited gesture
- Displays both **live webcam feed** and **reaction meme** side-by-side.

---

## 🛠️ Tech Stack
- **Python**
- **OpenCV**
- **MediaPipe**
- **NumPy**

---

## ⚙️ How to Run
1. **Clone this repository**:
   ```bash
   git clone https://github.com/WalaaAlzahrani/ai-reaction-app.git
   cd ai-reaction-app

2. Create and activate virtual environment:
   ```bash
   python -m venv ml_env
   ml_env\Scripts\activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Add your meme images in the project folder (e.g., smiling.jpg, thinking.jpg, etc.).

5. Run the app:
   ```bash
   python main.py
