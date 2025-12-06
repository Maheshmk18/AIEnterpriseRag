import requests
import time

# Login
print('Logging in...')
login_response = requests.post('http://localhost:8000/api/v1/auth/login', 
    data={'username': 'admin', 'password': 'admin123'})
token = login_response.json()['access_token']
print('OK - Logged in\n')

# Ask a question and measure time
print('Asking: "What is the leave policy?"')
start_time = time.time()

chat_response = requests.post(
    'http://localhost:8000/api/v1/chat/',
    headers={'Authorization': f'Bearer {token}'},
    json={'message': 'What is the leave policy?'},
    timeout=30
)

end_time = time.time()
elapsed = end_time - start_time

if chat_response.status_code == 200:
    result = chat_response.json()
    print(f'\n⏱️  Response Time: {elapsed:.2f} seconds')
    print(f'\n📝 AI Response:\n{result["response"]}')
    print(f'\n📚 Sources: {[s["filename"] for s in result.get("sources", [])]}')
else:
    print(f'ERROR: {chat_response.text}')
