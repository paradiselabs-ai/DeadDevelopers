from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update-ai-percentage/', views.update_ai_percentage, name='update_ai_percentage'),
    path('profile/update-avatar/', views.update_avatar, name='update_avatar'),
]
