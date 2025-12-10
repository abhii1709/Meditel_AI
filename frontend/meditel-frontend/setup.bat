#!/bin/bash
echo "🚀 Setting up Meditel Healthcare System"
echo ""

echo "1. Installing frontend dependencies..."
npm install

echo ""
echo "2. Starting frontend development server..."
echo ""
echo "========================================"
echo "🎯 IMPORTANT: Make sure your backend is running!"
echo "Backend should be running at: http://localhost:8000"
echo ""
echo "To start backend:"
echo "cd /path/to/backend"
echo "uvicorn main:app --reload --port 8000"
echo "========================================"
echo ""
echo "3. Frontend will run at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

npm run dev