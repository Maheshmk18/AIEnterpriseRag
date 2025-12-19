import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Fix path to include backend
sys.path.append(os.path.join(os.getcwd(), 'backend'))

env_path = Path('backend/.env').absolute()
load_dotenv(dotenv_path=env_path)

from app.rag.vector_store import get_vector_store

def check_vectors():
    try:
        vs = get_vector_store()
        count = vs.get_document_count()
        print(f"Total vectors in Pinecone: {count}")
    except Exception as e:
        print(f"Error checking vectors: {e}")

if __name__ == "__main__":
    check_vectors()
