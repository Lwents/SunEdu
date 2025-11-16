# Environment Configuration Guide

## ⚠️ IMPORTANT: Security Best Practices

**NEVER commit `.env` files with sensitive data to Git!**

All production environment variables should be managed through **GitHub Secrets**.

## Setup Instructions

### Local Development

1. Copy the local environment template:
```bash
cp .env.local.example .env.local
```

2. Update `.env.local` with your local settings

### Production Deployment

Production environment variables are managed via GitHub Secrets:

1. Go to: https://github.com/Lwents/SunEdu/settings/secrets/actions

2. Update the `BACKEND_ENV_FILE` secret with the full `.env` content

3. Required variables:
   - `SECRET_KEY` - Django secret key
   - `DEBUG=False`
   - Database credentials (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`)
   - `ALLOWED_HOSTS` - Comma-separated list of domains
   - `CSRF_TRUSTED_ORIGINS` - Comma-separated HTTPS URLs
   - `CORS_ALLOWED_ORIGINS` - Comma-separated HTTPS URLs
   - `FRONTEND_URL` - Frontend domain URL
   - Email settings (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`)
   - Payment gateway credentials (if needed)

4. Deploy will automatically use the secret to create `.env` on server

## Email Configuration

For production email sending:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=your-smtp-server.com
EMAIL_PORT=465
EMAIL_USE_TLS=false
EMAIL_USE_SSL=true
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-password-here
DEFAULT_FROM_EMAIL=YourApp <your-email@domain.com>
```

## Security Notes

- ✅ Use GitHub Secrets for production
- ✅ Use strong, randomly generated SECRET_KEY
- ✅ Use strong database passwords
- ✅ Keep `.env` files in `.gitignore`
- ❌ Never commit sensitive data to repository
- ❌ Never share credentials in public channels
