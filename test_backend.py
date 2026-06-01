import requests
import sys
import os

BASE_URL = "http://127.0.0.1:8000"
IMAGE_PATH = "assets/alpha-numeric.jpeg"

def test_backend():
    print(f"Testing /api/detect with image: {IMAGE_PATH}")
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: Image {IMAGE_PATH} not found.")
        sys.exit(1)
        
    with open(IMAGE_PATH, "rb") as f:
        files = {"file": f}
        try:
            response = requests.post(f"{BASE_URL}/api/detect", files=files)
            response.raise_for_status()
            json_response = response.json()
            print("Exact JSON response:")
            print(json_response)
        except Exception as e:
            print(f"Error calling /api/detect: {e}")
            if 'response' in locals():
                print(f"Response text: {response.text}")
            sys.exit(1)

    text_to_speak = json_response.get("text")
    if not text_to_speak:
        print("Error: No text returned in response.")
        sys.exit(1)
        
    print(f"\nTesting /api/tts with text: '{text_to_speak}'")
    try:
        response = requests.get(f"{BASE_URL}/api/tts", params={"text": text_to_speak})
        response.raise_for_status()
        
        output_file = "test_speech.mp3"
        with open(output_file, "wb") as f:
            f.write(response.content)
            
        file_size = os.path.getsize(output_file)
        print(f"Success! MP3 file generated: {output_file} ({file_size} bytes)")
        
    except Exception as e:
        print(f"Error calling /api/tts: {e}")
        if 'response' in locals():
            print(f"Response text: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    test_backend()
