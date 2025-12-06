import os
import google.generativeai as genai
from typing import List
import time

# Configure API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("⚠️ WARNING: GOOGLE_API_KEY not found. Embeddings will fail.")

class EmbeddingsGenerator:
    def __init__(self):
        self.model = "models/embedding-001"
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Gemini"""
        embeddings = []
        try:
            # Gemini has batch limit, handle safely
            for text in texts:
                # Add small delay to avoid rate limits on free tier
                time.sleep(0.5) 
                
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document",
                    title="Embedded Document"
                )
                embeddings.append(result['embedding'])
            return embeddings
        except Exception as e:
            print(f"❌ Error generating embeddings: {e}")
            return []
    
    def generate_single_embedding(self, text: str) -> List[float]:
        """Generate embedding for query"""
        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"❌ Error generating single embedding: {e}")
            return []

embeddings_generator = EmbeddingsGenerator()
