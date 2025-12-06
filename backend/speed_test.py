import time
import sys
sys.path.insert(0, '.')

from app.services.rag_pipeline import rag_pipeline

print("=" * 60)
print("SPEED TEST - qwen2.5:0.5b vs deepseek-r1:1.5b")
print("=" * 60)

queries = [
    "What is the leave policy?",
    "How do I submit expenses?",
    "What are office hours?"
]

for query in queries:
    print(f"\nQuery: {query}")
    print("-" * 60)
    
    start = time.time()
    result = rag_pipeline.query(query, user_id=1, user_role='employee')
    elapsed = time.time() - start
    
    print(f"Time: {elapsed:.2f}s")
    print(f"Response: {result['response'][:100]}...")
    print(f"Sources: {len(result['sources'])} documents")

print("\n" + "=" * 60)
print("SPEED TEST COMPLETE")
print("=" * 60)
print("\nExpected: 2-4 seconds per query (much faster than before!)")
