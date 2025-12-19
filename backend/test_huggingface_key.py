import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

print("=" * 60)
print("HUGGING FACE API KEY TEST")
print("=" * 60)

# Check if key exists
if not HUGGINGFACE_API_KEY:
    print("ERROR: HUGGINGFACE_API_KEY not found in .env file")
    exit(1)

print(f"API Key found: {HUGGINGFACE_API_KEY[:15]}...")
print(f"Key length: {len(HUGGINGFACE_API_KEY)} characters")
print()

# Test the API key with Hugging Face
try:
    print("Testing API key with Hugging Face Inference API...")
    client = InferenceClient(api_key=HUGGINGFACE_API_KEY)
    
    # Try a simple chat completion
    messages = [
        {"role": "user", "content": "Say 'Hello, the API key is working!' in one sentence."}
    ]
    
    print("Sending test request to Qwen 2.5 Coder...")
    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        messages=messages,
        max_tokens=50,
        temperature=0.7
    )
    
    response = completion.choices[0].message.content
    print()
    print("SUCCESS! API Key is working!")
    print(f"Response: {response}")
    print()
    
except Exception as e:
    print()
    print("ERROR: API Key test failed!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print()
    print("Possible reasons:")
    print("   1. Invalid API key")
    print("   2. API key doesn't have access to Inference API")
    print("   3. Rate limit exceeded")
    print("   4. Network connectivity issues")
    print("   5. Model not accessible with this key")
    print()
    print("Check your API key at: https://huggingface.co/settings/tokens")
    print()

print("=" * 60)
