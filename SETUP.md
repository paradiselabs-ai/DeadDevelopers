# DeadDevelopers Setup Guide

This guide will help you get the DeadDevelopers platform up and running locally or deploy it to production.

## Prerequisites

- Python 3.11+
- PostgreSQL (for production) or SQLite (for local development)
- Redis (optional, for caching and WebSockets in production)
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/paradiselabs-ai/DeadDevelopers.git
cd DeadDevelopers
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

**Minimum required configuration for local development:**

```env
# Generate a secret key with: python -c "import secrets; print(secrets.token_urlsafe(50))"
SECRET_KEY=your-generated-secret-key-here
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (for development, use console backend)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**For production, you'll also need:**

```env
# Production settings
DJANGO_DEBUG=False
ALLOWED_HOSTS=yourdomain.com,.vercel.app

# Database
POSTGRES_URL=postgresql://user:password@host:port/database

# Email (SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@deaddevelopers.com

# Redis/Cache (Vercel KV or your Redis instance)
KV_URL=redis://your-redis-url

# OAuth (optional)
GITHUB_CLIENT_ID=your-github-oauth-client-id
GITHUB_CLIENT_SECRET=your-github-oauth-client-secret
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Start the Development Server

**Option A: Using the startup script (recommended)**

```bash
./start_dev.sh
```

**Option B: Manual start**

```bash
python main.py
```

The server will be available at `http://localhost:8000`

## Production Deployment (Vercel)

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Set Up Vercel Project

```bash
vercel login
vercel link
```

### 3. Configure Environment Variables

Set all production environment variables in the Vercel dashboard or via CLI:

```bash
vercel env add SECRET_KEY
vercel env add POSTGRES_URL
vercel env add EMAIL_HOST_USER
# ... add all other required variables
```

### 4. Deploy

```bash
vercel --prod
```

## Key Features Implemented

### Phase 1: Critical Fixes & Security

- ✅ **Unified Session Management**: AuthBridge synchronizes FastHTML and Django sessions
- ✅ **CSRF Protection**: All forms include CSRF tokens
- ✅ **Rate Limiting**: Login and signup endpoints are protected from brute-force attacks
- ✅ **Email Verification**: SMTP configuration for account verification emails
- ✅ **Security Hardening**: No hardcoded secrets, proper DEBUG and ALLOWED_HOSTS configuration
- ✅ **Logging**: Comprehensive logging for debugging and monitoring
- ✅ **WebSocket Support**: Channels configured for real-time chat
- ✅ **Migration Checks**: Automatic verification that database migrations are applied

### Phase 2: Code Quality

- ✅ **Refactored Feed System**: Eliminated duplicate code in scrolling feeds
- ✅ **Helper Modules**: Created reusable utilities for common tasks
- ✅ **Development Tools**: Added startup script for easier local development

## Common Issues

### "SECRET_KEY environment variable must be set"

Make sure you've created a `.env` file and set the `SECRET_KEY` variable. Generate one with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Database Migration Errors

If you see migration errors on startup, run:

```bash
python manage.py migrate
```

Or skip the migration check temporarily:

```bash
SKIP_MIGRATION_CHECK=1 python main.py
```

### Email Verification Not Working

For local development, set `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` in your `.env` file. Verification emails will be printed to the console instead of sent via SMTP.

For production, configure proper SMTP settings with a real email service.

### WebSocket/Chat Not Working

Ensure Redis is configured (via `KV_URL` environment variable) for production. For local development, the in-memory channel layer will be used automatically.

## Architecture Overview

**Stack:**
- **Frontend**: FastHTML (Python-based HTML generation)
- **Backend**: Django (ORM, authentication, admin)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Cache/WebSockets**: Redis (via Channels)
- **Hosting**: Vercel

**Key Components:**
- `app.py`: FastHTML application initialization and auth middleware
- `auth_bridge.py`: Unified authentication layer between FastHTML and Django
- `routes/`: FastHTML route handlers
- `django_config/`: Django settings and configuration
- `chat/`: WebSocket consumers for real-time chat
- `users/`: Custom user model

## Contributing

Please read the main README.md for contribution guidelines.

## License

See LICENSE file for details.
