import requests
import sys
import traceback

def test_endpoint(url):
    print(f"Testing URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Content Length: len(response.content) = {len(response.content)} bytes")
        
        # Check if it's returning HTML instead of MP3
        if 'text/html' in response.headers.get('Content-Type', ''):
            print(f"\nWARNING: Endpoint returned HTML instead of audio/mpeg!")
            print(f"First 500 characters of response:")
            print(response.text[:500])
        else:
            print("Successfully received non-HTML response.")
            
    except Exception as e:
        print("Request failed!")
        traceback.print_exc()
    print("="*50 + "\n")

if __name__ == "__main__":
    local_url = "http://127.0.0.1:8000/api/tts?text=hello"
    ngrok_url = "https://probably-ravioli-crayfish.ngrok-free.dev/api/tts?text=hello"
    
    test_endpoint(local_url)
    test_endpoint(ngrok_url)
