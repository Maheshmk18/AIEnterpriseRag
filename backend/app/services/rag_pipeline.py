from typing import List, Dict, Any, Optional, Generator

from ..rag.embeddings import embeddings_generator
from ..rag.vector_store import vector_store
from ..rag.llm import llm_handler


class RAGPipeline:
    def __init__(self):
        self.embeddings = embeddings_generator
        self.vector_store = vector_store
        self.llm = llm_handler
    
    def index_document(
        self,
        document_id: int,
        chunks: List[str],
        filename: str,
        user_id: int
    ) -> int:
        """Index document chunks into the vector store"""
        embeddings = self.embeddings.generate_embeddings(chunks)
        
        ids = [f"doc_{document_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "document_id": document_id,
                "chunk_index": i,
                "filename": filename,
                "user_id": user_id
            }
            for i in range(len(chunks))
        ]
        
        self.vector_store.add_documents(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(chunks)
    
    def query(
        self,
        query: str,
        user_id: Optional[int] = None,
        n_results: int = 5,  # Reduced from 8 to 5 for faster processing
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_role: str = "employee"
    ) -> Dict[str, Any]:
        """Query the knowledge base"""
        context = []
        metadatas = []
        
        try:
            # Generate embedding for query
            query_embedding = self.embeddings.generate_single_embedding(query)
            
            # Query vector store (no filtering, all users see all documents)
            results = self.vector_store.query(
                query_embedding=query_embedding,
                n_results=n_results,
                where=None
            )
            
            context = results.get("documents", [[]])[0] if results.get("documents") else []
            metadatas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []
            
            # Debug logging
            print(f"\n🔍 RAG Query: '{query}'")
            print(f"📄 Retrieved {len(context)} document chunks")
            if context:
                print(f"📌 Top result preview: {context[0][:100]}...")
            else:
                print("⚠️  No documents found in vector store")
            
        except Exception as e:
            print(f"❌ Vector store query error: {str(e)}")
            # Continue with empty context - LLM will provide general response
        
        # Generate response (LLM handles empty context gracefully)
        try:
            response = self.llm.generate_response(
                query=query,
                context=context,
                chat_history=chat_history,
                user_role=user_role
            )
            print(f"✅ Response generated successfully")
        except Exception as e:
            print(f"❌ LLM error: {str(e)}")
            response = "I apologize, but I'm having trouble processing your request. Please try again."
        
        # Build sources list
        sources = []
        seen_docs = set()
        for meta in metadatas:
            doc_key = (meta.get("filename", "Unknown"), meta.get("document_id", 0))
            if doc_key not in seen_docs:
                sources.append({
                    "filename": meta.get("filename", "Unknown"),
                    "chunk_index": meta.get("chunk_index", 0),
                    "document_id": meta.get("document_id", 0)
                })
                seen_docs.add(doc_key)
        
        return {
            "response": response,
            "sources": sources
        }
    
    def query_stream(
        self,
        query: str,
        user_id: Optional[int] = None,
        n_results: int = 5,
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_role: str = "employee"
    ) -> Generator[str, None, None]:
        """Stream query response"""
        context = []
        
        try:
            query_embedding = self.embeddings.generate_single_embedding(query)
            
            # Query all documents (no filtering)
            results = self.vector_store.query(
                query_embedding=query_embedding,
                n_results=n_results,
                where=None
            )
            
            context = results.get("documents", [[]])[0] if results.get("documents") else []
            
        except Exception as e:
            print(f"Vector store stream query error: {str(e)}")
        
        # Stream response
        try:
            for chunk in self.llm.generate_response_stream(
                query=query,
                context=context,
                chat_history=chat_history,
                user_role=user_role
            ):
                yield chunk
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def delete_document(self, document_id: int) -> None:
        """Delete document from vector store"""
        try:
            self.vector_store.delete_by_document_id(document_id)
        except Exception as e:
            print(f"Error deleting document: {e}")


rag_pipeline = RAGPipeline()
