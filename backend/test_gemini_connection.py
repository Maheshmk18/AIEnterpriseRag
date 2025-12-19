import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"🔑 API Key found: {api_key[:20]}..." if api_key else "❌ No API key found")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        print("\n🧪 Testing LLM connection...")
        response = model.generate_content("Say 'Hello, I am working!' if you can read this.")
        print(f"✅ LLM Response: {response.text}")
        
        print("\n🧪 Testing embeddings...")
        result = genai.embed_content(
            model="models/text-embedding-004",
            content="test query",
            task_type="retrieval_query"
        )
        print(f"✅ Embedding generated: {len(result['embedding'])} dimensions")
        
        print("\n✅ All tests passed! Google Gemini API is working correctly.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ Cannot test without API key")
