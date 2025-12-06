import os
from typing import List
import ollama

# Use Ollama for embeddings (free, local)
EMBEDDING_MODEL = "nomic-embed-text"


class EmbeddingsGenerator:
    def __init__(self, model: str = EMBEDDING_MODEL):
        self.model = model
        self._ensure_model()
    
    def _ensure_model(self):
        """Ensure the embedding model is available"""
        try:
            # Check if model exists
            models_response = ollama.list()
            if hasattr(models_response, 'models'):
                model_names = [m.model.split(':')[0] for m in models_response.models]
            elif isinstance(models_response, dict) and 'models' in models_response:
                model_names = [m['model'].split(':')[0] if isinstance(m, dict) else m.model.split(':')[0] for m in models_response['models']]
            else:
                model_names = []
            
            if 'nomic-embed-text' not in model_names:
                print(f"Pulling embedding model {self.model}...")
                ollama.pull(self.model)
                print(f"Model {self.model} ready!")
            else:
                print(f"✓ Embedding model {self.model} is ready")
        except Exception as e:
            print(f"Warning: Could not verify embedding model: {e}")
            print("Attempting to use model anyway...")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        embeddings = []
        for text in texts:
            response = ollama.embed(model=self.model, input=text)
            if isinstance(response, dict) and 'embeddings' in response:
                embeddings.append(response['embeddings'][0])
            elif hasattr(response, 'embeddings'):
                embeddings.append(response.embeddings[0])
            else:
                raise ValueError(f"Unexpected response format from ollama.embed: {response}")
        return embeddings
    
    def generate_single_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        response = ollama.embed(model=self.model, input=text)
        if isinstance(response, dict) and 'embeddings' in response:
            return response['embeddings'][0]
        elif hasattr(response, 'embeddings'):
            return response.embeddings[0]
        else:
            raise ValueError(f"Unexpected response format from ollama.embed: {response}")


embeddings_generator = EmbeddingsGenerator()
