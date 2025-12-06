import os
import google.generativeai as genai
from typing import List, Dict, Optional, Generator

# Configure API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("✓ Google Gemini API Key loaded")
else:
    print("⚠️ WARNING: GOOGLE_API_KEY not found. LLM will fail.")

class LLMHandler:
    def __init__(self):
        # Use Gemini Flash (Fast & Free)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def _is_casual_chat(self, query: str) -> bool:
        casual_words = ['okay', 'ok', 'thanks', 'thank you', 'bye', 'hello', 'hi', 
                       'hey', 'good', 'great', 'nice', 'cool', 'sure', 'yes', 'no',
                       'alright', 'got it', 'understood', 'fine']
        return query.lower().strip().strip('.!?') in casual_words
    
    def generate_response(
        self,
        query: str,
        context: List[str],
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_role: str = "employee"
    ) -> str:
        """Generate response using Gemini"""
        
        # Handle casual chat instantly
        if self._is_casual_chat(query):
            return "How can I help you regarding company documents?"
        
        # Build prompt
        context_text = "\n\n---\n\n".join(context[:5]) if context else ""
        
        if context_text:
            prompt = f"""You are a helpful enterprise assistant. Answer based on the context below.

CONTEXT:
{context_text}

QUESTION: {query}

INSTRUCTIONS:
1. Answer only using the context.
2. Be concise and professional.
3. If the answer is not in the context, say "I couldn't find that information in the documents."
"""
        else:
            prompt = f"""You are a helpful enterprise assistant.

QUESTION: {query}

There are no relevant documents found. Please suggest the user upload documents or contact HR/IT manager."""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Gemini Error: {e}")
            return "I apologize, but I'm having trouble connecting to the AI service. Please try again later."

    def generate_response_stream(
        self,
        query: str,
        context: List[str],
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_role: str = "employee"
    ) -> Generator[str, None, None]:
        """Stream response (Gemini supports streaming too)"""
        
        # Simple non-streaming fallback for now or implementation similar to above
        # For simplicity in this quick migration, calling standard generate
        response = self.generate_response(query, context, chat_history, user_role)
        yield response

llm_handler = LLMHandler()
