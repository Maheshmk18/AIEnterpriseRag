#!/bin/bash

cd enterprise-rag/backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd enterprise-rag/frontend && npm run dev &
FRONTEND_PID=$!

wait $BACKEND_PID $FRONTEND_PID
