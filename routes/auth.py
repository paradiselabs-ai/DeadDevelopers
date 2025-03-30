from fasthtml.common import *
from dataclasses import dataclass
from app import app, rt, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Q
import re
from fasthtml.svg import Svg, ft_svg as tag
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress

@dataclass
class SignupForm:
    email: str
    password: str
    first_name: str
    last_name: str
    username: str
    agree_terms: bool = False

def signup_form(errors=None):
    """Modern signup form based on the React implementation"""
    # Ensure errors is a list or empty
    if errors is None:
        errors = []
    elif not isinstance(errors, list):
        errors = [error_message(errors)]
    # Create responsive JavaScript to handle mobile/desktop views
    responsive_script = Script("""
    document.addEventListener('DOMContentLoaded', function() {
        function checkMobile() {
            return window.innerWidth < 768;
        }

        function setupLayout() {
            const isMobile = checkMobile();
            const formWrapper = document.querySelector('.form-wrapper');
            const mobileSection = document.querySelector('.mobile-social-section');
            const verticalDivider = document.querySelector('.vertical-divider');
            const socialContent = document.querySelector('.social-content');

            if (isMobile) {
                // Mobile layout
                if (mobileSection) mobileSection.style.display = 'block';
                if (verticalDivider) verticalDivider.style.display = 'none';
                if (socialContent) socialContent.style.display = 'none';
            } else {
                // Desktop layout
                if (mobileSection) mobileSection.style.display = 'none';
                if (verticalDivider) verticalDivider.style.display = 'block';
                if (socialContent) socialContent.style.display = 'flex';
            }
        }

        // Initial setup
        setupLayout();

        // Re-check on window resize
        window.addEventListener('resize', setupLayout);

        // Handle social login buttons
        window.handleGoogleSignUp = function() {
            console.log("Signing up with Google");
            window.location.href = '/accounts/google/login/';
        };

        window.handleGithubSignUp = function() {
            console.log("Signing up with GitHub");
            window.location.href = '/accounts/github/login/';
        };
    });
    """)

    # Link to the CSS file
    css_link = Link(rel="stylesheet", href="/css/sign-up.css")

    # Google SVG icon
    google_svg = Svg(
        tag("path", d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"),
        viewBox="0 0 24 24",
        xmlns="http://www.w3.org/2000/svg",
        cls="social-icon"
    )

    # GitHub SVG icon
    github_svg = Svg(
        tag("path", d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"),
        viewBox="0 0 24 24",
        xmlns="http://www.w3.org/2000/svg",
        cls="social-icon"
    )

    # Mobile social section (only shown on mobile)
    mobile_social_section = Div(
        Div(
            Span("OR CONTINUE WITH"),
            cls="divider"
        ),
        Div(
            Button(
                google_svg,
                "Google",
                type="button",
                cls="social-button google-button",
                onclick="handleGoogleSignUp()"
            ),
            Button(
                github_svg,
                "GitHub",
                type="button",
                cls="social-button github-button",
                onclick="handleGithubSignUp()"
            ),
            cls="social-logins"
        ),
        cls="mobile-social-section"
    )

    # Feature highlights for desktop view
    feature_highlights = Div(
        H3("Why join DeadDevelopers?", cls="features-title"),
        Ul(
            Li(
                Div(cls="feature-icon code-icon"),
                Div(
                    H4("Collaborative Coding"),
                    P("Code together in real-time with team members"),
                    cls="feature-text"
                ),
                cls="feature-item"
            ),
            Li(
                Div(cls="feature-icon deploy-icon"),
                Div(
                    H4("One-Click Deployment"),
                    P("Deploy your projects instantly to production"),
                    cls="feature-text"
                ),
                cls="feature-item"
            ),
            Li(
                Div(cls="feature-icon community-icon"),
                Div(
                    H4("Developer Community"),
                    P("Connect with like-minded developers"),
                    cls="feature-text"
                ),
                cls="feature-item"
            ),
            cls="features-list"
        ),
        cls="feature-highlights"
    )

    # Main form content
    form_content = Div(
        A(
            Svg(
                tag("path", d="M19 12H5", stroke="currentColor", stroke_width="2", stroke_linecap="round", stroke_linejoin="round"),
                tag("path", d="M12 19L5 12L12 5", stroke="currentColor", stroke_width="2", stroke_linecap="round", stroke_linejoin="round"),
                width="16",
                height="16",
                viewBox="0 0 24 24",
                fill="none",
                xmlns="http://www.w3.org/2000/svg",
                cls="back-icon"
            ),
            "Back to Home",
            href="/",
            cls="back-link"
        ),
        Div(
            H1("Join DeadDevelopers"),
            P("Create your account to get started", cls="form-subtitle"),
            cls="form-header"
        ),
        Form(
            Div(
                Div(
                    Div(
                        Label("First Name", for_="firstName"),
                        Input(
                            type="text",
                            id="firstName",
                            name="first_name",
                            placeholder="First name",
                            required=True
                        ),
                        cls="form-group"
                    ),
                    Div(
                        Label("Last Name", for_="lastName"),
                        Input(
                            type="text",
                            id="lastName",
                            name="last_name",
                            placeholder="Last name",
                            required=True
                        ),
                        cls="form-group"
                    ),
                    cls="name-row"
                ),
                Div(
                    Label("Username", for_="username"),
                    Input(
                        type="text",
                        id="username",
                        name="username",
                        placeholder="Choose a username",
                        required=True
                    ),
                    cls="form-group"
                ),
                Div(
                    Label("Email Address", for_="email"),
                    Input(
                        type="email",
                        id="email",
                        name="email",
                        placeholder="Email address",
                        required=True
                    ),
                    cls="form-group"
                ),
                Div(
                    Label("Password", for_="password"),
                    Input(
                        type="password",
                        id="password",
                        name="password",
                        placeholder="Create a password",
                        required=True
                    ),
                    P("Must be at least 8 characters", cls="password-hint"),
                    cls="form-group"
                ),
                Div(
                    Input(
                        type="checkbox",
                        id="agreeTerms",
                        name="agree_terms",
                        required=True
                    ),
                    Label(
                        "I agree to the ",
                        A("Terms of Service", href="#", cls="terms-link"),
                        " and ",
                        A("Privacy Policy", href="#", cls="terms-link"),
                        for_="agreeTerms",
                        cls="checkbox-label"
                    ),
                    cls="form-group checkbox-group"
                ),
                Div(
                    *errors if errors else "",
                    id="signup-errors",
                    cls="form-errors"
                ),
                cls="form-section"
            ),
            Button(
                "Create Account",
                type="submit",
                cls="signup-button"
            ),
            action="/signup",
            method="post",
            cls="signup-form"
        ),
        mobile_social_section,
        Div(
            "Already have an account? ",
            A("Sign in", href="/login", cls="signin-link"),
            cls="signin-prompt"
        ),
        cls="form-content"
    )

    # Desktop social content (only shown on desktop)
    social_content = Div(
        Div(
            H2("Or continue with", cls="desktop-heading"),
            Div(
                Button(
                    google_svg,
                    "Google",
                    type="button",
                    cls="social-button google-button",
                    onclick="handleGoogleSignUp()"
                ),
                Button(
                    github_svg,
                    "GitHub",
                    type="button",
                    cls="social-button github-button",
                    onclick="handleGithubSignUp()"
                ),
                cls="social-logins"
            ),
            feature_highlights,
            cls="social-content-inner"
        ),
        cls="social-content"
    )

    # Main container
    return Div(Link(rel="stylesheet", href="/css/sign-up.css"),
        css_link,
        responsive_script,
        Div(
            form_content,
            Div(cls="vertical-divider"),
            social_content,
            cls="form-wrapper"
        ),
        cls="container"
    )

def error_message(error_text):
    """Format error message with terminal-style appearance that matches the application's aesthetic"""
    # Format error text to look like a terminal message
    formatted_text = error_text.strip()

    return Div(
        P(f"{formatted_text}", cls="error-text"),
        cls="error-message"
    )

def signup_page(errors=None):
    """Render the full signup page with the form and any errors"""
    # Ensure errors is properly formatted
    if errors is None:
        errors = []

    return Titled(
        Link(rel="stylesheet", href="/css/style.css"),
        signup_form(errors)
    )

@rt('/signup')
def get():
    """Render modern signup form"""
    return signup_page()

@rt('/signup')
def post(form: SignupForm, req):
    """Handle signup form submission and create Django user"""
    # Form validation with modern error messages
    errors = []

    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", form.email):
        errors.append(error_message("Invalid email format."))

    # Check if email already exists
    if User.objects.filter(email=form.email).exists():
        errors.append(error_message("Email already registered."))

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
    except Exception as e:
        # Handle any other validation errors
        errors.append(error_message(str(e)))

    # Validate terms agreement
    if not form.agree_terms:
        errors.append(error_message("You must agree to the Terms of Service and Privacy Policy."))

    # Return form with errors if validation failed
    if errors:
        # Return the full signup page with errors
        return signup_page(errors)

    try:
        # Create user through Django's auth system
        user = User.objects.create_user(
            username=form.username,
            email=form.email,
            password=form.password,
            first_name=form.first_name,
            last_name=form.last_name,
            ai_percentage=0
        )

        # Create EmailAddress record for the user (unverified)
        email_address, created = EmailAddress.objects.get_or_create(
            user=user,
            email=form.email,
            defaults={'primary': True, 'verified': False}
        )

        # Send verification email
        send_email_confirmation(req, user)

        # Add a welcome toast with improved messaging
        add_toast(req.session, f"Welcome, {user.get_display_name()}! Please check your email to verify your account and unlock all features.", "success")

        # Redirect to verification sent page
        return RedirectResponse('/accounts/confirm-email/', status_code=303)

    except Exception as e:
        # Handle any unexpected errors during user creation
        errors.append(error_message(f"An error occurred during registration: {str(e)}"))
        return signup_page(errors)

def login_form(error=None):
    """Styled login form that closely matches the original React implementation"""
    # Handle different types of error inputs
    if isinstance(error, list):
        # If it's a list of errors, use them directly
        errors = error
    elif error:
        # If it's a single error string, convert to a list with one error message
        errors = [error_message(error)]
    else:
        # No errors
        errors = []
    
    # Create the form component - structured like the React version
    form = Form(
        Div(
            Label("Email Address", for_="email"),
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
            Label("Password", for_="password"),
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
            *errors if errors else "",
            id="login-errors",
            cls="form-errors"
        ),
        Button(
            "Log In",
            type="submit",
            cls="login-button"
        ),
        action="/login",
        method="post",
        cls="signin-form"
    )
    
    # Create responsive JavaScript to handle mobile/desktop views exactly like React's approach
    responsive_script = Script("""
    function isMobile() {
        return window.innerWidth < 768;
    }
    
    function handleGoogleLogin() {
        console.log("Logging in with Google");
        window.location.href = '/accounts/google/login/';
    }

    function handleGithubLogin() {
        console.log("Logging in with GitHub");
        window.location.href = '/accounts/github/login/';
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
            Span("OR CONTINUE WITH"),
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
                A(
                Svg(
                    tag("path", d="M19 12H5", stroke="currentColor", stroke_width="2", stroke_linecap="round", stroke_linejoin="round"),
                    tag("path", d="M12 19L5 12L12 5", stroke="currentColor", stroke_width="2", stroke_linecap="round", stroke_linejoin="round"),
                    width="16",
                    height="16",
                    viewBox="0 0 24 24",
                    fill="none",
                    xmlns="http://www.w3.org/2000/svg",
                    cls="back-icon"
                    ),
                    "Back to Home",
                    href="/",
                    cls="back-link"
                 ),
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

def login_page(error=None):
    """Render the full login page with the form and any errors"""
    # Ensure errors is properly formatted
    if error is None:
        errors = []
    elif isinstance(error, list):
        errors = error
    else:
        errors = [error_message(error)]

    return Titled(
        Link(rel="stylesheet", href="/css/style.css"),
        login_form(errors)
    )

@rt('/login')
def get():
    """Render modern login form"""
    return login_page()

@rt('/login')
def post(email: str, password: str, req):
    """Handle login form submission and authenticate Django user"""
    # Attempt to authenticate user
    user = authenticate(username=email, password=password)

    # Create a list for errors
    errors = []

    # If authentication fails, return login page with error
    if not user:
        errors.append(error_message("Invalid email or password"))
        return login_page(errors)

    # Check if email is verified
    try:
        email_address = EmailAddress.objects.get(user=user, email=email)
        if not email_address.verified:
            # Send a new verification email
            send_email_confirmation(req, user)
            errors.append(error_message("Email not verified. We've sent a new verification email to your address."))
            return login_page(errors)
    except EmailAddress.DoesNotExist:
        # Create an email address record if it doesn't exist
        EmailAddress.objects.create(
            user=user,
            email=email,
            primary=True,
            verified=False
        )
        # Send verification email
        send_email_confirmation(req, user)
        errors.append(error_message("Email not verified. We've sent a verification email to your address."))
        return login_page(errors)

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
