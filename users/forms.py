from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration.
    Extends UserCreationForm to include our custom fields.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'})
    )
    
    class Meta:
        model = User
        fields = ('email', 'username', 'name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        
    def save(self, commit=True):
        user = super().save(commit=False)
        name_parts = self.cleaned_data['name'].split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """
    Form for user profile updates.
    Extends UserChangeForm to include our custom fields.
    """
    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name', 'last_name',
            'bio', 'avatar', 'github_username', 'twitter_username',
            'website', 'theme_preference'
        )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add modern styling to the form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'profile-input'})


class ProfilePictureForm(forms.ModelForm):
    """
    Form for updating just the user's profile picture.
    """
    class Meta:
        model = User
        fields = ('avatar',)
