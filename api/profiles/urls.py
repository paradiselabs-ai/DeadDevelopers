from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # List all public profiles
    path('', views.user_profile_list, name='profile-list'),
    
    # Current user's profile
    path('me/', views.CurrentUserProfileView.as_view(), name='profile-me'),
    
    # Specific user profile by username
    path('<str:username>/', views.UserProfileDetailView.as_view(), name='profile-detail'),
]
