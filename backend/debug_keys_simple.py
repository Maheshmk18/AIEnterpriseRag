import os
from dotenv import load_dotenv
load_dotenv()
print(f"HUGGINGFACE_API_KEY: {'[SET]' if os.getenv('HUGGINGFACE_API_KEY') else '[NOT SET]'}")
print(f"GOOGLE_API_KEY: {'[SET]' if os.getenv('GOOGLE_API_KEY') else '[NOT SET]'}")
print(f"PINECONE_API_KEY: {'[SET]' if os.getenv('PINECONE_API_KEY') else '[NOT SET]'}")
