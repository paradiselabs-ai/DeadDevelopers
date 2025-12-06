from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from users.models import User
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a profile to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj == request.user


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a user profile.
    GET: Anyone can view public profiles
    PUT/PATCH: Only the owner can update their profile
    """
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the currently authenticated user's profile.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_profile_list(request):
    """
    List all public user profiles.
    Optional query parameters:
    - search: Search by username or display name
    - limit: Limit the number of results (default: 20, max: 100)
    """
    queryset = User.objects.filter(is_public=True)
    
    # Search functionality
    search = request.query_params.get('search', None)
    if search:
        queryset = queryset.filter(
            username__icontains=search
        ) | queryset.filter(
            first_name__icontains=search
        ) | queryset.filter(
            last_name__icontains=search
        )
    
    # Limit results
    limit = int(request.query_params.get('limit', 20))
    limit = min(limit, 100)  # Max 100 results
    
    queryset = queryset[:limit]
    
    serializer = UserProfileSerializer(
        queryset,
        many=True,
        context={'request': request}
    )
    
    return Response(serializer.data)
