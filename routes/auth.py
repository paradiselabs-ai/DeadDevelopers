from fasthtml.common import *
from dataclasses import dataclass
from app import app, rt, django_authenticate, django_create_user, django_logout

@dataclass
class SignupForm:
    email: str
    password: str
    name: str

@dataclass
class LoginForm:
    email: str
    password: str

@rt('/login')
def get():
    """Login page using FastHTML components"""
    return Titled("Login - DeadDevelopers",
        Container(
            Div(
                H1("Login to DeadDevelopers", cls="text-center"),
                Form(
                    # Email field
                    Div(
                        Label("Email"),
                        Input(type="email", id="email", name="email", 
                              required=True, cls="form-input"),
                        cls="form-group"
                    ),
                    # Password field
                    Div(
                        Label("Password"),
                        Input(type="password", id="password", name="password", 
                              required=True, cls="form-input"),
                        cls="form-group"
                    ),
                    # Error message (hidden by default)
                    Div(
                        P("Invalid email or password", cls="error-message"),
                        id="login-error", 
                        style="display: none",
                        cls="error-container"
                    ),
                    # Submit button
                    Button("Login", type="submit", cls="submit-button"),
                    hx_post="/login",
                    hx_target="body",
                    hx_swap="outerHTML"
                ),
                # Signup link
                Div(
                    P(
                        "Don't have an account? ",
                        A("Sign up", href="/signup"),
                        cls="text-center"
                    ),
                    cls="signup-link"
                ),
                cls="login-container"
            ),
            cls="login-page"
        ),
        Script("""
            document.addEventListener('htmx:responseError', function(event) {
                if (event.detail.elt.getAttribute('hx-post') === '/login') {
                    document.getElementById('login-error').style.display = 'block';
                }
            });
        """)
    )

@rt('/login')
def post(form: LoginForm, session):
    """Handle login form submission"""
    success, user = django_authenticate(form.email, form.password, session)
    if success:
        # Add toast notification
        add_toast(session, f"Welcome back, {user['name']}! Your AI assistant is ready to code.", "success")
        return RedirectResponse('/dashboard', status_code=303)
    else:
        # Return error response for HTMX
        return Response(
            "Invalid email or password", 
            status_code=401,
            headers={"HX-Trigger": '{"showLoginError": true}'}
        )

@rt('/signup')
def get():
    """Signup page using FastHTML components"""
    return Titled("Sign Up - DeadDevelopers",
        Container(
            Div(
                H1("Join DeadDevelopers", cls="text-center"),
                Form(
                    # Name field
                    Div(
                        Label("Name"),
                        Input(type="text", id="name", name="name", 
                              required=True, cls="form-input"),
                        cls="form-group"
                    ),
                    # Email field
                    Div(
                        Label("Email"),
                        Input(type="email", id="email", name="email", 
                              required=True, cls="form-input"),
                        cls="form-group"
                    ),
                    # Password field
                    Div(
                        Label("Password"),
                        Input(type="password", id="password", name="password", 
                              required=True, cls="form-input"),
                        cls="form-group"
                    ),
                    # Disclaimer
                    Div(
                        P("By signing up, you acknowledge that AI will write most of your code, and you're totally fine with that.", 
                          cls="disclaimer-text"),
                        cls="disclaimer"
                    ),
                    # Error container
                    Div(id="signup-errors", cls="error-container"),
                    # Submit button
                    Button("Create Account", type="submit", cls="submit-button"),
                    hx_post="/signup",
                    hx_target="body",
                    hx_swap="outerHTML"
                ),
                # Login link
                Div(
                    P(
                        "Already have an account? ",
                        A("Log in", href="/login"),
                        cls="text-center"
                    ),
                    cls="login-link"
                ),
                cls="signup-container"
            ),
            cls="signup-page"
        )
    )

@rt('/signup')
def post(form: SignupForm, session):
    """Handle signup form submission"""
    success, result = django_create_user({
        'email': form.email,
        'password': form.password,
        'name': form.name
    }, session)

    if success:
        # Add toast notification
        add_toast(session, f"Welcome aboard, {form.name}! Let's write some AI-powered code.", "success")
        return RedirectResponse('/dashboard', status_code=303)
    else:
        # Return form with errors
        # In a real implementation, you would extract and display the validation errors
        return Response(
            "Error in form submission", 
            status_code=400,
            headers={"HX-Trigger": '{"showSignupErrors": true}'}
        )

@rt('/logout')
def get(session):
    """Handle logout"""
    django_logout(session)
    add_toast(session, "See you soon! Your AI will miss you.", "info")
    return RedirectResponse('/', status_code=303)

@rt('/profile')
def get(session, user_id=None):
    """User profile page"""
    # Get user data from session
    user_data = session.get('user', {})
    if not user_data:
        return RedirectResponse('/login', status_code=303)
    
    return Titled(f"My Profile - {user_data.get('name', 'User')}",
        Container(
            Div(
                H1("My Profile", cls="profile-header"),
                P("Manage your DeadDevelopers account", cls="profile-description"),
                # Profile content would go here
                Div(
                    # AI usage meter
                    Div(
                        H3("AI Usage: ", 
                           Span(f"{user_data.get('ai_percentage', 0)}%", 
                                id="ai-percentage-value"), 
                           cls="ai-meter-label"),
                        Div(
                            Div(
                                cls="ai-fill", 
                                id="ai-meter-fill",
                                style=f"width: {user_data.get('ai_percentage', 0)}%",
                                hx_post="/update-ai-percentage",
                                hx_trigger="change from:#ai-percentage-slider",
                                hx_vals='js:{"ai_percentage": document.getElementById("ai-percentage-slider").value}',
                                hx_swap="outerHTML"
                            ),
                            cls="ai-meter"
                        ),
                        Div(
                            Input(
                                type="range", 
                                min="0", 
                                max="100", 
                                value=str(user_data.get('ai_percentage', 0)), 
                                id="ai-percentage-slider"
                            ),
                            cls="ai-range-control"
                        ),
                        cls="profile-section"
                    ),
                    
                    # Other profile sections
                    Div(
                        A("← Back to Dashboard", 
                          href="/dashboard", 
                          cls="dashboard-link"),
                        cls="profile-actions"
                    ),
                    cls="profile-content"
                ),
                cls="profile-container"
            )
        ),
        # Add some JavaScript to handle the AI percentage slider
        Script("""
            document.getElementById('ai-percentage-slider').addEventListener('input', function() {
                document.getElementById('ai-percentage-value').innerText = this.value + '%';
                document.getElementById('ai-meter-fill').style.width = this.value + '%';
            });
        """)
    )

@rt('/update-ai-percentage')
def post(ai_percentage: int, session):
    """Update the user's AI usage percentage"""
    # Update session data
    user_data = session.get('user', {})
    user_data['ai_percentage'] = ai_percentage
    session['user'] = user_data
    
    # Return the updated meter fill element
    return Div(
        cls="ai-fill", 
        id="ai-meter-fill",
        style=f"width: {ai_percentage}%",
        hx_post="/update-ai-percentage",
        hx_trigger="change from:#ai-percentage-slider",
        hx_vals='js:{"ai_percentage": document.getElementById("ai-percentage-slider").value}',
        hx_swap="outerHTML"
    )
