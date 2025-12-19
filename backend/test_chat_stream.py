import requests
import json
import sys

def test_stream():
    url = "http://localhost:8000/api/v1/chat/stream"
    
    # First, we need to login to get a token
    auth_url = "http://localhost:8000/api/v1/auth/login"
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    print(f"Logging in as admin...")
    try:
        auth_response = requests.post(auth_url, data=login_data)
        if auth_response.status_code != 200:
            print(f"Login failed: {auth_response.text}")
            return
            
        token = auth_response.json()["access_token"]
        print("Login successful. Token obtained.")
        
    except Exception as e:
        print(f"Connection error during login: {e}")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": "What is the capital of France?",
        "session_id": None
    }
    
    print("\nTesting Stream Endpoint...")
    try:
        with requests.post(url, json=payload, headers=headers, stream=True) as r:
            if r.status_code != 200:
                print(f"Stream request failed: {r.status_code} - {r.text}")
                return
                
            print("Stream started. Receiving chunks:")
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    print(f"Received: {decoded_line}")
                    if decoded_line.startswith("data: "):
                        data = json.loads(decoded_line[6:])
                        if 'content' in data:
                            sys.stdout.write(data['content'])
                            sys.stdout.flush()
    except Exception as e:
        print(f"\nStream Error: {e}")

if __name__ == "__main__":
    test_stream()
