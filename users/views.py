from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfilePictureForm
from .models import User


def signup_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Initial AI usage at 0%
            user.ai_percentage = 0
            user.save()
            
            # Auto-login after signup
            login(request, user)
            messages.success(request, "Welcome to DeadDevelopers! Let's start building with AI.")
            return redirect('dashboard')
        else:
            # For HTMX/FastHTML integration, return JSON errors
            if request.headers.get('HX-Request'):
                errors = {field: errors[0] for field, errors in form.errors.items()}
                return JsonResponse({'status': 'error', 'errors': errors}, status=400)
    else:
        form = CustomUserCreationForm()
    
    # This view is primarily for API usage, FastHTML handles the UI
    if request.headers.get('HX-Request'):
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_display_name()}!")
            
            # Return success for API/HTMX requests
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'status': 'success',
                    'redirect': '/dashboard',
                    'user': {
                        'name': user.get_display_name(),
                        'email': user.email,
                        'ai_percentage': user.ai_percentage
                    }
                })
            
            return redirect('dashboard')
        else:
            # Return error for API/HTMX requests
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid email or password'
                }, status=400)
            
            messages.error(request, "Invalid email or password")
    
    # This view is primarily for API usage, FastHTML handles the UI
    if request.headers.get('HX-Request'):
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
    return render(request, 'users/login.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, "You've been logged out. Your AI assistant will miss you!")
    
    # Return JSON for API/HTMX requests
    if request.headers.get('HX-Request'):
        return JsonResponse({
            'status': 'success',
            'redirect': '/'
        })
    
    return redirect('home')


@login_required
def profile_view(request):
    """View and edit user profile"""
    user = request.user
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            
            # Return success for API/HTMX requests
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'status': 'success',
                    'user': {
                        'name': user.get_display_name(),
                        'email': user.email,
                        'ai_percentage': user.ai_percentage
                    }
                })
            
            return redirect('profile')
        else:
            # Return error for API/HTMX requests
            if request.headers.get('HX-Request'):
                errors = {field: errors[0] for field, errors in form.errors.items()}
                return JsonResponse({'status': 'error', 'errors': errors}, status=400)
    else:
        form = CustomUserChangeForm(instance=user)
    
    context = {
        'form': form,
        'user': user
    }
    
    # This view is primarily for API usage, FastHTML handles the UI
    if request.headers.get('HX-Request'):
        # Return user data for HTMX/FastHTML integration
        return JsonResponse({
            'user': {
                'name': user.get_display_name(),
                'email': user.email,
                'username': user.username,
                'ai_percentage': user.ai_percentage,
                'bio': user.bio,
                'github_username': user.github_username,
                'twitter_username': user.twitter_username,
                'website': user.website,
                'theme_preference': user.theme_preference,
                'avatar_url': user.avatar.url if user.avatar else None,
                'challenge_count': user.challenge_count,
                'completed_projects': user.completed_projects,
            }
        })
    
    return render(request, 'users/profile.html', context)


@login_required
@require_POST
def update_avatar(request):
    """Update user profile picture (AJAX/HTMX endpoint)"""
    if 'avatar' not in request.FILES:
        return JsonResponse({'status': 'error', 'message': 'No image provided'}, status=400)
    
    form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        user = form.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Profile picture updated',
            'avatar_url': user.avatar.url if user.avatar else None
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid image'}, status=400)


@login_required
@require_POST
def update_ai_percentage(request):
    """Update user's AI usage percentage"""
    try:
        percentage = int(request.POST.get('ai_percentage', 0))
        if 0 <= percentage <= 100:
            user = request.user
            user.ai_percentage = percentage
            user.save()
            return JsonResponse({
                'status': 'success',
                'ai_percentage': percentage
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Percentage must be between 0 and 100'
            }, status=400)
    except ValueError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid percentage value'
        }, status=400)
