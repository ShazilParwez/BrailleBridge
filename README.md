# BrailleBridge

BrailleBridge is an AI-powered accessibility platform that converts physical Braille into readable English text and spoken audio in real time. The project combines computer vision, machine learning, and text-to-speech technology to help bridge the communication gap between Braille users and non-Braille readers.

## Inspiration

Millions of visually impaired individuals rely on Braille for reading and communication. However, many people around them cannot understand Braille, creating accessibility barriers in everyday life. BrailleBridge was built to make Braille content instantly understandable through AI-powered recognition and speech generation.

## Features

- Real-time Braille recognition using a webcam
- Physical Braille detection from camera captures
- Braille-to-English text conversion
- Text-to-Speech audio playback
- Modern Flutter Web interface
- Upload image support
- Responsive and accessibility-focused design

## Demo Workflow

1. Open Camera
2. Capture Braille Image
3. Analyze Image
4. View English Translation
5. Listen to Audio Output

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
- Ngrok Tunnel (Backend Exposure)

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

## How It Works

### Step 1: Capture
The user captures a photo of physical Braille using the browser camera.

### Step 2: Detection
The image is sent to the FastAPI backend where a custom YOLOv8 model detects Braille cells.

### Step 3: Decoding
Detected Braille patterns are converted into their corresponding English characters.

### Step 4: Translation
The decoded text is displayed in the interface.

### Step 5: Speech Generation
The translated text can be played as audio using the integrated text-to-speech pipeline.

## Challenges Faced

- Real-world Braille recognition is significantly harder than recognizing clean dataset images.
- Physical camera images introduce:
  - Perspective distortion
  - Lighting variations
  - Shadows
  - Blur
  - Uneven spacing
- Flutter Web camera integration required custom HTML5 video handling.
- Managing image capture and browser permissions across devices required extensive debugging.

## Future Improvements

- Multi-line Braille paragraph recognition
- Higher accuracy custom-trained models
- Mobile application support
- Offline inference
- Multiple language support
- Handwritten Braille recognition
- Cloud-based model serving

## Installation

### Clone Repository

```bash
git clone https://github.com/ShazilParwez/BrailleBridge.git
cd BrailleBridge
```

### Backend Setup

```bash
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn main:app --reload
```

### Frontend Setup

```bash
flutter pub get
flutter run -d chrome
```

## Project Status

Hackathon Prototype – Functional MVP

Current strengths:
- Physical Braille recognition
- Real-time camera workflow
- Speech output
- End-to-end accessibility pipeline

## Author

**Shazil Parwez**

GitHub: https://github.com/ShazilParwez
Deployment: https://braillebridge-ten.vercel.app/

---

Built with the goal of making information more accessible through AI.
