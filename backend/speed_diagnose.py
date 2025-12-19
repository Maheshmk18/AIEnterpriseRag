import time
import os
from dotenv import load_dotenv

print("⏱️  STARTING RAG SPEED TEST...")
start_total = time.time()

# 1. Load Env
t0 = time.time()
load_dotenv()
print(f"✅ Env loaded in {time.time() - t0:.4f}s")

# Check keys
google_key = os.getenv("GOOGLE_API_KEY")
print(f"ℹ️  Google Key present: {bool(google_key)}")

# 2. Test Embeddings (Google)
print("\n🧪 Testing Embedding Generation (Google)...")
try:
    t0 = time.time()
    import google.generativeai as genai
    genai.configure(api_key=google_key)
    result = genai.embed_content(
        model="models/text-embedding-004",
        content="What is the speed of this system?",
        task_type="retrieval_query"
    )
    print(f"✅ Embedding generated in {time.time() - t0:.4f}s")
except Exception as e:
    print(f"❌ Embedding Failed: {e}")

# 3. Test Vector Store (Pinecone)
# Skip for now to isolate LLM, but if RAG is on, this matters.
# Let's assume user is hitting the Chat endpoint which does RAG.

# 4. Test LLM (Gemini)
print("\n🧪 Testing LLM Response (Gemini Flash)...")
try:
    t0 = time.time()
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Reply with just the word 'Fast'.")
    print(f"✅ LLM Response in {time.time() - t0:.4f}s")
    print(f"📝 Output: {response.text.strip()}")
except Exception as e:
    print(f"❌ LLM Failed: {e}")

print(f"\n🏁 Total Diagnostic Time: {time.time() - start_total:.4f}s")
