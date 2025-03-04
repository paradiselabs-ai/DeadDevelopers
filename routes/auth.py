from fasthtml.common import *
from dataclasses import dataclass
from app import app, rt

@dataclass
class SignupForm:
    email: str
    password: str
    name: str

def signup_form():
    return Card(
        H2("Join DeadDevelopers"),
        Form(
            Input(
                type="text",
                name="name",
                placeholder="Your Name",
                required=True,
                cls="signup-input"
            ),
            Input(
                type="email",
                name="email",
                placeholder="Email",
                required=True,
                cls="signup-input"
            ),
            Input(
                type="password",
                name="password",
                placeholder="Password",
                required=True,
                cls="signup-input"
            ),
            P(
                "By signing up, you acknowledge that AI will write most of your code, " 
                "and you're totally fine with that.",
                cls="signup-disclaimer"
            ),
            Button(
                "Create Account",
                type="submit",
                cls="signup-submit"
            ),
            hx_post="/signup",
            cls="signup-form"
        ),
        cls="signup-card"
    )

@rt('/signup')
def get():
    return signup_form()

@rt('/signup')
def post(form: SignupForm, session):
    # TODO: Implement actual user creation with Django auth
    # For now, just redirect to dashboard
    session['user'] = {
        'name': form.name,
        'email': form.email,
        'ai_percent': 0
    }
    add_toast(session, f"Welcome aboard, {form.name}! Let's write some AI-powered code.", "success")
    return RedirectResponse('/dashboard', status_code=303)

def login_form():
    return Card(
        H2("Welcome Back"),
        Form(
            Input(
                type="email",
                name="email",
                placeholder="Email",
                required=True,
                cls="login-input"
            ),
            Input(
                type="password",
                name="password",
                placeholder="Password",
                required=True,
                cls="login-input"
            ),
            Button(
                "Log In",
                type="submit",
                cls="login-submit"
            ),
            hx_post="/login",
            cls="login-form"
        ),
        cls="login-card"
    )

@rt('/login')
def get():
    return login_form()

@rt('/login')
def post(email: str, password: str, session):
    # TODO: Implement actual login with Django auth
    session['user'] = {
        'name': 'Test User',
        'email': email,
        'ai_percent': 0
    }
    add_toast(session, "Welcome back! Your AI assistant is ready to code.", "success")
    return RedirectResponse('/dashboard', status_code=303)

@rt('/logout')
def get(session):
    add_toast(session, "See you soon! Your AI will miss you.", "info")
    session.clear()
    return RedirectResponse('/', status_code=303)
