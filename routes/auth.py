from fasthtml.common import *
from dataclasses import dataclass
from app import app, rt, User
from auth_bridge import AuthBridge, csrf_input
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# Rate limiting uses django.core.cache directly rather than the
# django-ratelimit @ratelimit decorator, because @ratelimit expects a
# Django HttpRequest object and FastHTML/@rt routes hand us a Starlette
# request — the decorator chain doesn't compose cleanly. Manual cache
# checks keep the per-route logic explicit and FastHTML-compatible.
from django.core.cache import cache
import re
from fasthtml.svg import Svg, ft_svg as tag
# Email confirmation will be handled manually if needed
# from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress
from typing import List

@dataclass
class SignupForm:
    email: str
    password: str
    name: str
    username: str = None

def error_message(error_text: str) -> Div:
    """Format error message with terminal style"""
    return Div(
        P(f"ERROR: {error_text}", cls="error-text"),
        cls="error-message terminal-error"
    )

def signup_form(req, errors: List[Div] = None):
    """Terminal-styled signup form with the project's aesthetic"""
    return Card(
        A("ESC ← Let me look at more things that would make me want to join", 
            href="/",
            cls="back-link terminal-link",
            style="display: block; margin-bottom: 15px;"
        ),
        H2("Join DeadDevelopers", cls="terminal-header"),
        Form(
            csrf_input(req),  # CSRF protection
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
                *errors if errors else [],
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

@rt('/signup')
def get(req):
    """Render signup form with terminal aesthetics"""
    return signup_form(req)

@rt('/signup')
def post(form: SignupForm, req, session):
    """Handle signup form submission and create Django user"""
    # Rate limiting check
    client_ip = req.client.host
    rate_limit_key = f"signup_ratelimit_{client_ip}"
    
    # Check if IP has exceeded rate limit (5 signups per hour)
    signup_count = cache.get(rate_limit_key, 0)
    if signup_count >= 5:
        return signup_form(req, [error_message("Too many signup attempts. Please try again later.")])
    
    # Form validation with terminal-style error messages
    errors: List[Div] = []

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
        return signup_form(req, errors)

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

    # Create EmailAddress record for the user (auto-verified in development)
    email_address, created = EmailAddress.objects.get_or_create(
        user=user,
        email=form.email,
        defaults={'primary': True, 'verified': True}  # Auto-verify in development
    )

    # Send verification email
    # TODO: Re-enable email confirmation when allauth is properly configured
    # send_email_confirmation(req, user)
    
    # Increment rate limit counter
    cache.set(rate_limit_key, signup_count + 1, 3600)  # 1 hour expiry

    # Add a welcome toast
    add_toast(session, f"Welcome, {user.get_display_name()}! Please check your email to verify your account.", "success")

    # Redirect to verification sent page
    return RedirectResponse('/accounts/confirm-email/', status_code=303)

def login_form(req, error: str = None):
    """Styled login form that closely matches the original React implementation"""
    error_content = error_message(error) if error else ""
    
    # Create the form component - structured like the React version
    form = Form(
        csrf_input(req),  # CSRF protection
        Div(
            Label("Email Address", htmlFor="email"),
            Input(
                type="email",
                id="email",
                name="email",
                placeholder="Enter your email",
                required=True,
                cls="signin-input"
            ),
            cls="form-group"
        ),
        Div(
            Label("Password", htmlFor="password"),
            Input(
                type="password",
                id="password",
                name="password",
                placeholder="Enter your password",
                required=True,
                cls="signin-input"
            ),
            A("Forgot Password?", href="#", cls="forgot-password"),
            cls="form-group"
        ),
        Div(
            error_content,
            id="login-errors",
            cls="form-errors"
        ),
        Button(
            "Log In",
            type="submit",
            cls="login-button"
        ),
        hx_post="/login",
        cls="signin-form"
    )
    
    # Create responsive JavaScript to handle mobile/desktop views exactly like React's approach
    responsive_script = Script("""
    function isMobile() {
        return window.innerWidth < 768;
    }
    
    function handleGoogleLogin() {
        console.log("Logging in with Google");
        // Add your Google login logic here
    }
    
    function handleGithubLogin() {
        console.log("Logging in with GitHub");
        // Add your GitHub login logic here
    }
    
    // Initial setup on page load
    document.addEventListener('DOMContentLoaded', function() {
        setupLayout();
        // Re-check on window resize
        window.addEventListener('resize', setupLayout);
    });
    
    function setupLayout() {
        const formWrapper = document.querySelector('.form-wrapper');
        const mobileSection = document.querySelector('.mobile-social-section');
        const divider = document.querySelector('.vertical-divider');
        const socialContent = document.querySelector('.social-content');
        const formContent = document.querySelector('.form-content');
        
        if (isMobile()) {
            // Mobile layout
            if (mobileSection) mobileSection.style.display = 'block';
            if (divider) divider.style.display = 'none';
            if (socialContent) socialContent.style.display = 'none';
            
            if (formWrapper) {
                formWrapper.style.display = 'block';
                formWrapper.style.backgroundColor = 'rgba(42, 42, 42, 0.75)';
                formWrapper.style.borderRadius = '14px';
                formWrapper.style.border = '1px solid rgba(0, 255, 0, 0.15)';
                formWrapper.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.4), 0 0 2px rgba(0, 255, 0, 0.2), 0 0 8px rgba(0, 255, 0, 0.1)';
                formWrapper.style.padding = '2.75rem';
                formWrapper.style.maxWidth = '400px';
            }
            
            if (formContent) {
                formContent.style.padding = '0';
                formContent.style.border = 'none';
                formContent.style.borderRadius = '0';
                formContent.style.boxShadow = 'none';
                formContent.style.backgroundColor = 'transparent';
            }
        } else {
            // Desktop layout
            if (mobileSection) mobileSection.style.display = 'none';
            if (divider) divider.style.display = 'block';
            if (socialContent) socialContent.style.display = 'flex';
            
            if (formWrapper) {
                formWrapper.style.display = 'grid';
                formWrapper.style.backgroundColor = 'transparent';
                formWrapper.style.borderRadius = '0';
                formWrapper.style.border = 'none';
                formWrapper.style.boxShadow = 'none';
                formWrapper.style.padding = '0';
                formWrapper.style.maxWidth = '900px';
            }
            
            if (formContent) {
                formContent.style.padding = '2.75rem';
                formContent.style.backgroundColor = 'rgba(42, 42, 42, 0.75)';
                formContent.style.borderRadius = '14px 0 0 14px';
                formContent.style.border = '1px solid rgba(0, 255, 0, 0.15)';
                formContent.style.borderRight = 'none';
                formContent.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.4), 0 0 2px rgba(0, 255, 0, 0.2), 0 0 8px rgba(0, 255, 0, 0.1)';
            }
        }
    }
    """)
    
    # Mobile version of social login options
    mobile_social_section = Div(
        Div(
            Span("OR"),
            cls="divider"
        ),
        Div(
            Button(
                Svg(
                    tag("path", d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z", fill="currentColor"),
                    viewBox="0 0 24 24",
                    xmlns="http://www.w3.org/2000/svg",
                    cls="social-icon"
                ),
                "Continue with Google",
                type="button",
                cls="social-button google-button",
                onclick="handleGoogleLogin()"
            ),
            Button(
                Svg(
                    tag("path", d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12", fill="currentColor"),
                    viewBox="0 0 24 24",
                    xmlns="http://www.w3.org/2000/svg",
                    cls="social-icon"
                ),
                "Continue with GitHub",
                type="button",
                cls="social-button github-button",
                onclick="handleGithubLogin()"
            ),
            cls="social-logins"
        ),
        P(
            "Don't have an account? ",
            A("Sign up now", href="/signup", cls="signup-link"),
            cls="signup-prompt"
        ),
        cls="mobile-social-section"
    )
    
    # Return a structure that closely mirrors the React component's layout
    return Div(
        Link(rel="stylesheet", href="/css/sign-in.css"),
        Div(
            Div(
                H1("Sign In to DeadDevelopers"),
                form,
                mobile_social_section,  # Only shown on mobile
                cls="form-content"
            ),
            # The vertical divider for desktop layout - completely separate from panel borders
            Div(cls="vertical-divider"),
            # Desktop social content (only shown on desktop)
            Div(
                H2("Or continue with", cls="desktop-heading"),
                Div(
                    Button(
                        Svg(
                            tag("path", d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z", fill="currentColor"),
                            viewBox="0 0 24 24",
                            xmlns="http://www.w3.org/2000/svg",
                            cls="social-icon"
                        ),
                        "Continue with Google",
                        type="button",
                        cls="social-button google-button",
                        onclick="handleGoogleLogin()"
                    ),
                    Button(
                        Svg(
                            tag("path", d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12", fill="currentColor"),
                            viewBox="0 0 24 24",
                            xmlns="http://www.w3.org/2000/svg",
                            cls="social-icon"
                        ),
                        "Continue with GitHub",
                        type="button",
                        cls="social-button github-button",
                        onclick="handleGithubLogin()"
                    ),
                    cls="social-logins"
                ),
                P(
                    "Don't have an account? ",
                    A("Sign up now", href="/signup", cls="signup-link"),
                    cls="signup-prompt"
                ),
                cls="social-content"
            ),
            cls="form-wrapper"
        ),
        responsive_script,
        cls="container"
    )

@rt('/login')
def get(req):
    """Render login form with terminal aesthetics"""
    return login_form(req)

@rt('/login')
def post(email: str, password: str, req, session):
    """Handle login form submission and authenticate Django user"""
    # Rate limiting check
    client_ip = req.client.host
    rate_limit_key = f"login_ratelimit_{client_ip}"
    
    # Check if IP has exceeded rate limit (10 login attempts per 15 minutes)
    login_count = cache.get(rate_limit_key, 0)
    if login_count >= 10:
        return login_form(req, "Too many login attempts. Please try again in 15 minutes.")
    
    # Attempt to authenticate user
    user = authenticate(username=email, password=password)

    # If authentication fails, return login form with error
    if not user:
        # Increment failed login counter
        cache.set(rate_limit_key, login_count + 1, 900)  # 15 minutes expiry
        return login_form(req, "Invalid email or password")

    # Check if email is verified
    try:
        email_address = EmailAddress.objects.get(user=user, email=user.email)
        if not email_address.verified:
            # Auto-verify in development mode (when SMTP is not configured)
            # In production, uncomment email sending and remove auto-verification
            email_address.verified = True
            email_address.save()
            # TODO: Re-enable email confirmation in production
            # send_email_confirmation(req, user)
            # return login_form(req, "Email not verified. We've sent a new verification email to your address.")
    except EmailAddress.DoesNotExist:
        # Create an email address record and auto-verify in development
        email_address = EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=True  # Auto-verify in development
        )
        # TODO: Re-enable email confirmation in production
        # send_email_confirmation(req, user)
        # return login_form(req, "Email not verified. We've sent a verification email to your address.")

    # Use AuthBridge to log in user in both FastHTML and Django sessions
    AuthBridge.login_user(req, session, user)

    # Clear rate limit on successful login
    cache.delete(rate_limit_key)

    # Add welcome back toast
    add_toast(session, f"Welcome back, {user.get_display_name()}!", "success")

    # Redirect to dashboard, stamping the Django sessionid cookie so DRF
    # /api/* endpoints recognise the user too.
    response = RedirectResponse('/dashboard', status_code=303)
    return AuthBridge.apply_session_cookie(response, req)

@rt('/logout')
def get(req, session):
    """Log user out of both Django and FastHTML sessions"""
    AuthBridge.logout_user(req, session)
    add_toast(session, "You've been logged out successfully.", "info")
    response = RedirectResponse('/', status_code=303)
    return AuthBridge.apply_session_cookie(response, req)
