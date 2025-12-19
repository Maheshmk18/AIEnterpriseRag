import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Fix path to include backend
sys.path.append(os.path.join(os.getcwd(), 'backend'))

env_path = Path('backend/.env').absolute()
print(f"Loading env from: {env_path}")
load_dotenv(dotenv_path=env_path)

def check_keys():
    keys = [
        "GOOGLE_API_KEY",
        "HUGGINGFACE_API_KEY",
        "PINECONE_API_KEY",
        "DATABASE_URL"
    ]
    
    for key in keys:
        val = os.environ.get(key)
        if val:
            print(f"✅ {key}: Found (starts with {val[:4]}..., length: {len(val)})")
        else:
            print(f"❌ {key}: Not found")

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    check_keys()
