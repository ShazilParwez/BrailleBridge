# BrailleBridge

BrailleBridge is an AI-powered accessibility platform that converts physical Braille into readable English text and spoken audio in real time. By combining computer vision, machine learning, and text-to-speech technology, BrailleBridge helps bridge the communication gap between Braille users and non-Braille readers.

---

## Inspiration

Millions of visually impaired individuals rely on Braille for reading and communication. However, many people around them cannot understand Braille, creating accessibility barriers in everyday life.

BrailleBridge was built to make Braille content instantly understandable through AI-powered recognition and speech generation, making information more accessible and inclusive.

---

## Features

- Real-time Braille recognition using a webcam
- Physical Braille detection from camera captures
- Braille-to-English text conversion
- Text-to-Speech (TTS) audio playback
- Modern Flutter Web interface
- Image upload support
- Responsive and accessibility-focused design

---

## Demo Workflow

1. Open Camera
2. Capture Braille Image
3. Analyze Image
4. View English Translation
5. Listen to Audio Output

---

## Tech Stack

### Frontend
- Flutter Web
- Dart
- HTML5 Camera APIs
- Audioplayers

### Backend
- FastAPI
- Python

### AI / Machine Learning
- YOLOv8
- Ultralytics

### Computer Vision
- OpenCV
- Pillow (PIL)

### Deployment
- Vercel (Frontend)
- Ngrok (Backend Exposure)

---

## Project Architecture

```text
Camera/Image Input
        │
        ▼
 Flutter Web Frontend
        │
        ▼
 FastAPI Backend
        │
        ▼
 YOLOv8 Braille Detection
        │
        ▼
 Braille Decoding Logic
        │
        ▼
 English Translation
        │
        ▼
 Text-to-Speech Output
```

---

## How It Works

### Step 1: Capture
The user captures a photo of physical Braille using the browser camera.

### Step 2: Detection
The image is sent to the FastAPI backend, where a YOLOv8-based model detects Braille cells.

### Step 3: Decoding
Detected Braille patterns are converted into their corresponding English characters.

### Step 4: Translation
The decoded text is displayed within the application.

### Step 5: Speech Generation
The translated text can be played as audio using the integrated text-to-speech pipeline.

---

## Challenges Faced

- Real-world Braille recognition is significantly harder than recognizing clean dataset images.
- Physical camera images introduce:
  - Perspective distortion
  - Lighting variations
  - Shadows
  - Blur
  - Uneven spacing
- Flutter Web camera integration required custom HTML5 video handling.
- Managing image capture and browser permissions across devices required extensive debugging and testing.

---

## Future Improvements

- Multi-line Braille paragraph recognition
- Higher accuracy custom-trained models
- Mobile application support
- Offline inference
- Multiple language support
- Handwritten Braille recognition
- Cloud-based model serving

---

## Installation

### Clone Repository

```bash
git clone https://github.com/ShazilParwez/BrailleBridge.git
cd BrailleBridge
```

### Backend Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn main:app --reload
```

### Frontend Setup

```bash
flutter pub get
flutter run -d chrome
```

---

## Live Demo

🌐 **Deployment:** https://braillebridge-ten.vercel.app/

---

## Project Status

### Hackathon Prototype – Functional MVP

Current strengths:

- Physical Braille recognition
- Real-time camera workflow
- Speech output
- End-to-end accessibility pipeline
- Browser-based experience with no installation required

---

## Attribution

This project uses pretrained Braille detection weights derived from the DotNeuralNet ecosystem and the YOLOv8 architecture for Braille cell recognition.

Additional development completed for this project includes:

- Flutter Web frontend development
- Real-time browser camera integration
- FastAPI backend integration
- Braille decoding pipeline
- Text-to-Speech functionality
- UI/UX redesign
- Deployment and testing workflow
- End-to-end accessibility experience

---

## Author

**Shazil Parwez**

GitHub: https://github.com/ShazilParwez

---

Built with the goal of making information more accessible through AI.
