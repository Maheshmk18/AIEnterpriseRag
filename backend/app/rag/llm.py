import os
from typing import List, Dict, Optional, Generator
from openai import OpenAI

# OpenAI API Key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Print API key status on startup
if OPENAI_API_KEY:
    print(f"✓ OpenAI API Key loaded (starts {OPENAI_API_KEY[:20]}...)")
else:
    print("⚠ No OpenAI API Key found - will use Ollama fallback")


class LLMHandler:
    def __init__(self):
        self.client = None
        if OPENAI_API_KEY:
            try:
                self.client = OpenAI(api_key=OPENAI_API_KEY)
            except Exception as e:
                print(f"Failed to initialize OpenAI: {e}")
        self.model = "gpt-3.5-turbo"
    
    def _is_casual_chat(self, query: str) -> bool:
        """Detect casual chat - only exact matches"""
        casual_words = ['okay', 'ok', 'thanks', 'thank you', 'bye', 'hello', 'hi', 
                       'hey', 'good', 'great', 'nice', 'cool', 'sure', 'yes', 'no',
                       'alright', 'got it', 'understood', 'fine']
        query_clean = query.lower().strip().strip('.!?')
        # Only match exact casual words, not short queries
        return query_clean in casual_words
    
    def generate_response(
        self,
        query: str,
        context: List[str],
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_role: str = "employee"
    ) -> str:
        """Generate response - works with or without context"""
        
        # Handle casual chat instantly
        if self._is_casual_chat(query):
            responses = {
                'okay': 'Is there anything else I can help you with?',
                'ok': 'Is there anything else I can help you with?',
                'thanks': "You're welcome! Let me know if you need anything else.",
                'thank you': "You're welcome! Let me know if you need anything else.",
                'bye': 'Goodbye! Feel free to return if you have any questions.',
                'hello': 'Hello! How can I help you today?',
                'hi': 'Hi! How can I assist you today?',
                'hey': 'Hello! What can I help you with?',
                'good': 'Great! What would you like to know?',
                'great': 'Wonderful! How can I assist you?',
            }
            return responses.get(query.lower().strip().strip('.!?'), 'How can I help you?')
        
        # Build context from RAG results
        context_text = "\n\n---\n\n".join(context[:5]) if context else ""
        
        # Create system prompt
        if context_text:
            system_prompt = f"""You are an AI assistant for an enterprise knowledge base system. Your role is to provide accurate, helpful answers based on company documents.

RETRIEVED CONTEXT FROM COMPANY DOCUMENTS:
{context_text}

INSTRUCTIONS:
1. Answer the user's question using ONLY the information from the context above
2. If the context contains the answer, provide a clear, detailed response
3. If the context is relevant but incomplete, answer what you can and mention what's missing
4. If the context doesn't contain relevant information, clearly state: "I couldn't find specific information about this in the available documents."
5. Be professional, concise, and helpful
6. Use bullet points or numbered lists when appropriate for clarity
7. If you reference specific information, you can mention it comes from the company documents

Remember: Base your answer strictly on the provided context. Do not make up information."""
        else:
            system_prompt = """You are an AI assistant for an enterprise knowledge base system.

Currently, there are no documents in the knowledge base that match your query, or no documents have been uploaded yet.

Please respond politely and suggest:
1. The user may want to upload relevant documents to the knowledge base
2. They can contact their department manager or HR for this information
3. They can try rephrasing their question

Be helpful and professional."""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add chat history
        if chat_history:
            for msg in chat_history[-4:]:  # Last 4 messages
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": query})
        
        # Try Ollama first (since OpenAI has quota issues)
        try:
            import ollama
            
            # Build prompt for Ollama
            if context_text:
                prompt = f"""You are an AI assistant. Answer the question based on the context below.

CONTEXT:
{context_text}

QUESTION: {query}

Provide a clear, concise answer based only on the context above."""
            else:
                prompt = f"""You are an AI assistant. No relevant documents were found.

QUESTION: {query}

Politely inform the user that no documents were found and suggest they upload relevant documents or contact their department."""
            
            response = ollama.generate(
                model="qwen2.5:0.5b",  # Fast, lightweight model
                prompt=prompt,
                options={
                    "num_predict": 200,  # Reduced from 300 for faster response
                    "temperature": 0.3,   # Lower for more focused answers
                    "top_p": 0.9,
                    "num_ctx": 2048      # Context window
                }
            )
            return response['response'].strip()
            
        except Exception as ollama_error:
            print(f"Ollama error: {ollama_error}")
        
        # Fallback to OpenAI if Ollama fails
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"OpenAI API error: {e}")
                if "insufficient_quota" in str(e):
                    return "I apologize, but the OpenAI API quota has been exceeded. Please add credits to your OpenAI account or use the local Ollama model."
        
        # Final fallback
        return "I apologize, but I'm having trouble processing your request. Please try again or contact support."
    
    def _fallback_response(self, query: str, context: List[str]) -> str:
        """Fallback to Ollama if OpenAI fails"""
        try:
            import ollama
            context_text = "\n".join(context[:3]) if context else "No context available."
            prompt = f"""Based on this context: {context_text}

Answer this question: {query}

Provide a helpful, concise response."""
            
            response = ollama.generate(
                model="qwen2.5:0.5b", 
                prompt=prompt,
                options={"num_predict": 200, "temperature": 0.7}
            )
            return response['response'].strip()
        except Exception as e:
            print(f"Ollama fallback error: {e}")
            return f"I apologize, but I'm having trouble processing your request right now. Please try again or contact your {query} department for assistance."
    
    def generate_response_stream(
        self,
        query: str,
        context: List[str],
        chat_history: Optional[List[Dict[str, str]]] = None,
        user_role: str = "employee"
    ) -> Generator[str, None, None]:
        """Stream response"""
        
        if self._is_casual_chat(query):
            yield "Hello! How can I help you today?"
            return
        
        context_text = "\n\n".join(context[:5]) if context else ""
        
        if context_text:
            system_prompt = f"""You are an AI assistant for an enterprise knowledge base system.

RETRIEVED CONTEXT:
{context_text}

Answer based strictly on the context above. Be clear, concise, and helpful."""
        else:
            system_prompt = """You are an AI assistant for an enterprise knowledge base. 
No documents found matching the query. Suggest uploading relevant documents or contacting the appropriate department."""
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.append({"role": "user", "content": query})
        
        # Try Ollama first
        try:
            import ollama
            
            if context_text:
                prompt = f"""Answer based on context:

{context_text}

Question: {query}"""
            else:
                prompt = f"""No documents found. Question: {query}

Suggest uploading documents."""
            
            response = ollama.generate(
                model="qwen2.5:0.5b",  # Fast model
                prompt=prompt,
                options={
                    "num_predict": 200,
                    "temperature": 0.3,
                    "num_ctx": 2048
                }
            )
            yield response['response'].strip()
            return
            
        except Exception as e:
            print(f"Ollama stream error: {e}")
        
        # Fallback to OpenAI
        if self.client:
            try:
                stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500,
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
                return
            except Exception as e:
                print(f"OpenAI stream error: {e}")
        
        # Final fallback
        yield "Error: Unable to generate response. Please try again."


llm_handler = LLMHandler()
