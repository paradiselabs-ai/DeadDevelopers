import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')
django.setup()

# Import Django management commands
from django.core.management import call_command

def run_tests():
    """Run Django tests for the authentication system"""
    print("Running authentication tests...")
    call_command('test', 'tests.test_auth_extended')
    
    print("\nTests complete!")

if __name__ == "__main__":
    run_tests()