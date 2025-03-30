from fasthtml.common import *
from app import app, rt
from django.urls import reverse
from allauth.account.models import EmailConfirmation, EmailAddress
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist

# Custom terminal-styled components
def terminal_card(*args, **kwargs):
    """Create a terminal-styled card component"""
    return Div(*args, cls=f"terminal-card {kwargs.get('cls', '')}", **{k: v for k, v in kwargs.items() if k != 'cls'})

def code_block(content):
    """Create a terminal-styled code block"""
    return Div(content, cls="code-block")

def success_message(content):
    """Create a terminal-styled success message"""
    return Div(P(content, raw=True), cls="success-message")

def error_message(content):
    """Create a terminal-styled error message"""
    return Div(P(content), cls="error-message")

def terminal_button(text, **kwargs):
    """Create a terminal-styled button"""
    return Button(text, cls=f"terminal-button {kwargs.get('cls', '')}", **{k: v for k, v in kwargs.items() if k != 'cls'})

def terminal_link(text, href, **kwargs):
    """Create a terminal-styled link"""
    return A(text, href=href, cls=f"terminal-button {kwargs.get('cls', '')}", **{k: v for k, v in kwargs.items() if k != 'cls'})

# Common page elements
def email_page_headers():
    """Return common headers for email confirmation pages"""
    return [
        Link(rel='stylesheet', href='/css/style.css'),
        Link(rel='stylesheet', href='/css/email_confirm.css'),
        Link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap')
    ]

# Email confirmation route
@rt('/accounts/confirm-email/<key>')
def get(key: str):
    """Handle email confirmation GET request"""
    try:
        # Try to get the confirmation object
        confirmation = EmailConfirmation.objects.get(key=key)
        email = confirmation.email_address.email

        # Return confirmation page
        return Titled(
            "Email Verification - DeadDevelopers",
            *email_page_headers(),
            Div(
                terminal_card(
                    H1("Email Verification"),
                    code_block(f"// Verifying email: {email}"),
                    Form(
                        success_message(f"Please confirm that <strong>{email}</strong> is your email address by clicking the button below."),
                        terminal_button("CONFIRM EMAIL", type="submit"),
                        method="post",
                        action=f"/accounts/confirm-email/{key}"
                    ),
                    cls="terminal-card"
                ),
                cls="container"
            )
        )
    except ObjectDoesNotExist:
        # Handle invalid or expired key
        return email_confirmation_error("This confirmation link is invalid or has expired.")

@rt('/accounts/confirm-email/<key>')
def post(key: str):
    """Handle email confirmation POST request"""
    try:
        # Try to get the confirmation object
        confirmation = EmailConfirmation.objects.get(key=key)

        # Confirm the email
        confirmation.email_address.verified = True
        confirmation.email_address.save()

        # Return success page
        return Titled(
            "Email Verified Successfully - DeadDevelopers",
            *email_page_headers(),
            Div(
                terminal_card(
                    H1("Email Verified Successfully"),
                    success_message("Your email address has been verified successfully!"),
                    code_block("""// Status: VERIFICATION_COMPLETE
// Account: ACTIVATED
// Next step: LOGIN"""),
                    P("You can now log in to your DeadDevelopers account and start building with AI."),
                    terminal_link("GO TO DASHBOARD", "/dashboard"),
                    cls="terminal-card"
                ),
                cls="container"
            )
        )
    except ObjectDoesNotExist:
        # Handle invalid or expired key
        return email_confirmation_error("This confirmation link is invalid or has expired.")

def email_confirmation_error(error_text):
    """Display error page for email confirmation"""
    return Titled(
        "Verification Error - DeadDevelopers",
        *email_page_headers(),
        Div(
            terminal_card(
                H1("Verification Error"),
                error_message(error_text),
                code_block("""// Error code: VERIFICATION_FAILED
// Possible causes:
// - Link has expired
// - Link has already been used
// - Invalid verification key"""),
                P("Please request a new verification email or contact support if the problem persists."),
                terminal_link("REQUEST NEW EMAIL", "/accounts/email"),
                cls="terminal-card"
            ),
            cls="container"
        )
    )

# Handle verification sent page
@rt('/accounts/confirm-email/')
def get():
    """Handle verification sent page"""
    return Titled(
        "Verification Email Sent - DeadDevelopers",
        *email_page_headers(),
        Div(
            terminal_card(
                H1("Verification Email Sent"),
                code_block("// Status: VERIFICATION_PENDING"),
                success_message("We've sent a verification email to your address. Please check your inbox and click the verification link."),
                P("If you don't see the email, check your spam folder or request a new verification email."),
                terminal_link("BACK TO LOGIN", "/login"),
                cls="terminal-card"
            ),
            cls="container"
        )
    )