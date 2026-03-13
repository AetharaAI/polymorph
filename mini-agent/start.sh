#!/bin/bash

# Start both backend and frontend services

echo "Starting AetherOps Agentic Harness..."

# Start backend
echo "Starting backend on port 8000..."
cd backend
uvicorn main:app --port 8000 &
BACKEND_PID=$!

cd ..

# Start frontend
echo "Starting frontend on port 3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "Services started:"
echo "  Backend: http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

wait
