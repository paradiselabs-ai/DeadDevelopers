import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')
django.setup()

# Import Django management commands
from django.core.management import call_command

def run_migrations():
    """Run Django makemigrations and migrate commands"""
    print("Checking for model changes...")
    call_command('makemigrations')
    
    print("\nApplying migrations...")
    call_command('migrate')
    
    print("\nMigrations complete!")

if __name__ == "__main__":
    run_migrations()