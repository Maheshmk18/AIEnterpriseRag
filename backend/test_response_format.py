"""
Test improved LLM response formatting
"""
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from app.services.rag_pipeline import rag_pipeline

print("=" * 80)
print("🧪 TESTING IMPROVED LLM RESPONSE FORMATTING")
print("=" * 80)

test_query = "What are the leave policies?"
print(f"\n📝 Query: '{test_query}'")
print("\n" + "-" * 80)

result = rag_pipeline.query(
    query=test_query,
    user_id=1,
    user_role="employee"
)

print("\n✨ FORMATTED RESPONSE:")
print("=" * 80)
print(result['response'])
print("=" * 80)

print(f"\n📚 Sources: {len(result['sources'])} documents")
for i, source in enumerate(result['sources'][:3], 1):
    print(f"  {i}. {source['filename']}")

print("\n" + "=" * 80)
print("🏁 TEST COMPLETE")
print("=" * 80)
