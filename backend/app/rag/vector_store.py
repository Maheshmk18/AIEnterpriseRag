import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional

from ..core.config import settings


class VectorStore:
    def __init__(self):
        persist_dir = settings.CHROMA_PERSIST_DIRECTORY
        os.makedirs(persist_dir, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        return results
    
    def delete_by_document_id(self, document_id: int) -> None:
        self.collection.delete(
            where={"document_id": document_id}
        )
    
    def get_document_count(self) -> int:
        return self.collection.count()


vector_store = VectorStore()
