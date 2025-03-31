from fasthtml.common import *
from dataclasses import dataclass
from app import app, rt, User, add_toast
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Q
import re
from fasthtml.svg import Svg, ft_svg as tag
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress
from utils.toast import handle_session_safely, RequestWrapper

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

def handle_session_safely(session, action_func, default_value=None, log_prefix="Session operation"):
    """
    Safely handle session operations with proper error handling.

    Args:
        session: The session object to operate on
        action_func: A function that performs the session operation
        default_value: Value to return if operation fails
        log_prefix: Prefix for error logging

    Returns:
        The result of action_func or default_value if an error occurs
    """
    try:
        return action_func(session)
    except Exception as e:
        print(f"{log_prefix} error: {str(e)}")
        return default_value

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

    try:
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", form.email):
            errors.append(error_message("Invalid email format."))

        # Check if email already exists (case-insensitive)
        try:
            if User.objects.filter(email__iexact=form.email).exists():
                errors.append(error_message("Email already registered."))
        except Exception as db_error:
            print(f"Database error checking email existence: {str(db_error)}")
            errors.append(error_message("We couldn't verify if your email is available. Please try again."))

        # Check if username is available
        try:
            if User.objects.filter(username=form.username).exists():
                errors.append(error_message("Username already taken."))
        except Exception as db_error:
            print(f"Database error checking username existence: {str(db_error)}")
            errors.append(error_message("We couldn't verify if your username is available. Please try again."))

        # Validate password strength
        try:
            validate_password(form.password)
        except ValidationError as e:
            # Format Django's password validation errors
            for error in e.messages:
                errors.append(error_message(error))
        except Exception as e:
            # Handle any other validation errors
            print(f"Password validation error: {str(e)}")
            errors.append(error_message("Password validation failed. Please ensure it meets security requirements."))

        # Validate terms agreement
        if not form.agree_terms:
            errors.append(error_message("You must agree to the Terms of Service and Privacy Policy."))

        # Return form with errors if validation failed
        if errors:
            # Return the full signup page with errors
            return signup_page(errors)

        # User creation process
        try:
            # Create user through Django's auth system
            # Store email in lowercase for consistency
            user = User.objects.create_user(
                username=form.username,
                email=form.email.lower(),  # Always store email in lowercase
                password=form.password,
                first_name=form.first_name,
                last_name=form.last_name,
                ai_percentage=0
            )
        except Exception as user_error:
            # Detailed error handling for user creation
            error_message_text = "An error occurred during account creation."

            if "UNIQUE constraint" in str(user_error) and "username" in str(user_error).lower():
                error_message_text = "This username is already taken. Please choose another."
            elif "UNIQUE constraint" in str(user_error) and "email" in str(user_error).lower():
                error_message_text = "This email is already registered. Please use another email or try to log in."
            else:
                # Log the detailed error for debugging
                print(f"User creation error: {str(user_error)}")

            errors.append(error_message(error_message_text))
            return signup_page(errors)

        # Email verification setup
        try:
            # Create EmailAddress record for the user (unverified)
            # Use the email from the user object (already lowercase)
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,  # Use the email from the user object (already lowercase)
                defaults={'primary': True, 'verified': False}
            )
        except Exception as email_record_error:
            # Log the error but continue - this is recoverable
            print(f"Error creating email address record: {str(email_record_error)}")
            # We'll still try to send the verification email

        # Send verification email
        email_sent = False
        try:
            # Wrap the request to provide build_absolute_uri method
            wrapped_request = RequestWrapper(req)

            # Send confirmation with wrapped request
            send_email_confirmation(wrapped_request, user)
            email_sent = True
        except Exception as email_error:
            # Log the error for debugging
            print(f"Error sending verification email: {str(email_error)}")
            # We'll handle this in the toast message

        # Add appropriate toast message based on email sending success using our safer helper
        if email_sent:
            handle_session_safely(
                req.session,
                lambda session: add_toast(session, f"Welcome, {user.get_display_name()}! Please check your email to verify your account and unlock all features.", "success"),
                None,  # Default return value (None) if operation fails
                "Signup success toast with email verification"
            )
        else:
            handle_session_safely(
                req.session,
                lambda session: add_toast(session, f"Welcome, {user.get_display_name()}! We couldn't send a verification email right now. Please try requesting one from your profile later.", "warning"),
                None,  # Default return value (None) if operation fails
                "Signup warning toast for email verification failure"
            )

        # Redirect to verification sent page or dashboard based on email sending success
        if email_sent:
            return RedirectResponse('/accounts/confirm-email/', status_code=303)
        else:
            # If email wasn't sent, redirect to dashboard with a warning
            return RedirectResponse('/dashboard', status_code=303)

    except Exception as e:
        # Handle any unexpected errors during the entire registration process
        print(f"Unexpected error during registration: {str(e)}")
        errors.append(error_message("An unexpected error occurred during registration. Please try again later."))
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
    # Create a list for errors
    errors = []

    try:
        # Try to find user by email (case-insensitive)
        try:
            # First try exact match
            user = authenticate(username=email, password=password)

            # If that fails, try case-insensitive match
            if not user:
                # Find user with case-insensitive email match
                try:
                    matching_user = User.objects.get(email__iexact=email)
                    # Authenticate with the correct case of email
                    user = authenticate(username=matching_user.email, password=password)
                except (User.DoesNotExist, User.MultipleObjectsReturned):
                    user = None
        except Exception as auth_error:
            print(f"Authentication error: {str(auth_error)}")
            user = None

        # If authentication fails, return login page with error
        if not user:
            errors.append(error_message("Invalid email or password"))
            return login_page(errors)

        # Check if email is verified (case-insensitive)
        try:
            # Get the email address record for this user (case-insensitive)
            email_address = EmailAddress.objects.get(user=user, email__iexact=email)
            if not email_address.verified:
                try:
                    # Wrap the request to provide build_absolute_uri method
                    wrapped_request = RequestWrapper(req)

                    # Send a new verification email
                    send_email_confirmation(wrapped_request, user)
                    errors.append(error_message("Email not verified. We've sent a new verification email to your address."))
                except Exception as e:
                    # Handle email sending errors
                    print(f"Error sending verification email: {str(e)}")
                    errors.append(error_message("Email not verified. We tried to send a verification email but encountered an error. Please try again later."))
                return login_page(errors)
        except EmailAddress.DoesNotExist:
            # Create an email address record if it doesn't exist
            try:
                # Always store email in lowercase for consistency
                EmailAddress.objects.create(
                    user=user,
                    email=user.email,  # Use the email from the user object (already lowercase)
                    primary=True,
                    verified=False
                )
                # Send verification email
                try:
                    send_email_confirmation(req, user)
                    errors.append(error_message("Email not verified. We've sent a verification email to your address."))
                except Exception as e:
                    # Handle email sending errors
                    print(f"Error sending verification email: {str(e)}")
                    errors.append(error_message("Email not verified. We tried to send a verification email but encountered an error. Please try again later."))
            except Exception as e:
                # Handle email address creation errors
                print(f"Error creating email address record: {str(e)}")
                errors.append(error_message("An error occurred while processing your account. Please contact support."))
            return login_page(errors)

        # Helper function to set session data
        def set_session_data(session, user):
            session['auth'] = user.username
            session['user'] = {
                'name': user.get_display_name(),
                'email': user.email,
                'ai_percentage': user.ai_percentage
            }
            return True  # Return value indicating success

        # Set session data for FastHTML access using our safer helper
        session_updated = handle_session_safely(
            req.session,
            lambda session: set_session_data(session, user),
            False,  # Default return value (False) if operation fails
            "Login session update"
        )

        if not session_updated:
            errors.append(error_message("Login successful, but we encountered an issue with your session. You may need to log in again."))
            return login_page(errors)

        # Add welcome back toast using our safer helper
        handle_session_safely(
            req.session,
            lambda session: add_toast(session, f"Welcome back, {user.get_display_name()}!", "success"),
            None,  # Default return value (None) if operation fails
            "Login toast notification"
        )

        # Redirect to dashboard
        return RedirectResponse('/dashboard', status_code=303)

    except Exception as e:
        # Catch any other unexpected errors during the login process
        print(f"Unexpected error during login: {str(e)}")
        errors.append(error_message("An unexpected error occurred. Please try again later."))
        return login_page(errors)

@rt('/logout')
def get(req):
    """Log user out of both Django and FastHTML sessions"""
    # Track if we had any issues during logout
    had_session_issues = False

    # Helper function to clear FastHTML session
    def clear_fasthtml_session(session):
        if 'auth' in session:
            del session['auth']
        if 'user' in session:
            del session['user']
        return True

    # Helper function to handle Django logout
    def do_django_logout(request):
        logout(request)
        return True

    # Clear FastHTML session first using our safer helper
    fasthtml_session_cleared = handle_session_safely(
        req.session,
        clear_fasthtml_session,
        False,  # Default return value (False) if operation fails
        "FastHTML session clearing during logout"
    )

    if not fasthtml_session_cleared:
        had_session_issues = True

    # Clear Django session if available
    django_logout_success = handle_session_safely(
        req,
        do_django_logout,
        False,  # Default return value (False) if operation fails
        "Django logout"
    )

    if not django_logout_success:
        had_session_issues = True

    # Add appropriate logout toast based on whether there were issues
    if had_session_issues:
        handle_session_safely(
            req.session,
            lambda session: add_toast(session, "You've been logged out, but we encountered some session issues. If you experience any problems, please clear your browser cookies.", "warning"),
            None,  # Default return value (None) if operation fails
            "Logout warning toast"
        )
    else:
        handle_session_safely(
            req.session,
            lambda session: add_toast(session, "You've been logged out successfully.", "info"),
            None,  # Default return value (None) if operation fails
            "Logout success toast"
        )

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

    try:
        # Validate username change
        try:
            if username != user.username and User.objects.filter(username=username).exists():
                errors.append(error_message("Username already taken."))
        except Exception as db_error:
            print(f"Database error checking username existence: {str(db_error)}")
            errors.append(error_message("We couldn't verify if your username is available. Please try again."))

        # Validate email change (case-insensitive)
        try:
            # Case-insensitive comparison
            if email.lower() != user.email.lower() and User.objects.filter(email__iexact=email).exists():
                errors.append(error_message("Email already registered."))
        except Exception as db_error:
            print(f"Database error checking email existence: {str(db_error)}")
            errors.append(error_message("We couldn't verify if your email is available. Please try again."))

        # Validate URL format if provided
        if website and not website.startswith(('http://', 'https://')):
            website = f"https://{website}"

        # Return form with errors if validation failed
        if errors:
            # Get the edit form and insert errors
            try:
                response = get(req)
                response.find("#profile-errors").content = errors
                return response
            except Exception as form_error:
                print(f"Error generating edit form with errors: {str(form_error)}")
                # Fallback to a simple error message if form generation fails
                return RedirectResponse('/profile', status_code=303)

        # Update user fields
        try:
            original_username = user.username
            user.username = username
            user.email = email.lower()  # Always store email in lowercase
            user.first_name = first_name
            user.last_name = last_name
            user.bio = bio
            user.github_username = github_username
            user.twitter_username = twitter_username
            user.website = website
            user.theme_preference = theme_preference
            user.save()
        except Exception as save_error:
            print(f"Error saving user profile: {str(save_error)}")

            # Check for specific database errors
            error_message_text = "An error occurred while saving your profile."
            if "UNIQUE constraint" in str(save_error) and "username" in str(save_error).lower():
                error_message_text = "This username is already taken. Please choose another."
            elif "UNIQUE constraint" in str(save_error) and "email" in str(save_error).lower():
                error_message_text = "This email is already registered. Please use another email."

            errors.append(error_message(error_message_text))
            response = get(req)
            response.find("#profile-errors").content = errors
            return response

        # Helper function to update session data
        def update_session_data(session):
            session['auth'] = user.username
            session['user'] = {
                'name': user.get_display_name(),
                'email': user.email,
                'ai_percentage': user.ai_percentage
            }
            return True

        # Helper function to revert username
        def revert_username(user_obj):
            user_obj.username = original_username
            user_obj.save()
            return True

        # Update session data using our safer helper
        session_updated = handle_session_safely(
            req.session,
            update_session_data,
            False,  # Default return value (False) if operation fails
            "Profile update session update"
        )

        # If username changed but session update failed, this could cause login issues
        # Try to revert the username change to maintain session consistency
        if not session_updated and original_username != username:
            username_reverted = handle_session_safely(
                user,
                revert_username,
                False,  # Default return value (False) if operation fails
                "Username reversion after session update failure"
            )

            if username_reverted:
                errors.append(error_message("We couldn't update your username due to session issues. Other changes were saved."))
                response = get(req)
                response.find("#profile-errors").content = errors
                return response

        # Add appropriate success/warning message using our safer helper
        if session_updated:
            handle_session_safely(
                req.session,
                lambda session: add_toast(session, "Profile updated successfully!", "success"),
                None,  # Default return value (None) if operation fails
                "Profile update success toast"
            )
        else:
            handle_session_safely(
                req.session,
                lambda session: add_toast(session, "Profile updated, but we encountered session issues. You may need to log in again.", "warning"),
                None,  # Default return value (None) if operation fails
                "Profile update warning toast"
            )

        # Redirect to profile view
        return get(req)

    except Exception as e:
        # Handle any unexpected errors during the entire update process
        print(f"Unexpected error during profile update: {str(e)}")
        try:
            errors.append(error_message("An unexpected error occurred. Some changes may not have been saved."))
            response = get(req)
            response.find("#profile-errors").content = errors
            return response
        except Exception:
            # Last resort fallback if everything else fails
            return RedirectResponse('/profile', status_code=303)
