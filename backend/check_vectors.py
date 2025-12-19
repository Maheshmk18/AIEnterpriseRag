from app.rag.vector_store import get_vector_store
from dotenv import load_dotenv
load_dotenv()

vs = get_vector_store()
if vs:
    try:
        count = vs.get_document_count()
        print(f"Total vectors in Pinecone: {count}")
    except Exception as e:
        print(f"Error getting count: {e}")
else:
    print("Failed to initialize vector store")
