# DeadDevelopers Deployment Guide

This guide covers deploying DeadDevelopers to production on Vercel.

## Pre-Deployment Checklist

### 1. Environment Variables

Ensure all required environment variables are set in your Vercel project:

**Required:**
- ✅ `SECRET_KEY` - Django secret key (generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
- ✅ `DJANGO_DEBUG` - Set to `False` for production
- ✅ `ALLOWED_HOSTS` - Comma-separated list of allowed domains (e.g., `yourdomain.com,.vercel.app`)
- ✅ `POSTGRES_URL` - Vercel Postgres connection string
- ✅ `EMAIL_HOST` - SMTP server hostname
- ✅ `EMAIL_PORT` - SMTP port (usually 587 for TLS)
- ✅ `EMAIL_USE_TLS` - Set to `True`
- ✅ `EMAIL_HOST_USER` - SMTP username/email
- ✅ `EMAIL_HOST_PASSWORD` - SMTP password or app-specific password
- ✅ `DEFAULT_FROM_EMAIL` - Email address to send from

**Optional but Recommended:**
- `KV_URL` - Vercel KV (Redis) URL for caching and WebSocket support
- `GITHUB_CLIENT_ID` - GitHub OAuth client ID
- `GITHUB_CLIENT_SECRET` - GitHub OAuth client secret
- `GITLAB_CLIENT_ID` - GitLab OAuth client ID
- `GITLAB_CLIENT_SECRET` - GitLab OAuth client secret

### 2. Database Setup

1. **Create Vercel Postgres Database:**
   ```bash
   vercel postgres create
   ```

2. **Link to your project:**
   ```bash
   vercel postgres link
   ```

3. **Run migrations:**
   ```bash
   # After first deployment, run migrations via Vercel CLI
   vercel env pull .env.local
   python manage.py migrate
   ```

### 3. Redis/Cache Setup (Optional but Recommended)

1. **Create Vercel KV store:**
   ```bash
   vercel kv create
   ```

2. **Link to your project:**
   ```bash
   vercel kv link
   ```

### 4. Email Configuration

For production email sending, you'll need an SMTP service. Options include:

- **Gmail** (with app-specific password)
- **SendGrid**
- **Mailgun**
- **AWS SES**

**Gmail Example:**
1. Enable 2-factor authentication on your Google account
2. Generate an app-specific password
3. Set environment variables:
   ```
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-specific-password
   ```

### 5. OAuth Setup (Optional)

**GitHub OAuth:**
1. Go to GitHub Settings > Developer settings > OAuth Apps
2. Create a new OAuth App
3. Set Authorization callback URL to: `https://yourdomain.com/accounts/github/login/callback/`
4. Add client ID and secret to Vercel environment variables

**GitLab OAuth:**
1. Go to GitLab Settings > Applications
2. Create a new application
3. Set Redirect URI to: `https://yourdomain.com/accounts/gitlab/login/callback/`
4. Add client ID and secret to Vercel environment variables

## Deployment Steps

### Initial Deployment

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Link your project:**
   ```bash
   vercel link
   ```

4. **Set environment variables:**
   ```bash
   # Set all required variables
   vercel env add SECRET_KEY production
   vercel env add DJANGO_DEBUG production
   vercel env add ALLOWED_HOSTS production
   # ... continue for all variables
   ```

5. **Deploy to production:**
   ```bash
   vercel --prod
   ```

### Post-Deployment Tasks

1. **Run database migrations:**
   ```bash
   # Pull environment variables locally
   vercel env pull .env.local
   
   # Run migrations
   python manage.py migrate
   ```

2. **Create superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

3. **Collect static files (if needed):**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Test the deployment:**
   - Visit your production URL
   - Test user registration and email verification
   - Test login/logout functionality
   - Test WebSocket chat (if Redis is configured)
   - Check admin panel at `/admin`

## Continuous Deployment

Vercel automatically deploys when you push to your main branch. To set this up:

1. **Connect your GitHub repository** in the Vercel dashboard
2. **Configure build settings:**
   - Build Command: (leave empty, Vercel auto-detects)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`

3. **Enable automatic deployments** for your main branch

## Monitoring and Maintenance

### Logs

View application logs in the Vercel dashboard or via CLI:

```bash
vercel logs
```

### Database Backups

Vercel Postgres automatically creates backups. You can also create manual backups:

```bash
# Export database
vercel postgres dump > backup.sql

# Restore database
vercel postgres restore < backup.sql
```

### Performance Monitoring

Monitor your application's performance in the Vercel dashboard:
- Response times
- Error rates
- Traffic patterns
- Resource usage

## Troubleshooting

### Common Issues

**1. "SECRET_KEY environment variable must be set"**
- Ensure `SECRET_KEY` is set in Vercel environment variables
- Check that it's set for the production environment

**2. "DisallowedHost" error**
- Add your domain to `ALLOWED_HOSTS` environment variable
- Include both your custom domain and `.vercel.app` domain

**3. Email not sending**
- Verify SMTP credentials are correct
- Check that `EMAIL_BACKEND` is set to `django.core.mail.backends.smtp.EmailBackend`
- Test SMTP connection manually

**4. WebSocket/Chat not working**
- Ensure `KV_URL` is set and Redis is properly configured
- Check that `channels` and `channels-redis` are in requirements.txt
- Verify ASGI configuration in `django_config/asgi.py`

**5. Static files not loading**
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Verify Vercel is serving static files correctly

### Health Check

Create a simple health check endpoint to verify deployment:

```python
@rt('/health')
def health_check():
    return {"status": "ok", "version": "1.0.0"}
```

Test it:
```bash
curl https://yourdomain.com/health
```

## Rollback

If something goes wrong, you can rollback to a previous deployment:

1. **Via Vercel Dashboard:**
   - Go to Deployments
   - Find the working deployment
   - Click "Promote to Production"

2. **Via CLI:**
   ```bash
   vercel rollback
   ```

## Security Best Practices

- ✅ Never commit `.env` files to Git
- ✅ Use strong, unique `SECRET_KEY`
- ✅ Keep `DJANGO_DEBUG=False` in production
- ✅ Use HTTPS only (Vercel provides this automatically)
- ✅ Regularly update dependencies
- ✅ Monitor logs for suspicious activity
- ✅ Use rate limiting on sensitive endpoints
- ✅ Enable CSRF protection on all forms
- ✅ Use secure session cookies

## Support

For issues specific to:
- **Vercel**: Check [Vercel Documentation](https://vercel.com/docs)
- **Django**: Check [Django Documentation](https://docs.djangoproject.com/)
- **DeadDevelopers**: Open an issue on GitHub

## Next Steps

After successful deployment:
1. Set up custom domain (if not already done)
2. Configure DNS settings
3. Enable SSL/TLS (automatic with Vercel)
4. Set up monitoring and alerting
5. Create a backup strategy
6. Document your deployment process
