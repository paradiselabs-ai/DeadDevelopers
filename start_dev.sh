#!/bin/bash

# DeadDevelopers Development Startup Script
# This script helps you start the development server with proper checks

set -e  # Exit on error

echo "🚀 Starting DeadDevelopers Development Server"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before continuing."
    echo "   Minimum required: SECRET_KEY"
    exit 1
fi

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser if needed (optional)
echo ""
read -p "Do you want to create a superuser? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Start the development server
echo ""
echo "✅ All checks passed! Starting server..."
echo "🌐 Server will be available at: http://localhost:8000"
echo ""
python main.py
