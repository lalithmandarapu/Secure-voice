# 🔐 SecureVoice - Assistive Communication System with Encryption & Gesture Support

SecureVoice is a web-based assistive communication platform built with **Flask**, designed to help individuals who are unable to speak communicate through voice or hand gestures. It securely processes input using **AES encryption**, and then **decrypts and converts it to speech** output. It also supports **multilingual communication** and **offline usage** with Service Workers.

---

## 🌟 Key Features

- 🎤 **Voice Input** using Web Speech API (no extensions required)
- ✋ **Real-Time Gesture Recognition** via webcam using MediaPipe Hands
- 🔐 **AES Encryption/Decryption** of messages (client-side)
- 🗣️ **Text-to-Speech Output** of decrypted messages
- 🌐 **Multilingual Support** (English, Hindi, Spanish)
- 📴 **Offline Mode** using Service Workers
- 💻 **Clean, Responsive UI** using Bootstrap

---

## 📁 Folder Structure

securevoice/
├── app.py 
├── templates/
│ └── index.html 
├── static/
│ ├── script.js 
│ ├── crypto.js 
│ └── service-worker.js 


---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/securevoice.git
cd securevoice
