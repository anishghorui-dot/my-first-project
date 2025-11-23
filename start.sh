#!/bin/bash
# Quick Start Script for TIBCO BW XPath Translator

set -e

echo "=================================================="
echo "   TIBCO BW XPath Translator - Quick Start"
echo "=================================================="
echo

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✅ Docker detected - using Docker Compose (recommended)"
    echo
    read -p "Start with Docker? (Y/n): " use_docker
    use_docker=${use_docker:-Y}
    
    if [[ $use_docker =~ ^[Yy]$ ]]; then
        echo
        echo "🚀 Starting application with Docker Compose..."
        docker-compose up --build -d
        
        echo
        echo "⏳ Waiting for services to be ready..."
        sleep 10
        
        echo
        echo "✅ Application is running!"
        echo
        echo "   Frontend: http://localhost:3000"
        echo "   Backend:  http://localhost:5000"
        echo
        echo "To view logs: docker-compose logs -f"
        echo "To stop:      docker-compose down"
        exit 0
    fi
fi

# Manual setup
echo "📦 Setting up manually..."
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi
echo "✅ Python $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js $(node --version)"
echo

# Setup Backend
echo "🔧 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "   Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "   Activating virtual environment..."
source venv/bin/activate

echo "   Installing Python dependencies..."
pip install -q -r requirements.txt

echo "   Starting Flask backend..."
python3 app.py > /tmp/flask.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

cd ..

# Setup Frontend
echo
echo "🎨 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "   Installing Node.js dependencies..."
    npm install --silent
fi

echo "   Starting React frontend..."
npm start > /tmp/react.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

cd ..

# Wait for services
echo
echo "⏳ Waiting for services to start..."
sleep 5

echo
echo "=================================================="
echo "✅ Application is running!"
echo "=================================================="
echo
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:5000"
echo
echo "Backend  PID: $BACKEND_PID (log: /tmp/flask.log)"
echo "Frontend PID: $FRONTEND_PID (log: /tmp/react.log)"
echo
echo "To stop the application:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo
echo "To view logs:"
echo "   tail -f /tmp/flask.log    # Backend"
echo "   tail -f /tmp/react.log    # Frontend"
echo
