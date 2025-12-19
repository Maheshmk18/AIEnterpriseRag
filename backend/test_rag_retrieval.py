"""
Test script to verify RAG pipeline retrieves from vector database
"""
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from app.services.rag_pipeline import rag_pipeline
from app.rag.vector_store import vector_store

print("=" * 80)
print("🧪 TESTING RAG PIPELINE - VECTOR DATABASE RETRIEVAL")
print("=" * 80)

# Check vector store status
print("\n📊 STEP 1: Checking Vector Store Status")
print("-" * 80)
try:
    doc_count = vector_store.get_document_count()
    print(f"✅ Vector Store Connected")
    print(f"📄 Total documents in vector store: {doc_count}")
    
    if doc_count == 0:
        print("⚠️  WARNING: No documents found in vector store!")
        print("   You need to upload documents first for RAG to work.")
    else:
        print(f"✅ Vector store has {doc_count} document chunks")
except Exception as e:
    print(f"❌ Error checking vector store: {e}")

# Test query
print("\n🔍 STEP 2: Testing Query with Vector Retrieval")
print("-" * 80)

test_query = "What are the leave policies?"
print(f"Query: '{test_query}'")
print()

try:
    result = rag_pipeline.query(
        query=test_query,
        user_id=1,
        user_role="employee"
    )
    
    print("\n📋 RESULTS:")
    print("-" * 80)
    print(f"Response: {result['response'][:200]}...")
    print(f"\n📚 Sources Retrieved: {len(result['sources'])}")
    
    if result['sources']:
        print("\n📄 Source Documents:")
        for i, source in enumerate(result['sources'], 1):
            print(f"  {i}. {source['filename']} (chunk {source['chunk_index']})")
        print("\n✅ SUCCESS: Vector database retrieval is working!")
    else:
        print("\n⚠️  No sources retrieved from vector database")
        print("   This means either:")
        print("   1. No documents uploaded yet")
        print("   2. Query didn't match any documents")
        print("   3. Vector store connection issue")
        
except Exception as e:
    print(f"\n❌ Error during query: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("🏁 TEST COMPLETE")
print("=" * 80)
