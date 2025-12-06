import requests
import json

# Login
print('1. Logging in...')
login_response = requests.post('http://localhost:8000/api/v1/auth/login', 
    data={'username': 'admin', 'password': 'admin123'})
token = login_response.json()['access_token']
print('   OK - Logged in successfully')

# Upload document
print('2. Uploading document...')
with open('sample_hr_policy.txt', 'rb') as f:
    upload_response = requests.post(
        'http://localhost:8000/api/v1/documents/upload',
        headers={'Authorization': f'Bearer {token}'},
        files={'file': ('sample_hr_policy.txt', f, 'text/plain')}
    )
    
if upload_response.status_code == 200:
    doc = upload_response.json()
    print(f'   OK - Document uploaded: {doc["original_filename"]} ({doc["chunk_count"]} chunks)')
else:
    print(f'   ERROR - Upload failed: {upload_response.text}')

# Ask a question
print('3. Asking question: What is the leave policy?')
chat_response = requests.post(
    'http://localhost:8000/api/v1/chat/',
    headers={'Authorization': f'Bearer {token}'},
    json={'message': 'What is the leave policy?'},
    timeout=120
)

if chat_response.status_code == 200:
    result = chat_response.json()
    print('   OK - Got response!')
    print('\n=== AI RESPONSE ===')
    print(result['response'])
    print('\n=== SOURCES ===')
    for s in result.get('sources', []):
        print(f'  - {s["filename"]}')
else:
    print(f'   ERROR - Chat failed: {chat_response.text}')
