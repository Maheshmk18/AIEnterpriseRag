
import time
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.rag_pipeline import rag_pipeline
from app.rag.llm import get_llm_handler

def diagnose_speed():
    print("🚀 Starting Pipeline Speed Diagnosis...")
    
    query = "What is the company policy on remote work?"
    
    # Measure Total
    t_start = time.time()
    
    # 1. Embedding
    print("\n1. Generating Query Embedding...")
    t0 = time.time()
    embedding = rag_pipeline.embeddings.generate_single_embedding(query)
    t_embed = time.time() - t0
    print(f"   ⏱️  Time: {t_embed:.4f}s")
    
    # 2. Vector Search
    print("\n2. Vector Store Query (Pinecone)...")
    t0 = time.time()
    results = rag_pipeline.vector_store.query(embedding, n_results=5)
    t_vector = time.time() - t0
    print(f"   ⏱️  Time: {t_vector:.4f}s")
    print(f"   📄 Docs Found: {len(results.get('documents', [[]])[0])}")
    
    # 3. LLM Generation
    print("\n3. LLM Generation (Gemini 2.5 Flash)...")
    context = results.get('documents', [[]])[0] if results.get('documents') else []
    t0 = time.time()
    llm = get_llm_handler()
    response = llm.generate_response(query, context)
    t_llm = time.time() - t0
    print(f"   ⏱️  Time: {t_llm:.4f}s")
    
    t_total = time.time() - t_start
    print("="*30)
    print(f"🏁 Total Pipeline Time: {t_total:.4f}s")
    print("\nBreakdown:")
    print(f"  - Embedding: {t_embed/t_total*100:.1f}%")
    print(f"  - Vector DB: {t_vector/t_total*100:.1f}%")
    print(f"  - LLM Gen  : {t_llm/t_total*100:.1f}%")

if __name__ == "__main__":
    try:
        diagnose_speed()
    except Exception as e:
        print(f"Error: {e}")
