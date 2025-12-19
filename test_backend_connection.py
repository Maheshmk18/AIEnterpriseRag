import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_chat():
    try:
        # First login to get token (assuming user exist)
        # Using common admin credentials found in history or models
        # But wait, I don't know the password. I'll check my check_env output.
        # Actually, I'll just check the DB directly if I can.
        
        # Alternatively, just check if the endpoint is reachable
        response = requests.get(f"http://localhost:8000/")
        print(f"Root status: {response.status_code}, {response.json()}")
        
    except Exception as e:
        print(f"Connection failed: {e}. Is the backend running?")

if __name__ == "__main__":
    test_chat()
