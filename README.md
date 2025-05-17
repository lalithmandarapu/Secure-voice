# 🛡️ SecureVoice – Assistive Communication System

SecureVoice is a secure and intelligent communication system designed for mute individuals. It supports both **gesture-based** and **voice-based** input to convert user messages into encrypted format and display/decrypt them via a web interface.

---

## 📁 Folder Structure

securevoice/
├── app.py # Flask backend
├── templates/
│ └── index.html # Formal HTML interface
├── static/
│ ├── script.js # JS logic for UI control and API calls
│ ├── crypto.js # AES encryption/decryption frontend logic
│ └── service-worker.js # Enables offline functionality

---

## ✨ Features

- 🔠 Live Gesture Recognition (via webcam + Mediapipe)
- 🎙️ Voice Input Recognition (via Web Speech API)
- 🔐 AES Encryption and Decryption of inputs
- 📢 Optional Text-to-Speech Output
- 🧾 Formal User Interface with input display and status
- 📴 Offline Mode Support via Service Worker

---

## 🔤 Supported Gestures (Demo)

| Hand Sign Style | Letter Detected |
|------------------|------------------|
| ✌️ Index + Middle up | V |
| ☝️ Only Index up     | I |
| ✋ All Fingers up     | O |
| 🤙 L shape (Index + Pinky) | L |
| 👍👍👍👍 4 Fingers up | A |
| ✊ Fist (No fingers up) | T |
| 👍✌️ Thumb + Index | H |

(*You can add more by customizing the `detect_letter_from_landmarks()` function in `app.py`*)

---

## ▶️ How to Run the Project

### 1. Install Python dependencies:

```bash
pip install flask opencv-python mediapipe
