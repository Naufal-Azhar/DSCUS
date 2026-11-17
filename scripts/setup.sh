#!/bin/bash
set -e

echo "🚀 Setting up DecisionMirror..."

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your actual configuration"
fi

# Build and start services
echo "🐳 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 5

# Run database migrations
echo "📊 Running database migrations..."
docker-compose exec -T api alembic upgrade head

echo "✅ Setup complete!"
echo ""
echo "Services are running:"
echo "  - Frontend: http://localhost:5173"
echo "  - API:      http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "To stop services:    docker-compose down"
echo "To view logs:        docker-compose logs -f"
echo "To restart:          docker-compose restart"
