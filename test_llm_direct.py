import os
from dotenv import load_dotenv
from pathlib import Path
import sys

sys.path.append(os.path.join(os.getcwd(), 'backend'))

env_path = Path('backend/.env').absolute()
load_dotenv(dotenv_path=env_path)

from app.rag.llm import get_llm_handler

def test_llm():
    handler = get_llm_handler()
    print(f"Provider: {handler.provider}")
    try:
        print("Response: ", end="", flush=True)
        for chunk in handler.generate_response_stream("What is the company mission?", []):
            print(chunk, end="", flush=True)
        print()
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    test_llm()
