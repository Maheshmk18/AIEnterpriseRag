"""
Quick RAG test to verify everything is working
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Login
print("Logging in...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={
        "username": "admin",
        "password": "admin123",
        "grant_type": "password"
    }
)

if login_response.status_code != 200:
    print(f"Login failed: {login_response.text}")
    exit(1)

token = login_response.json()["access_token"]
print("✓ Login successful\n")

# Test queries
test_queries = [
    "company policy",
    "What is the leave policy?",
    "How do I submit expenses?",
    "What are the password requirements?"
]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print("=" * 80)
print("TESTING RAG SYSTEM")
print("=" * 80)

for query in test_queries:
    print(f"\nQuery: {query}")
    print("-" * 80)
    
    response = requests.post(
        f"{BASE_URL}/chat/",
        headers=headers,
        json={"message": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        answer = data.get("response", "")
        sources = data.get("sources", [])
        
        print(f"Answer: {answer[:150]}...")
        print(f"Sources: {len(sources)} documents")
        
        if sources:
            print("✓ RAG is working - documents retrieved!")
        else:
            print("⚠ Warning: No sources found")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
