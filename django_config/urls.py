from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),  # Django-allauth URLs
    
    # Redirect paths used in tests but handled by FastHTML
    path('', RedirectView.as_view(url='/'), name='home'),
    path('dashboard/', RedirectView.as_view(url='/dashboard'), name='dashboard'),
    
    # Add additional app URLs here when created
    # path('forum/', include('machina.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
