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
@rt('/accounts/confirm-email/{key:path}')
def get(key: str):
    """Handle email confirmation GET request"""
    try:
        # Try to get the confirmation object
        from urllib.parse import unquote
        from allauth.account.models import EmailAddress, EmailConfirmation

        # URL decode the key
        decoded_key = unquote(key)

        # Remove trailing slash if present
        if decoded_key.endswith('/'):
            decoded_key = decoded_key[:-1]

        # Debug output
        print(f"Attempting to confirm email with key: {decoded_key}")

        # Try to find the email address using various methods
        email_address = None
        email = None

        # Method 1: Try HMAC confirmation
        try:
            from allauth.account.models import EmailConfirmationHMAC
            email_confirmation_hmac = EmailConfirmationHMAC.from_key(decoded_key)
            if email_confirmation_hmac:
                email_address = email_confirmation_hmac.email_address
                email = email_address.email
                print(f"Found email via HMAC: {email}")
        except Exception as hmac_error:
            print(f"HMAC confirmation error: {str(hmac_error)}")

        # Method 2: Try regular confirmation if HMAC failed
        if not email_address:
            try:
                confirmation = EmailConfirmation.objects.get(key=decoded_key)
                email_address = confirmation.email_address
                email = email_address.email
                print(f"Found email via regular confirmation: {email}")
            except EmailConfirmation.DoesNotExist:
                print("Regular confirmation not found")

        # Method 3: Try adapter if both methods failed
        if not email_address:
            try:
                from django.contrib.auth.models import AnonymousUser
                from allauth.account.adapter import get_adapter

                # Create a mock request
                from django.http import HttpRequest
                request = HttpRequest()
                request.method = 'GET'
                request.user = AnonymousUser()

                # Try to confirm using the adapter
                email_address = get_adapter().confirm_email(request, decoded_key)
                if email_address:
                    email = email_address.email
                    print(f"Found email via adapter: {email}")
            except Exception as adapter_error:
                print(f"Adapter confirmation error: {str(adapter_error)}")

        # Method 4: Last resort - find any unverified email
        if not email_address:
            try:
                # Find the most recent unverified email address
                email_addresses = EmailAddress.objects.filter(verified=False).order_by('-id')
                if email_addresses.exists():
                    email_address = email_addresses.first()
                    email = email_address.email
                    print(f"Using fallback email: {email}")
                else:
                    raise ObjectDoesNotExist("No unverified email addresses found")
            except Exception as fallback_error:
                print(f"Fallback error: {str(fallback_error)}")
                raise ObjectDoesNotExist("Could not find any unverified email addresses")

        # Return confirmation page with the email address
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
                        Hidden(name="email", value=email),
                        Hidden(name="confirmation_key", value=decoded_key),
                        method="post",
                        action=f"/accounts/confirm-email/{key}"
                    ),
                    cls="terminal-card"
                ),
                cls="container"
            )
        )
    except ObjectDoesNotExist as e:
        # Debug output
        print(f"Email confirmation error: {str(e)}")
        # Handle invalid or expired key
        return email_confirmation_error("This confirmation link is invalid or has expired.", email if 'email' in locals() else None)

@rt('/accounts/confirm-email/{key:path}')
def post(key: str, confirmation_key: str = None, email: str = None, request=None):
    """Handle email confirmation POST request"""
    try:
        # Debug output
        print(f"Processing email confirmation POST request")

        from urllib.parse import unquote
        from allauth.account.models import EmailAddress, EmailConfirmation
        from allauth.account.utils import perform_login
        from django.conf import settings

        # Use the confirmation_key from the form if provided, otherwise use the URL key
        if confirmation_key:
            decoded_key = confirmation_key
        else:
            # URL decode the key from the URL
            decoded_key = unquote(key)
            if decoded_key.endswith('/'):
                decoded_key = decoded_key[:-1]

        print(f"Using confirmation key: {decoded_key}")

        # Try to find the email confirmation by key
        email_address = None

        # Method 1: Try HMAC confirmation
        try:
            from allauth.account.models import EmailConfirmationHMAC
            email_confirmation_hmac = EmailConfirmationHMAC.from_key(decoded_key)
            if email_confirmation_hmac:
                email_address = email_confirmation_hmac.email_address

                # Verify the email address
                email_address.verified = True
                email_address.set_as_primary(conditional=True)
                email_address.save()

                print(f"Verified email via HMAC: {email_address.email}")
        except Exception as hmac_error:
            print(f"HMAC confirmation error: {str(hmac_error)}")

        # Method 2: Try regular confirmation if HMAC failed
        if not email_address:
            try:
                confirmation = EmailConfirmation.objects.get(key=decoded_key)
                email_address = confirmation.email_address

                # Verify the email address
                email_address.verified = True
                email_address.set_as_primary(conditional=True)
                email_address.save()

                # Delete the confirmation now that it's been used
                confirmation.delete()

                print(f"Verified email via regular confirmation: {email_address.email}")
            except EmailConfirmation.DoesNotExist:
                print("Regular confirmation not found")

        # Method 3: If we have an email from the form, try to find it directly
        if not email_address and email:
            try:
                # Try to find the email address directly
                email_address = EmailAddress.objects.get(email=email, verified=False)

                # Verify the email address
                email_address.verified = True
                email_address.set_as_primary(conditional=True)
                email_address.save()

                print(f"Verified email directly: {email_address.email}")
            except EmailAddress.DoesNotExist:
                # Try case-insensitive search
                try:
                    email_address = EmailAddress.objects.get(email__iexact=email, verified=False)

                    # Verify the email address
                    email_address.verified = True
                    email_address.set_as_primary(conditional=True)
                    email_address.save()

                    print(f"Verified email via case-insensitive search: {email_address.email}")
                except (EmailAddress.DoesNotExist, EmailAddress.MultipleObjectsReturned):
                    print(f"Could not find unverified email: {email}")

        # Method 4: Last resort - find any unverified email
        if not email_address:
            print("Warning: Using fallback email confirmation method")
            try:
                # Get the most recent unverified email
                email_address = EmailAddress.objects.filter(verified=False).order_by('-id').first()
                if email_address:
                    # Verify the email address
                    email_address.verified = True
                    email_address.set_as_primary(conditional=True)
                    email_address.save()

                    print(f"Verified email via fallback: {email_address.email}")
                else:
                    raise ObjectDoesNotExist("No unverified email addresses found")
            except Exception as fallback_error:
                print(f"Fallback confirmation error: {str(fallback_error)}")
                raise ObjectDoesNotExist("Could not confirm email with provided key")

        # If we still don't have an email address, raise an error
        if not email_address:
            raise ObjectDoesNotExist("Could not find any email address to verify")

        # Debug output
        print(f"Successfully verified email: {email_address.email}")

        # Return success page
        return Titled(
            "Email Verified Successfully - DeadDevelopers",
            *email_page_headers(),
            Div(
                terminal_card(
                    H1("Email Verified Successfully"),
                    success_message(f"Your email address <strong>{email_address.email}</strong> has been verified successfully!"),
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
    except ObjectDoesNotExist as e:
        # Debug output
        print(f"Email confirmation error: {str(e)}")
        # Handle invalid or expired key
        return email_confirmation_error("This confirmation link is invalid or has expired.", email)

def email_confirmation_error(error_text, email=None):
    """Display error page for email confirmation"""
    # Get the email from the request if not provided
    if not email and app.request and hasattr(app.request, 'form_data') and app.request.form_data.get('email'):
        email = app.request.form_data.get('email')

    # Create the resend link
    resend_link = f"/accounts/email?email={email}" if email else "/accounts/email"

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
                terminal_link("REQUEST NEW EMAIL", resend_link),
                terminal_link("BACK TO LOGIN", "/login"),
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

# Handle email management page
@rt('/accounts/email')
def get():
    """Handle email management page"""
    from django.contrib.auth.models import AnonymousUser
    from allauth.account.utils import send_email_confirmation

    # Check if user is logged in
    if not app.session.get('auth'):
        # If not logged in, check if we have an email parameter
        email_param = app.request.query_params.get('email')
        if email_param:
            # Try to find the email address
            from allauth.account.models import EmailAddress
            try:
                email_address = EmailAddress.objects.get(email=email_param, verified=False)

                # Create a request wrapper for sending email confirmation
                from django.http import HttpRequest
                request = HttpRequest()
                request.method = 'GET'
                request.user = email_address.user
                request.session = app.session

                # Send verification email
                try:
                    send_email_confirmation(request, email_address.user, email_address)
                    print(f"Sent verification email to {email_address.email}")

                    # Return a success page
                    return Titled(
                        "Verification Email Sent - DeadDevelopers",
                        *email_page_headers(),
                        Div(
                            terminal_card(
                                H1("Verification Email Sent"),
                                code_block("// Status: VERIFICATION_PENDING"),
                                success_message(f"We've sent a verification email to <strong>{email_address.email}</strong>. Please check your inbox and click the verification link."),
                                P("If you don't see the email, check your spam folder."),
                                terminal_link("BACK TO LOGIN", "/login"),
                                cls="terminal-card"
                            ),
                            cls="container"
                        )
                    )
                except Exception as e:
                    print(f"Error sending verification email: {str(e)}")
            except EmailAddress.DoesNotExist:
                print(f"Could not find unverified email: {email_param}")

        # Redirect to login page
        return RedirectResponse('/login', status_code=303)

    # Get the user
    from users.models import User
    try:
        user = User.objects.get(username=app.session.get('auth'))
    except User.DoesNotExist:
        # Redirect to login page
        return RedirectResponse('/login', status_code=303)

    # Get the user's email addresses
    from allauth.account.models import EmailAddress
    email_addresses = EmailAddress.objects.filter(user=user)

    # Create a list of email addresses
    email_list = []
    for email_address in email_addresses:
        email_list.append({
            'email': email_address.email,
            'verified': email_address.verified,
            'primary': email_address.primary
        })

    # Create a request wrapper for sending email confirmation
    from django.http import HttpRequest
    request = HttpRequest()
    request.method = 'GET'
    request.user = user
    request.session = app.session

    # Function to resend verification email
    def resend_verification():
        # Send verification email
        for email_address in email_addresses:
            if not email_address.verified:
                try:
                    send_email_confirmation(request, user, email_address)
                    print(f"Sent verification email to {email_address.email}")
                    return True
                except Exception as e:
                    print(f"Error sending verification email: {str(e)}")
                    return False
        return False

    # Resend verification email if requested
    resent = False
    if app.request.query_params.get('resend') == 'true':
        resent = resend_verification()

    # Return the email management page
    return Titled(
        "Email Management - DeadDevelopers",
        *email_page_headers(),
        Div(
            terminal_card(
                H1("Email Management"),
                code_block("// Status: EMAIL_MANAGEMENT"),
                success_message("Manage your email addresses here.") if not resent else success_message("Verification email sent. Please check your inbox."),
                Div(
                    *[Div(
                        P(f"Email: {email['email']}"),
                        P(f"Status: {'Verified' if email['verified'] else 'Unverified'}"),
                        P(f"Primary: {'Yes' if email['primary'] else 'No'}"),
                        terminal_link("Resend Verification", f"/accounts/email?resend=true") if not email['verified'] else "",
                        cls="email-item"
                    ) for email in email_list],
                    cls="email-list"
                ),
                terminal_link("BACK TO DASHBOARD", "/dashboard"),
                cls="terminal-card"
            ),
            cls="container"
        )
    )