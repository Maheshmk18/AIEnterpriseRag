"""
Direct RAG test to diagnose issues
"""
import sys
sys.path.insert(0, '.')

from app.services.rag_pipeline import rag_pipeline

print("=" * 80)
print("TESTING RAG PIPELINE DIRECTLY")
print("=" * 80)

# Test query
test_query = "What is the annual leave policy?"

print(f"\nQuery: {test_query}")
print("-" * 80)

try:
    result = rag_pipeline.query(
        query=test_query,
        user_id=1,
        chat_history=[],
        user_role="employee"
    )
    
    print(f"\nResponse: {result['response']}")
    print(f"\nSources ({len(result['sources'])} found):")
    for source in result['sources']:
        print(f"  - {source['filename']}")
    
    print("\n" + "=" * 80)
    print("RAG TEST SUCCESSFUL!")
    print("=" * 80)
    
except Exception as e:
    print(f"\nERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 80)
    print("RAG TEST FAILED!")
    print("=" * 80)
