from app.services.rag_pipeline import rag_pipeline
from dotenv import load_dotenv
load_dotenv()

print("Testing RAG Query directly...")
result = rag_pipeline.query("What is the capital of France?")
print(f"Response: {result['response']}")
print(f"Sources: {result['sources']}")
