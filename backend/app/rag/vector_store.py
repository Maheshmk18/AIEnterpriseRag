import os
import time
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any, Optional

# Constants
INDEX_NAME = "enterprise-rag"
DIMENSION = 768  # Gemini Embedding (embedding-001) Output Dimension

class VectorStore:
    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            print("⚠️ WARNING: PINECONE_API_KEY not found. Vector Store will fail.")
            return

        self.pc = Pinecone(api_key=api_key)
        
        # Check if index exists, create if not
        existing_indexes = [i.name for i in self.pc.list_indexes()]
        
        if INDEX_NAME not in existing_indexes:
            print(f"Creating Pinecone index: {INDEX_NAME}...")
            try:
                self.pc.create_index(
                    name=INDEX_NAME,
                    dimension=DIMENSION,
                    # Start with free serverless (aws/us-east-1 is common free tier region)
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                # Wait for index to be ready
                while not self.pc.describe_index(INDEX_NAME).status['ready']:
                    time.sleep(1)
            except Exception as e:
                print(f"❌ Error creating index: {e}")
        
        self.index = self.pc.Index(INDEX_NAME)

    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        """Upload vectors to Pinecone"""
        # Prepare data in Pinecone format: (id, vector, metadata)
        # Add 'text' to metadata since Pinecone doesn't store separate 'documents'
        vectors = []
        for i, doc_id in enumerate(ids):
            # Ensure metadata doesn't contain nulls
            clean_meta = {k: v for k, v in metadatas[i].items() if v is not None}
            clean_meta['text'] = documents[i]  # Store text content in metadata
            
            vectors.append({
                "id": doc_id,
                "values": embeddings[i],
                "metadata": clean_meta
            })
            
        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)

    def query(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Query Pinecone"""
        try:
            # Pinecone filter format is simply the dict
            results = self.index.query(
                vector=query_embedding,
                top_k=n_results,
                filter=where,
                include_metadata=True
            )
            
            # Reformat to match original ChromaDB interface expected by pipeline
            # Chroma: {"documents": [[text1, text2]], "metadatas": [[meta1, meta2]]}
            
            cleaned_docs = []
            cleaned_metas = []
            
            for match in results['matches']:
                meta = match['metadata']
                text = meta.pop('text', "") # Extract text back out
                cleaned_docs.append(text)
                cleaned_metas.append(meta)
                
            return {
                "documents": [cleaned_docs],
                "metadatas": [cleaned_metas]
            }
            
        except Exception as e:
            print(f"❌ Query Error: {e}")
            return {"documents": [[]], "metadatas": [[]]}

    def delete_by_document_id(self, document_id: int) -> None:
        # Pinecone delete by metadata filter
        try:
            # Note: Delete by metadata is supported in Serverless
            self.index.delete(
                filter={"document_id": document_id}
            )
        except Exception as e:
            print(f"Error deleting: {e}")

    def get_document_count(self) -> int:
        stats = self.index.describe_index_stats()
        return stats['total_vector_count']

vector_store = VectorStore()
