#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Starting BOL Management System build..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# Setup database (migrations, superuser, sample data)
echo "🗄️  Setting up database..."
python manage.py setup_db

echo "✅ Build complete!"
