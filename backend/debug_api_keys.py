import os
from dotenv import load_dotenv

# Load env
load_dotenv()

google_key = os.getenv("GOOGLE_API_KEY")
hf_key = os.getenv("HUGGINGFACE_API_KEY")

print(f"GOOGLE_API_KEY present: {bool(google_key)}")
if google_key:
    print(f"GOOGLE_API_KEY prefix: {google_key[:5]}...")

print(f"HUGGINGFACE_API_KEY present: {bool(hf_key)}")
if hf_key:
    print(f"HUGGINGFACE_API_KEY prefix: {hf_key[:5]}...")

# Test Gemini Connection if available
if google_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=google_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("\nTesting Gemini 2.5 Flash...")
        response = model.generate_content("Say 'Gemini is working' if you can hear me.")
        print(f"Gemini Response: {response.text}")
    except Exception as e:
        print(f"Gemini Test Failed: {e}")

# Test HuggingFace Connection if available
if hf_key and not google_key: # Prioritize checking whatever is set
    try:
        from huggingface_hub import InferenceClient
        client = InferenceClient(api_key=hf_key)
        print("\nTesting HuggingFace...")
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-7B-Instruct",
            messages=[{"role": "user", "content": "Say 'HF is working'."}],
            max_tokens=20
        )
        print(f"HF Response: {completion.choices[0].message.content}")
    except Exception as e:
        print(f"HF Test Failed: {e}")
