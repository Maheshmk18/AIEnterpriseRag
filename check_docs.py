import requests

# Login
login_response = requests.post('http://localhost:8000/api/v1/auth/login', 
    data={'username': 'admin', 'password': 'admin123'})
token = login_response.json()['access_token']

# Check documents
docs_response = requests.get(
    'http://localhost:8000/api/v1/documents/',
    headers={'Authorization': f'Bearer {token}'}
)

print('Documents in knowledge base:')
docs = docs_response.json()
for doc in docs:
    print(f'  - {doc["original_filename"]} ({doc["chunk_count"]} chunks, status: {doc["status"]})')

if len(docs) == 0:
    print('  No documents found! Please upload a document first.')
