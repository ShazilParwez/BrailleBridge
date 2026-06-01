import cv2
import numpy as np
from PIL import Image, ImageDraw
from ultralytics import YOLO

# Load model
model = YOLO('../weights/yolov8_braille.pt')

# Load the last received physical test image
image_path = 'debug_received.jpg'
try:
    image = Image.open(image_path).convert("RGB")
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
except Exception as e:
    print(f"Error loading image: {e}")
    exit(1)

print("Running YOLO inference...")
res = model(cv_image)

boxes = res[0].boxes
print(f"\n--- STANDALONE CONFIDENCE AUDIT ---")
print(f"Total cells detected: {len(boxes)}")

if len(boxes) > 0:
    xyxy = boxes.xyxy.cpu().numpy()
    conf = boxes.conf.cpu().numpy()
    cls = boxes.cls.cpu().numpy()
    
    for i in range(len(boxes)):
        class_name = model.names[int(cls[i])]
        x1, y1, x2, y2 = xyxy[i]
        
        # Calculate size
        w = x2 - x1
        h = y2 - y1
        
        print(f"\nDetection {i+1}:")
        print(f"  Class: {class_name}")
        print(f"  Confidence: {conf[i]:.4f}")
        print(f"  Box size (W x H): {w:.2f} x {h:.2f}")
        
        # Save cropped cell
        try:
            cell_img = image.crop((x1, y1, x2, y2))
            cell_img.save(f"debug_cell_{i+1}.jpg")
            print(f"  => Saved debug_cell_{i+1}.jpg")
        except Exception as e:
            print(f"  => Failed to save cropped cell: {e}")

print("\nAudit complete.")
