# Authentication System Testing Guide

This guide provides step-by-step instructions for manually testing the DeadDevelopers authentication system, including email verification and GitHub OAuth integration.

## Prerequisites

1. Make sure the development server is running: `python app.py`
2. Run migrations: `python run_migrations.py`
3. Configure GitHub OAuth (for OAuth testing):
   - Create a GitHub OAuth App at https://github.com/settings/developers
   - Set callback URL to `http://localhost:8000/accounts/github/login/callback/`
   - Add GitHub client ID and secret to environment variables:
     ```
     GITHUB_CLIENT_ID=your_client_id
     GITHUB_CLIENT_SECRET=your_client_secret
     ```

## Test 1: Basic Signup and Email Verification

### Steps:
1. Navigate to http://localhost:8000/signup
2. Fill out the signup form with:
   - Name: Test User
   - Username: testuser123
   - Email: your_real_email@example.com (use a real email for testing)
   - Password: testpass123
3. Click "Create Account"

### Expected Results:
- You should be redirected to the email verification sent page
- Check the console output for the verification email (in development mode)
- The email should contain a verification link
- Click the verification link
- You should see a confirmation page
- Click "Confirm"
- You should be redirected to the login page
- Log in with your email and password
- You should be redirected to the dashboard

### Success Criteria:
- User account is created
- Email verification email is sent
- Email verification link works
- User can log in after verification
- User is redirected to dashboard

### Failure Indicators:
- Error messages during signup
- No verification email in console
- Verification link doesn't work
- Unable to log in after verification

## Test 2: Login with Unverified Email

### Steps:
1. Create a new account but don't verify the email
2. Try to log in with the unverified email

### Expected Results:
- You should see an error message: "Email not verified"
- A new verification email should be sent automatically
- Check the console for the new verification email

### Success Criteria:
- Error message is displayed
- New verification email is sent

### Failure Indicators:
- No error message
- No new verification email
- User is allowed to log in without verification

## Test 3: GitHub OAuth Signup

### Steps:
1. Navigate to http://localhost:8000/signup
2. Click "Sign up with GitHub"
3. Authorize the application on GitHub
4. Complete the signup form if additional information is needed

### Expected Results:
- You should be redirected to GitHub for authorization
- After authorization, you might need to complete a profile form
- After completing the form, you should be redirected to the dashboard
- Your GitHub username should be automatically populated

### Success Criteria:
- GitHub authorization works
- User account is created with GitHub data
- User is redirected to dashboard
- GitHub username is saved in the user profile

### Failure Indicators:
- GitHub authorization fails
- Error messages during the process
- GitHub data not properly saved

## Test 4: GitHub OAuth Login

### Steps:
1. Log out if you're logged in
2. Navigate to http://localhost:8000/login
3. Click "Continue with GitHub"
4. Authorize the application on GitHub (if not already authorized)

### Expected Results:
- You should be redirected to GitHub for authorization (if not already authorized)
- After authorization, you should be redirected to the dashboard
- Your session should be properly set up

### Success Criteria:
- GitHub authorization works
- User is logged in
- User is redirected to dashboard
- Session data is properly set

### Failure Indicators:
- GitHub authorization fails
- Error messages during the process
- User not properly logged in

## Test 5: Password Reset

### Steps:
1. Navigate to http://localhost:8000/login
2. Click "Forgot Password?"
3. Enter your email address
4. Check the console for the password reset email
5. Click the reset link
6. Enter a new password
7. Log in with the new password

### Expected Results:
- Password reset email is sent
- Reset link works
- New password can be set
- User can log in with the new password

### Success Criteria:
- Password reset email is sent
- Reset link works
- New password is accepted
- User can log in with the new password

### Failure Indicators:
- No password reset email
- Reset link doesn't work
- Error when setting new password
- Unable to log in with new password

## Test 6: Session Management

### Steps:
1. Log in with a verified account
2. Navigate to different pages (dashboard, profile, etc.)
3. Check browser developer tools to inspect cookies and session data
4. Log out
5. Try to access protected pages

### Expected Results:
- Session is maintained across pages
- Session data includes user information
- After logout, session is cleared
- Protected pages redirect to login after logout

### Success Criteria:
- Session persists across pages
- Session contains correct user data
- Session is cleared on logout
- Protected pages are inaccessible after logout

### Failure Indicators:
- Session lost between pages
- Incorrect session data
- Session not cleared on logout
- Protected pages accessible after logout

## Test 7: Mobile Responsiveness

### Steps:
1. Open the browser's device emulation mode (or use a mobile device)
2. Navigate to the signup and login pages
3. Test the forms and buttons on different screen sizes

### Expected Results:
- Forms and buttons are properly sized and positioned
- All functionality works on mobile devices
- No horizontal scrolling required
- GitHub OAuth buttons are visible and functional

### Success Criteria:
- Pages look good on mobile devices
- All functionality works on mobile
- No layout issues

### Failure Indicators:
- Layout breaks on small screens
- Buttons or forms not properly sized
- Horizontal scrolling required
- Functionality doesn't work on mobile

## Automated Testing

Run the automated tests to verify the authentication system:

```
python run_tests.py
```

All tests should pass. If any test fails, check the error message for details on what went wrong.

## Reporting Issues

If you encounter any issues during testing, please document:

1. The test case that failed
2. Steps to reproduce the issue
3. Expected vs. actual behavior
4. Any error messages
5. Browser and device information

This will help us quickly identify and fix the issue.