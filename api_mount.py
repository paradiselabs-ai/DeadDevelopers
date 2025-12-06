"""
Mount Django API within the FastHTML/Starlette application.
This allows the Django REST API to be accessible through the main app server.
"""
import os
from django.core.asgi import get_asgi_application

# Ensure Django settings are configured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_config.settings')

# Get Django ASGI application
django_app = get_asgi_application()


async def django_api_middleware(scope, receive, send):
    """
    Middleware to route /api/* requests to Django.
    All other requests pass through to FastHTML.
    """
    path = scope.get('path', '')
    
    # Route API requests to Django
    if path.startswith('/api/') or path.startswith('/admin/'):
        await django_app(scope, receive, send)
    else:
        # This will be handled by FastHTML
        # We shouldn't reach here if properly integrated
        pass
