import os
from dotenv import load_dotenv
from typing import List
import time

# Load environment variables first
load_dotenv()

# Configure API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class EmbeddingsGenerator:
    def __init__(self):
        self.model = "models/text-embedding-004"
        self._genai = None
        self._cache = {}  # Simple embedding cache

    @property
    def genai(self):
        if self._genai is None:
            import google.generativeai as genai
            if GOOGLE_API_KEY:
                genai.configure(api_key=GOOGLE_API_KEY)
            else:
                print("⚠️ WARNING: GOOGLE_API_KEY not found. Embeddings will fail.")
            self._genai = genai
        return self._genai
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Gemini"""
        embeddings = []
        try:
            # Gemini has batch limit, handle safely
            for text in texts:
                # Use cache if available
                if text in self._cache:
                    embeddings.append(self._cache[text])
                    continue

                # Add small delay to avoid rate limits on free tier
                time.sleep(0.5) 
                
                result = self.genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document",
                    title="Embedded Document"
                )
                self._cache[text] = result['embedding']
                embeddings.append(result['embedding'])
            return embeddings
        except Exception as e:
            print(f"❌ Error generating embeddings: {e}")
            return []
    
    def generate_single_embedding(self, text: str) -> List[float]:
        """Generate embedding for query"""
        # Return from cache if we've seen this query before
        if text in self._cache:
            return self._cache[text]

        try:
            result = self.genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_query"
            )
            self._cache[text] = result['embedding']
            return result['embedding']
        except Exception as e:
            print(f"❌ Error generating single embedding: {e}")
            return []

_embeddings_instance = None

def get_embeddings_generator():
    """Get or create the EmbeddingsGenerator instance (lazy initialization)"""
    global _embeddings_instance
    if _embeddings_instance is None:
        _embeddings_instance = EmbeddingsGenerator()
    return _embeddings_instance

# For backward compatibility
embeddings_generator = None  # Will be initialized on first use

