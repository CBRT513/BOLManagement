from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Set up the database with migrations and initial data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up database...')
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS('✅ Database connection successful'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database connection failed: {e}'))
            return
        
        # Run migrations
        try:
            self.stdout.write('Running migrations...')
            call_command('migrate', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Migrations completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Migrations failed: {e}'))
            return
        
        # Create superuser if it doesn't exist
        try:
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@localhost', 'admin123')
                self.stdout.write(self.style.SUCCESS('✅ Superuser created'))
            else:
                self.stdout.write(self.style.WARNING('ℹ️  Superuser already exists'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Superuser creation failed: {e}'))
        
        # Load sample data
        try:
            call_command('create_sample_data')
            self.stdout.write(self.style.SUCCESS('✅ Sample data loaded'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Sample data loading failed: {e}'))
        
        self.stdout.write(self.style.SUCCESS('✅ Database setup complete!'))