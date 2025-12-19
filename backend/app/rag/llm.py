import os
from dotenv import load_dotenv
from typing import List, Dict, Optional, Generator

# Load environment variables first
load_dotenv()

# Configure API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

class LLMHandler:
    def __init__(self):
        self.provider = "none"
        self.client = None
        self.model = None
        self.model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"

        if HUGGINGFACE_API_KEY:
            self.provider = "huggingface"
            from huggingface_hub import InferenceClient
            self.client = InferenceClient(api_key=HUGGINGFACE_API_KEY)
            print(f"✓ Hugging Face API Key loaded. Using {self.model_name}")
        elif GOOGLE_API_KEY:
            self.provider = "gemini"
            import google.generativeai as genai
            genai.configure(api_key=GOOGLE_API_KEY)
            # Use Gemini 1.5 Flash (Fast & Free)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("✓ Google Gemini API Key loaded")
        else:
            print("⚠️ WARNING: No API keys found. LLM will fail.")
    
    def _is_casual_chat(self, query: str) -> bool:
        query_lower = query.lower().strip().strip('.!?')
        
        # Direct matches
        casual_phrases = {
            'okay', 'ok', 'thanks', 'thank you', 'bye', 'hello', 'hi', 
            'hey', 'good', 'great', 'nice', 'cool', 'sure', 'yes', 'no',
            'alright', 'got it', 'understood', 'fine', 'good morning', 
            'good afternoon', 'good evening', 'how are you'
        }
        
        if query_lower in casual_phrases:
            return True
            
        # Starts with greeting but is short
        if any(query_lower.startswith(x) for x in ['hello', 'hi ', 'hey ']) and len(query_lower) < 20:
            return True
            
        return False
    
    def _build_prompt(self, query: str, context: List[str]) -> tuple[str, str]:
        """Build system and user messages for the LLM"""
        context_text = "\n\n---\n\n".join(context[:5]) if context else ""
        
        if context_text:
            system_instruction = """You are a helpful and friendly enterprise AI assistant. Answer the user's question based on the provided context.

INSTRUCTIONS:
1. Answer using ONLY the information from the provided context.
2. Format your response using clear Markdown:
   - Use **bold** for important terms or key points.
   - Use bullet points or numbered lists for steps, features, or lists of items.
   - Use `code blocks` for technical commands or code snippets if present in the context.
   - Use > blockquotes for direct citations or important notes.
3. Structure your answer with paragraphs for readability.
4. Be conversational and friendly, but maintain a professional tone.
5. If the context doesn't contain the answer, politely say "I couldn't find that specific information in the available documents." do not hallucinate."""
            
            user_message = f"CONTEXT:\n{context_text}\n\nUSER QUESTION: {query}"
        else:
            system_instruction = """You are a helpful and friendly enterprise AI assistant.
Unfortunately, I couldn't find any relevant documents in the knowledge base to answer the question.

Please provide a helpful response that:
1. Politely acknowledges you don't have specific documents about this topic.
2. Suggests the user could upload relevant documents if they have them.
3. Recommends contacting HR or IT support for assistance.
4. Maintains a helpful and polite tone."""
            
            user_message = f"USER QUESTION: {query}"
            
        return system_instruction, user_message
    
    def generate_response(
        self,
        query: str,
        context: List[str],
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_role: str = "employee"
    ) -> str:
        """Generate response using the configured provider"""
        
        # Handle casual chat instantly
        if self._is_casual_chat(query):
            return "How can I help you regarding company documents?"
        
        system_instruction, user_message = self._build_prompt(query, context)

        try:
            if self.provider == "huggingface":
                messages = [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_message}
                ]
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    max_tokens=1024,
                    temperature=0.7
                )
                return completion.choices[0].message.content.strip()

            elif self.provider == "gemini":
                # Gemini combines system/user prompt usually, or we can use the legacy prompt construction
                # Using the legacy prompt construction from previous code for stability, adapted slightly
                full_prompt = f"{system_instruction}\n\n{user_message}"
                response = self.model.generate_content(full_prompt)
                return response.text.strip()
            
            else:
                return "Configured AI provider is unavailable."

        except Exception as e:
            print(f"❌ LLM Error ({self.provider}): {e}")
            return "I apologize, but I'm having trouble connecting to the AI service. Please try again later."

    def generate_response_stream(
        self,
        query: str,
        context: List[str],
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_role: str = "employee"
    ) -> Generator[str, None, None]:
        """Stream response"""
        # Handle casual chat instantly
        if self._is_casual_chat(query):
            yield "How can I help you regarding company documents?"
            return

        system_instruction, user_message = self._build_prompt(query, context)

        try:
            # Primary Provider Attempt
            if self.provider == "huggingface":
                yield from self._stream_huggingface(system_instruction, user_message)
            elif self.provider == "gemini":
                yield from self._stream_gemini(system_instruction, user_message)
            else:
                yield "Configured AI provider is unavailable."

        except Exception as e:
            print(f"❌ Primary LLM Error ({self.provider}): {e}")
            
            # Fallback Logic
            fallback_provider = "gemini" if self.provider == "huggingface" else "huggingface"
            print(f"🔄 Attempting fallback to {fallback_provider}...")
            
            try:
                if fallback_provider == "gemini":
                    yield from self._stream_gemini(system_instruction, user_message)
                else:
                    yield from self._stream_huggingface(system_instruction, user_message)
            except Exception as e2:
                error_msg = str(e2)
                print(f"❌ Fallback also failed: {e2}")
                if "429" in error_msg or "quota" in error_msg.lower():
                    yield "I apologize, but I am currently experiencing high traffic (Quota Exceeded). Please try again in a minute."
                elif "401" in error_msg or "authorized" in error_msg.lower():
                    yield "I apologize, but there seems to be an issue with AI security keys."
                else:
                    yield "I apologize, but I'm having trouble connecting to all AI services."

    def _stream_huggingface(self, system_instruction: str, user_message: str):
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_message}
        ]
        stream = self.client.chat.completions.create(
            model=os.getenv("AI_MODEL", "Qwen/Qwen2.5-72B-Instruct"),
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
            stream=True
        )
        for chunk in stream:
            if chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    yield content

    def _stream_gemini(self, system_instruction: str, user_message: str):
        full_prompt = f"{system_instruction}\n\n{user_message}"
        response = self.model.generate_content(full_prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text

llm_handler = None

def get_llm_handler():
    """Get or create the LLM handler instance (lazy initialization)"""
    global llm_handler
    if llm_handler is None:
        llm_handler = LLMHandler()
    return llm_handler
