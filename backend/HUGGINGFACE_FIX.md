# Hugging Face API Key Permission Issue - SOLUTION

## Problem
Your API key shows error:
```
403 Forbidden: This authentication method does not have sufficient permissions 
to call Inference Providers on behalf of user Maheshmk.
```

## Solution Steps

### 1. Go to Hugging Face Token Settings
Visit: https://huggingface.co/settings/tokens

### 2. Find Your Token
Look for the token: hf_NYhpzWhHKoPp...

### 3. Update Token Permissions
Click on the token and ensure these permissions are enabled:
- ✅ **"Make calls to serverless Inference API"** (REQUIRED)
- ✅ "Read access to contents of all public gated repos you can access"
- ✅ "Read access to contents of all repos you can access"

### 4. OR Create a New Token
If you can't edit the existing token:
1. Click "New token"
2. Name it: "Enterprise RAG API"
3. Type: Select "Read" or "Write"
4. Enable: "Make calls to serverless Inference API"
5. Click "Generate token"
6. Copy the new token

### 5. Update .env File
Replace the old key with the new one in:
`d:\enterprise-rag\backend\.env`

```
HUGGINGFACE_API_KEY=your_new_token_here
```

### 6. Test Again
Run: `python test_huggingface_key.py`

---

## Alternative: Use Google Gemini (Free)
If you prefer not to deal with Hugging Face permissions, you can use Google Gemini instead:

1. Get a free API key from: https://aistudio.google.com/app/apikey
2. Add to .env:
   ```
   GOOGLE_API_KEY=your_gemini_key_here
   ```
3. The app will automatically use Gemini if HuggingFace is not available

---

## Current Status
- API Key: Found ✓
- Key Format: Valid ✓
- Permissions: Insufficient ✗
- Action Required: Update token permissions or use alternative provider
