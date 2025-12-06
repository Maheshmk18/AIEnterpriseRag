import requests

login_response = requests.post('http://localhost:8000/api/v1/auth/login', 
    data={'username': 'admin', 'password': 'admin123'})
token = login_response.json()['access_token']

print("Testing casual chat handling:\n")

test_cases = [
    ("What is the leave policy?", "Should give detailed answer"),
    ("okay", "Should give short casual response"),
    ("thanks", "Should say you're welcome"),
    ("hi", "Should greet briefly"),
    ("What are work hours?", "Should give detailed answer"),
    ("got it", "Should give short casual response"),
]

for question, expected in test_cases:
    response = requests.post(
        'http://localhost:8000/api/v1/chat/',
        headers={'Authorization': f'Bearer {token}'},
        json={'message': question},
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        answer = result['response']
        print(f'Q: "{question}"')
        print(f'Expected: {expected}')
        print(f'A: {answer}')
        print(f'Length: {len(answer)} chars\n')
