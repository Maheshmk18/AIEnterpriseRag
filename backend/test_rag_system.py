"""
Test RAG system by uploading documents and querying
"""
import requests
import os
import time

# API Configuration
BASE_URL = "http://localhost:8000/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/login"
UPLOAD_URL = f"{BASE_URL}/documents/upload"
CHAT_URL = f"{BASE_URL}/chat/"

# Admin credentials (update if different)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def login():
    """Login and get access token"""
    print("🔐 Logging in as admin...")
    
    # Use form data for OAuth2
    response = requests.post(
        LOGIN_URL,
        data={
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD,
            "grant_type": "password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login successful!")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def upload_documents(token):
    """Upload all test PDFs"""
    headers = {"Authorization": f"Bearer {token}"}
    test_docs_dir = "test_documents"
    
    if not os.path.exists(test_docs_dir):
        print(f"❌ Directory '{test_docs_dir}' not found!")
        return False
    
    pdf_files = [f for f in os.listdir(test_docs_dir) if f.endswith('.pdf')]
    
    print(f"\n📤 Uploading {len(pdf_files)} documents...")
    
    for pdf_file in pdf_files:
        filepath = os.path.join(test_docs_dir, pdf_file)
        
        with open(filepath, 'rb') as f:
            files = {'file': (pdf_file, f, 'application/pdf')}
            
            response = requests.post(
                UPLOAD_URL,
                headers=headers,
                files=files
            )
            
            if response.status_code == 200:
                print(f"  ✅ Uploaded: {pdf_file}")
            else:
                print(f"  ❌ Failed to upload {pdf_file}: {response.text}")
        
        time.sleep(1)  # Small delay between uploads
    
    print("\n⏳ Waiting 5 seconds for document processing...")
    time.sleep(5)
    return True

def test_queries(token):
    """Test RAG with various queries"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test queries for different departments
    test_queries = [
        {
            "query": "What is the annual leave policy?",
            "expected_dept": "HR"
        },
        {
            "query": "How do I submit expense reimbursement?",
            "expected_dept": "Finance"
        },
        {
            "query": "What are the password requirements?",
            "expected_dept": "IT"
        },
        {
            "query": "What is the sales commission structure?",
            "expected_dept": "Sales"
        },
        {
            "query": "What are the remote work policy rules?",
            "expected_dept": "Operations"
        },
        {
            "query": "What are the office hours?",
            "expected_dept": "Admin"
        },
        {
            "query": "What is the code review process?",
            "expected_dept": "Engineering"
        },
        {
            "query": "What are the brand color guidelines?",
            "expected_dept": "Marketing"
        }
    ]
    
    print("\n" + "="*80)
    print("🧪 TESTING RAG SYSTEM")
    print("="*80)
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}/{len(test_queries)}")
        print(f"Question: {test['query']}")
        print(f"Expected source: {test['expected_dept']} department")
        print("-" * 80)
        
        response = requests.post(
            CHAT_URL,
            headers=headers,
            json={"message": test['query']}
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "No response")
            sources = data.get("sources", [])
            
            print(f"✅ Answer: {answer[:200]}...")
            
            if sources:
                print(f"\n📚 Sources ({len(sources)} documents):")
                for source in sources:
                    print(f"  - {source.get('filename', 'Unknown')}")
            else:
                print("⚠️  No sources found - RAG may not be working properly!")
        else:
            print(f"❌ Query failed: {response.text}")
        
        time.sleep(2)  # Delay between queries
    
    print("\n" + "="*80)
    print("✅ RAG TESTING COMPLETE!")
    print("="*80)

def main():
    print("="*80)
    print("🚀 RAG SYSTEM TEST SCRIPT")
    print("="*80)
    
    # Step 1: Login
    token = login()
    if not token:
        return
    
    # Step 2: Upload documents
    if not upload_documents(token):
        return
    
    # Step 3: Test queries
    test_queries(token)
    
    print("\n✨ All tests completed!")
    print("\nIf you see sources in the responses, RAG is working correctly! ✅")
    print("If no sources appear, there may be an issue with document processing. ⚠️")

if __name__ == "__main__":
    main()
