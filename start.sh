#!/bin/bash

# Start the Language Identification API

echo "🚀 Starting Language Identification API..."
echo "==============================================="

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "🐳 Docker is available"
    
    # Check if we should build the image
    if [[ "$1" == "--build" ]] || ! docker image inspect langid-api &> /dev/null; then
        echo "🔨 Building Docker image..."
        docker build -t langid-api .
    fi
    
    # Stop existing container if running
    if docker ps -q -f name=langid-api | grep -q .; then
        echo "🛑 Stopping existing container..."
        docker stop langid-api
        docker rm langid-api
    fi
    
    # Start the container
    echo "🚀 Starting container..."
    docker run -d \
        --name langid-api \
        -p 8000:8000 \
        -v "$(pwd)/models:/app/models" \
        langid-api
    
    echo "✅ Container started!"
    echo "📊 Check status: docker logs -f langid-api"
    echo "🩺 Health check: curl http://localhost:8000/health"
    echo "📚 Documentation: http://localhost:8000/docs"
    
elif command -v python3 &> /dev/null; then
    echo "🐍 Using Python directly"
    
    # Check if dependencies are installed
    if ! python3 -c "import fastapi, uvicorn, fasttext" &> /dev/null; then
        echo "📦 Installing dependencies..."
        pip install -r requirements.txt
    fi
    
    # Start the server
    echo "🚀 Starting server..."
    python3 main.py
    
else
    echo "❌ Neither Docker nor Python3 is available"
    echo "Please install Docker or Python3 to run the API"
    exit 1
fi