import os
import sys
import django
import getpass

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')
django.setup()

# Import Django models
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_github_oauth():
    """
    Interactive script to set up GitHub OAuth for testing.
    
    This script will:
    1. Check if a Site exists and create one if needed
    2. Prompt for GitHub OAuth credentials
    3. Create or update the GitHub SocialApp
    """
    print("=== GitHub OAuth Setup for DeadDevelopers ===\n")
    
    # Step 1: Check Site configuration
    try:
        site = Site.objects.get(id=1)
        print(f"Found existing site: {site.domain}")
    except Site.DoesNotExist:
        domain = input("Enter your site domain (default: localhost:8000): ") or "localhost:8000"
        site = Site.objects.create(domain=domain, name=domain)
        print(f"Created new site: {site.domain}")
    
    # Step 2: Get GitHub OAuth credentials
    print("\nTo set up GitHub OAuth, you need to create an OAuth App on GitHub:")
    print("1. Go to https://github.com/settings/developers")
    print("2. Click 'New OAuth App'")
    print("3. Fill in the form:")
    print(f"   - Application name: DeadDevelopers (Development)")
    print(f"   - Homepage URL: http://{site.domain}")
    print(f"   - Authorization callback URL: http://{site.domain}/accounts/github/login/callback/")
    print("4. Click 'Register application'")
    print("5. Copy the Client ID and generate a Client Secret")
    
    client_id = input("\nEnter GitHub Client ID: ")
    client_secret = getpass.getpass("Enter GitHub Client Secret: ")
    
    if not client_id or not client_secret:
        print("Error: Client ID and Client Secret are required.")
        return
    
    # Step 3: Create or update the GitHub SocialApp
    try:
        app = SocialApp.objects.get(provider="github")
        app.client_id = client_id
        app.secret = client_secret
        app.save()
        print("\nUpdated existing GitHub OAuth app.")
    except SocialApp.DoesNotExist:
        app = SocialApp.objects.create(
            provider="github",
            name="GitHub",
            client_id=client_id,
            secret=client_secret
        )
        app.sites.add(site)
        print("\nCreated new GitHub OAuth app.")
    
    print("\nGitHub OAuth setup complete!")
    print("You can now test GitHub OAuth login and signup.")
    print("\nFor development, you can also set these environment variables:")
    print(f"GITHUB_CLIENT_ID={client_id}")
    print("GITHUB_CLIENT_SECRET=<your-secret>")

if __name__ == "__main__":
    setup_github_oauth()