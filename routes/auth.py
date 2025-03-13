from fasthtml.common import *
from dataclasses import dataclass
from app import app, rt, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Q
import re

@dataclass
class SignupForm:
    email: str
    password: str
    name: str
    username: str = None

def signup_form(errors=None):
    """Terminal-styled signup form with the project's aesthetic"""
    return Card(
        A("ESC ← Let me look at more things that would make me want to join", 
            href="/",
            cls="back-link terminal-link",
            style="display: block; margin-bottom: 15px;"
        ),
        H2("Join DeadDevelopers", cls="terminal-header"),
        Form(
            Input(
                type="text",
                name="name",
                placeholder="Your Name",
                required=True,
                cls="signup-input terminal-input"
            ),
            Input(
                type="text",
                name="username",
                placeholder="Username",
                required=True,
                cls="signup-input terminal-input"
            ),
            Input(
                type="email",
                name="email",
                placeholder="Email",
                required=True,
                cls="signup-input terminal-input"
            ),
            Input(
                type="password",
                name="password",
                placeholder="Password",
                required=True,
                cls="signup-input terminal-input"
            ),
            Div(
                errors if errors else "",
                id="signup-errors",
                cls="form-errors terminal-errors"
            ),
            P(
                "By signing up, you acknowledge that you are signing up.",
                cls="signup-disclaimer terminal-text"
            ),
            P(
                "THERE WILL BE NO ESCAPE... ",
                cls="signup-disclaimer terminal-text"
            ),
            P(
                "(unless you delete your account)",
                cls="signup-disclaimer terminal-text"
            ),
            Button(
                "Create Account",
                type="submit",
                cls="signup-submit terminal-button"
            ),
            hx_post="/signup",
            hx_swap="outerHTML",
            cls="signup-form terminal-form"
        ),
        P(
            "Already have an account? ",
            A("Log in", href="/login", cls="terminal-link"),
            cls="signup-link-text terminal-text"
        ),
        cls="signup-card terminal-card"
    )

def error_message(error_text):
    """Format error message with terminal style"""
    return Div(
        P(f"ERROR: {error_text}", cls="error-text"),
        cls="error-message terminal-error"
    )

@rt('/signup')
def get():
    """Render signup form with terminal aesthetics"""
    return signup_form()

@rt('/signup')
def post(form: SignupForm, req):
    """Handle signup form submission and create Django user"""
    # Form validation with terminal-style error messages
    errors = []
    
    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", form.email):
        errors.append(error_message("Invalid email format."))
    
    # Check if email already exists
    if User.objects.filter(email=form.email).exists():
        errors.append(error_message("Email already registered."))
    
    # Generate username from name if not provided
    if not form.username:
        form.username = form.name.lower().replace(" ", "_")
    
    # Check if username is available
    if User.objects.filter(username=form.username).exists():
        errors.append(error_message("Username already taken."))
    
    # Validate password strength
    try:
        validate_password(form.password)
    except ValidationError as e:
        # Format Django's password validation errors
        for error in e.messages:
            errors.append(error_message(error))
    
    # Return form with errors if validation failed
    if errors:
        response = signup_form(errors)
        return response
    
    # Split name into first and last name
    name_parts = form.name.split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    # Create user through Django's auth system
    user = User.objects.create_user(
        username=form.username,
        email=form.email,
        password=form.password,
        first_name=first_name,
        last_name=last_name,
        ai_percentage=0
    )
    
    # Set session data for FastHTML access instead of using Django login
    req.session['auth'] = user.username
    req.session['user'] = {
        'name': user.get_display_name(),
        'email': user.email,
        'ai_percentage': user.ai_percentage
    }
    
    # Add a welcome toast
    add_toast(req.session, f"Welcome aboard, {user.get_display_name()}! Let's write some AI-powered code.", "success")
    
    # Redirect to dashboard
    return RedirectResponse('/dashboard', status_code=303)

def login_form(error=None):
    """Terminal-styled login form"""
    error_content = error_message(error) if error else ""
    
    form = Form(
        Input(
            type="email",
            name="email",
            placeholder="Email",
            required=True,
            cls="login-input terminal-input"
        ),
        Input(
            type="password",
            name="password",
            placeholder="Password",
            required=True,
            cls="login-input terminal-input"
        ),
        # Error container
        Div(
            error_content,
            id="login-errors",
            cls="form-errors terminal-errors"
        ),
        Button(
            "Log In",
            type="submit",
            cls="login-submit terminal-button"
        ),
        hx_post="/login",
        cls="login-form terminal-form"
    )
    
    github_login = A(
        Div(
            Span("Continue with GitHub", cls="oauth-text"),
            cls="oauth-button github"
        ),
        href="/accounts/github/login/",
        cls="oauth-link"
    )
    
    signup_link = P(
        "Don't have an account? ",
        A("Sign up", href="/signup", cls="terminal-link"),
        cls="login-link-text terminal-text"
    )
    
    return Card(
        A("ESC ← Back to Homepage", 
            href="/",
            cls="back-link terminal-link",
            style="display: block; margin-bottom: 15px;"
        ),
        H2("Welcome Back", cls="terminal-header"),
        form,
        Div(
            P("OR", cls="divider-text"),
            cls="divider"
        ),
        github_login,
        signup_link,
        cls="login-card terminal-card"
    )

@rt('/login')
def get():
    """Render login form with terminal aesthetics"""
    return login_form()

@rt('/login')
def post(email: str, password: str, req):
    """Handle login form submission and authenticate Django user"""
    # Attempt to authenticate user
    user = authenticate(username=email, password=password)
    
    # If authentication fails, return login form with error
    if not user:
        return Card(
            A("← Back to home", href="/", cls="back-link terminal-link"),
            H2("Welcome Back", cls="terminal-header"),
            login_form("Invalid email or password"),
            cls="login-card terminal-card"
        )
    
    # Set session data for FastHTML access instead of using Django login
    req.session['auth'] = user.username
    req.session['user'] = {
        'name': user.get_display_name(),
        'email': user.email,
        'ai_percentage': user.ai_percentage
    }
    
    # Add welcome back toast
    add_toast(req.session, f"Welcome back, {user.get_display_name()}!", "success")
    
    # Redirect to dashboard
    return RedirectResponse('/dashboard', status_code=303)

@rt('/logout')
def get(req):
    """Log user out of both Django and FastHTML sessions"""
    # Clear FastHTML session first
    if 'auth' in req.session:
        del req.session['auth']
    if 'user' in req.session:
        del req.session['user']
    
    # Clear Django session if available
    try:
        logout(req)
    except Exception:
        # Ignore Django session errors in FastHTML context
        pass
    
    # Add logout toast
    add_toast(req.session, "You've been logged out successfully.", "info")
    
    # Redirect to home page with explicit 303 status code
    return RedirectResponse('/', status_code=303)

@rt('/profile')
def get(req):
    """Display user profile with terminal aesthetics"""
    if not req.user.is_authenticated:
        return RedirectResponse('/login', status_code=303)
    
    user = req.user
    
    # Format GitHub username link
    github_link = ""
    if user.github_username:
        github_link = A(
            f"@{user.github_username}",
            href=f"https://github.com/{user.github_username}",
            target="_blank",
            cls="profile-link terminal-link"
        )
    
    # Format Twitter username link
    twitter_link = ""
    if user.twitter_username:
        twitter_link = A(
            f"@{user.twitter_username}",
            href=f"https://twitter.com/{user.twitter_username}",
            target="_blank",
            cls="profile-link terminal-link"
        )
    
    # Format website link
    website_link = ""
    if user.website:
        website_link = A(
            user.website,
            href=user.website,
            target="_blank",
            cls="profile-link terminal-link"
        )
    
    # AI percentage visualization with terminal/code aesthetic
    ai_meter = Div(
        Div(
            Span(f"{user.ai_percentage}%", cls="percentage-text"),
            cls="percentage-bar",
            style=f"width: {user.ai_percentage}%"
        ),
        cls="ai-percentage-meter"
    )
    
    # Profile card
    profile_card = Card(
        H2(f"// {user.get_display_name()}", cls="terminal-header"),
        Div(
            # Avatar or default code icon
            Div(
                Img(
                    src=user.avatar.url if user.avatar else "/img/code-avatar.svg",
                    cls="profile-avatar"
                ),
                cls="avatar-container"
            ),
            
            # AI Developer Stats
            Div(
                H3("AI Developer Stats", cls="stats-header terminal-subheader"),
                Div(
                    Div(
                        H4("AI Code %", cls="stat-label"),
                        ai_meter,
                        cls="stat-item"
                    ),
                    Div(
                        H4("Challenges Completed", cls="stat-label"),
                        P(str(user.challenge_count), cls="stat-value terminal-text"),
                        cls="stat-item"
                    ),
                    Div(
                        H4("Projects Deployed", cls="stat-label"),
                        P(str(user.completed_projects), cls="stat-value terminal-text"),
                        cls="stat-item"
                    ),
                    cls="stats-grid"
                ),
                cls="profile-stats"
            ),
            
            # Bio section
            Div(
                H3("Bio", cls="terminal-subheader"),
                P(user.bio or "No bio yet. Tell us about your AI development journey.", cls="terminal-text bio-text"),
                cls="profile-bio"
            ),
            
            # Social links section
            Div(
                H3("Connect", cls="terminal-subheader"),
                Div(
                    Div(
                        Span("GitHub: ", cls="social-label terminal-text"),
                        github_link or Span("Not connected", cls="not-connected terminal-text"),
                        cls="social-item"
                    ),
                    Div(
                        Span("Twitter: ", cls="social-label terminal-text"),
                        twitter_link or Span("Not connected", cls="not-connected terminal-text"),
                        cls="social-item"
                    ),
                    Div(
                        Span("Website: ", cls="social-label terminal-text"),
                        website_link or Span("Not provided", cls="not-connected terminal-text"),
                        cls="social-item"
                    ),
                    cls="social-links"
                ),
                cls="profile-social"
            ),
            
            # Edit profile button
            Button(
                "Edit Profile",
                hx_get="/profile/edit",
                hx_target="#profile-container",
                cls="edit-profile-btn terminal-button"
            ),
            id="profile-container",
            cls="profile-container"
        ),
        cls="profile-card terminal-card"
    )
    
    return Titled(
        f"{user.get_display_name()} | Profile",
        profile_card
    )

@rt('/profile/edit')
def get(req):
    """Display profile edit form with terminal aesthetics"""
    if not req.user.is_authenticated:
        return RedirectResponse('/login', status_code=303)
    
    user = req.user
    
    # Profile edit form
    edit_form = Form(
        # Personal info section
        Div(
            H3("Personal Info", cls="form-section-header terminal-subheader"),
            
            Label("Name", cls="terminal-label"),
            Input(
                type="text",
                name="first_name",
                value=user.first_name,
                placeholder="First Name",
                cls="profile-input terminal-input"
            ),
            Input(
                type="text",
                name="last_name",
                value=user.last_name,
                placeholder="Last Name",
                cls="profile-input terminal-input"
            ),
            
            Label("Username", cls="terminal-label"),
            Input(
                type="text",
                name="username",
                value=user.username,
                placeholder="Username",
                cls="profile-input terminal-input"
            ),
            
            Label("Email", cls="terminal-label"),
            Input(
                type="email",
                name="email",
                value=user.email,
                placeholder="Email",
                cls="profile-input terminal-input"
            ),
            
            Label("Bio", cls="terminal-label"),
            Textarea(
                name="bio",
                placeholder="Tell us about your AI development journey",
                cls="profile-input bio-input terminal-input",
                rows=4
            ),
            user.bio or "",
            
            cls="form-section"
        ),
        
        # Social links section
        Div(
            H3("Social Links", cls="form-section-header terminal-subheader"),
            
            Label("GitHub Username", cls="terminal-label"),
            Input(
                type="text",
                name="github_username",
                value=user.github_username,
                placeholder="GitHub Username",
                cls="profile-input terminal-input"
            ),
            
            Label("Twitter Username", cls="terminal-label"),
            Input(
                type="text",
                name="twitter_username",
                value=user.twitter_username,
                placeholder="Twitter Username",
                cls="profile-input terminal-input"
            ),
            
            Label("Website", cls="terminal-label"),
            Input(
                type="url",
                name="website",
                value=user.website,
                placeholder="https://yourwebsite.com",
                cls="profile-input terminal-input"
            ),
            
            cls="form-section"
        ),
        
        # Preferences section
        Div(
            H3("Preferences", cls="form-section-header terminal-subheader"),
            
            Label("Theme", cls="terminal-label"),
            Select(
                Option("Dark", value="dark", selected=user.theme_preference == "dark"),
                Option("Light", value="light", selected=user.theme_preference == "light"),
                name="theme_preference",
                cls="profile-input terminal-select"
            ),
            
            cls="form-section"
        ),
        
        Div(
            id="profile-errors",
            cls="form-errors terminal-errors"
        ),
        
        Div(
            Button(
                "Save Changes",
                type="submit",
                cls="save-profile-btn terminal-button"
            ),
            Button(
                "Cancel",
                hx_get="/profile",
                hx_target="#profile-container",
                cls="cancel-btn terminal-button secondary"
            ),
            cls="form-buttons"
        ),
        
        hx_post="/profile/update",
        hx_target="#profile-container",
        cls="profile-edit-form terminal-form"
    )
    
    return edit_form

@rt('/profile/update')
def post(req, username: str, email: str, first_name: str, last_name: str, 
         bio: str = "", github_username: str = "", twitter_username: str = "", 
         website: str = "", theme_preference: str = "dark"):
    """Update user profile in Django"""
    if not req.user.is_authenticated:
        return RedirectResponse('/login', status_code=303)
    
    user = req.user
    errors = []
    
    # Validate username change
    if username != user.username and User.objects.filter(username=username).exists():
        errors.append(error_message("Username already taken."))
    
    # Validate email change
    if email != user.email and User.objects.filter(email=email).exists():
        errors.append(error_message("Email already registered."))
    
    # Return form with errors if validation failed
    if errors:
        # Get the edit form and insert errors
        response = get(req)
        response.find("#profile-errors").content = errors
        return response
    
    # Update user fields
    user.username = username
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.bio = bio
    user.github_username = github_username
    user.twitter_username = twitter_username
    user.website = website
    user.theme_preference = theme_preference
    user.save()
    
    # Update session data
    req.session['auth'] = user.username
    req.session['user'] = {
        'name': user.get_display_name(),
        'email': user.email,
        'ai_percentage': user.ai_percentage
    }
    
    # Add success message
    add_toast(req.session, "Profile updated successfully!", "success")
    
    # Redirect to profile view
    return get(req)
