import io
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import PIL.Image
from PIL import ImageDraw
from gtts import gTTS
import tempfile

from utils import parse_xywh_and_class, convert_to_english

app = FastAPI(title="BrailleVision API")

# Add CORS middleware for Flutter frontend to connect easily
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the YOLO model globally so it's ready for requests
MODEL_PATH = "../weights/yolov8_braille.pt"
try:
    model = YOLO(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.get("/")
def read_root():
    return {"message": "Welcome to BrailleVision API"}

@app.post("/api/detect")
async def detect_braille(file: UploadFile = File(...)):
    if not model:
        return JSONResponse(status_code=500, content={"error": "Model not loaded"})

    # Read image
    contents = await file.read()
    
    # Debug save exact received bytes
    with open("debug_received.jpg", "wb") as f:
        f.write(contents)
        
    image = PIL.Image.open(io.BytesIO(contents)).convert("RGB")
    
    print(f"\n--- UPLOAD VERIFICATION ---")
    print(f"Uploaded byte size: {len(contents)} bytes")
    print(f"Uploaded image dimensions (W, H): {image.size}")
    print(f"Saved exact received image to backend/debug_received.jpg\n")
    
    # Run inference
    CONF = 0.15 # same as demo
    res = model.predict(image, conf=CONF)
    boxes = res[0].boxes
    
    # Forensic bounding box drawing
    debug_img = image.copy()
    draw = ImageDraw.Draw(debug_img)
    
    print("\n--- FORENSIC ANALYSIS: PHYSICAL CAMERA TEST ---")
    print(f"Total cells YOLO thinks exist: {len(boxes)}")
    
    if len(boxes) > 0:
        xyxy = boxes.xyxy.cpu().numpy()
        conf = boxes.conf.cpu().numpy()
        cls = boxes.cls.cpu().numpy()
        
        for i in range(len(boxes)):
            class_name = model.names[int(cls[i])]
            x1, y1, x2, y2 = xyxy[i]
            
            # Draw on image
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            draw.text((x1, y1 - 15), f"{class_name} ({conf[i]:.2f})", fill="red")
            
            print(f"Detection {i+1}:")
            print(f"  Coords: ({x1:.2f}, {y1:.2f}) to ({x2:.2f}, {y2:.2f})")
            print(f"  Confidence: {conf[i]:.2f}")
            print(f"  Class (Binary Pattern): {class_name}")
            print("---")
            
    debug_img.save("physical_test_debug.jpg")
    print("Saved physical_test_debug.jpg with all bounding boxes drawn.")

    # Parse bounding boxes
    list_boxes = parse_xywh_and_class(boxes)
    
    # Translate to English
    result_text = ""
    final_sequence = []
    
    for box_line in list_boxes:
        box_classes = box_line[:, -1]
        class_names = [model.names[int(c)] for c in box_classes]
        final_sequence.extend(class_names)
        result_text += convert_to_english(class_names) + " "
    
    # Clean up spacing
    result_text = result_text.strip()
    
    print(f"Final sorted sequence before decoding: {final_sequence}")
    print(f"Final decoded text: '{result_text}'")
    print("--------------------------------------------------\n")
    
    return {"text": result_text}

@app.get("/api/tts")
async def text_to_speech(text: str):
    print(f"\n--- TTS ENDPOINT CALLED ---")
    print(f"Incoming text: '{text}'")
    
    if not text:
        return JSONResponse(status_code=400, content={"error": "No text provided"})
        
    try:
        tts = gTTS(text=text, lang='en')
        
        # Create a temporary file
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)
        temp_audio.close()
        
        file_size = os.path.getsize(temp_audio.name)
        
        print(f"MP3 file path: {temp_audio.name}")
        print(f"MP3 file size: {file_size} bytes")
        print(f"MP3 file exists: {os.path.exists(temp_audio.name)}")
        print(f"Response type returned: FileResponse (audio/mpeg)")
        print("---------------------------\n")
        
        return FileResponse(
            temp_audio.name, 
            media_type="audio/mpeg", 
            filename="speech.mp3",
            background=None # Normally you'd clean this up in a background task
        )
    except Exception as e:
        import traceback
        print("--- TTS GENERATION EXCEPTION ---")
        traceback.print_exc()
        print("--------------------------------")
        return JSONResponse(status_code=500, content={"error": str(e)})
