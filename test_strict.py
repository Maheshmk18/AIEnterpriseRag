import requests
import time

# Login
login_response = requests.post('http://localhost:8000/api/v1/auth/login', 
    data={'username': 'admin', 'password': 'admin123'})
token = login_response.json()['access_token']

print("Testing strict document-only responses:\n")

questions = [
    "What is the leave policy?",
    "What is my name?",  # Should refuse
    "What are the work hours?",
    "Tell me about Bitcoin",  # Should refuse
]

for q in questions:
    print(f"Q: {q}")
    start = time.time()
    
    response = requests.post(
        'http://localhost:8000/api/v1/chat/',
        headers={'Authorization': f'Bearer {token}'},
        json={'message': q},
        timeout=30
    )
    
    elapsed = time.time() - start
    
    if response.status_code == 200:
        result = response.json()
        print(f"A: {result['response']}")
        print(f"Time: {elapsed:.1f}s\n")
    else:
        print(f"Error: {response.status_code}\n")
