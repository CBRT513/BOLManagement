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

# Run database migrations explicitly
echo "🗄️  Running database migrations..."
python manage.py migrate --verbosity=2

# Create superuser if doesn't exist
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@localhost', 'admin123')
    print('✅ Superuser created')
else:
    print('ℹ️  Superuser already exists')
"

# Load sample data
echo "📊 Loading sample data..."
python manage.py create_sample_data || echo "⚠️ Sample data loading failed, continuing..."

echo "✅ Build complete!"
