import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Dict, Optional, Generator

# Load environment variables first
load_dotenv()

# Configure API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("✓ Google Gemini API Key loaded")
else:
    print("⚠️ WARNING: GOOGLE_API_KEY not found. LLM will fail.")

class LLMHandler:
    def __init__(self):
        # Use Gemini 2.5 Flash (Fast & Free)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
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
            prompt = f"""You are a helpful and friendly enterprise AI assistant. Answer the user's question based on the provided context.

CONTEXT:
{context_text}

USER QUESTION: {query}

INSTRUCTIONS:
1. Provide a clear, well-structured answer using ONLY the information from the context above.
2. Format your response naturally with proper paragraphs and line breaks for readability.
3. Use numbered lists or bullet points when presenting multiple items, but format them naturally (e.g., "1. Item one" on separate lines).
4. Be conversational and friendly while remaining professional.
5. If the context doesn't contain the answer, politely say "I couldn't find that specific information in the available documents."
6. Start with a brief introduction sentence, then provide the details.
7. End with a helpful closing if appropriate (e.g., contact information if mentioned in context).

Please provide a well-formatted, easy-to-read response:"""
        else:
            prompt = f"""You are a helpful and friendly enterprise AI assistant.

USER QUESTION: {query}

Unfortunately, I couldn't find any relevant documents in the knowledge base to answer your question.

Please provide a helpful response that:
1. Politely acknowledges you don't have specific documents about this topic
2. Suggests the user could upload relevant documents if they have them
3. Recommends contacting HR or IT support for assistance
4. Be warm and professional

Respond naturally:"""

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
