# Enterprise RAG Assistant

An enterprise-grade Retrieval-Augmented Generation (RAG) application that enables organizations to upload documents and interact with them through natural language queries.

## Features

- **Document Management**: Upload PDF, DOCX, and TXT files for processing
- **Intelligent Chat**: Ask questions about your documents using natural language
- **User Authentication**: Secure login and registration with JWT tokens
- **Admin Dashboard**: Manage users, view statistics, and monitor the system
- **Vector Search**: Semantic search powered by embeddings and ChromaDB
- **LLM Integration**: GPT-powered responses with source citations

## Tech Stack

### Backend
- FastAPI (Python)
- PostgreSQL (Database)
- ChromaDB (Vector Store)
- OpenAI (Embeddings & LLM)
- SQLAlchemy (ORM)

### Frontend
- React 18
- Vite
- Tailwind CSS
- React Router

## Getting Started

1. Set up environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SESSION_SECRET`: Secret key for JWT tokens

2. Install dependencies:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt

   # Frontend
   cd frontend
   npm install
   ```

3. Run the application:
   ```bash
   # Backend (port 8000)
   cd backend
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

   # Frontend (port 5000)
   cd frontend
   npm run dev
   ```

## API Documentation

Once the backend is running, visit `/docs` for the interactive Swagger documentation.

## Project Structure

```
enterprise-rag/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Configuration, security, dependencies
│   │   ├── database/     # Database models and connection
│   │   ├── rag/          # RAG components (embeddings, vector store, LLM)
│   │   └── services/     # Business logic
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   └── utils/        # Utility functions
│   └── package.json
└── README.md
```
