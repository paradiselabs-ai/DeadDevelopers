# Google Cloud Storage Setup for DeadDevelopers

This guide explains how to set up Google Cloud Storage for user-uploaded media files (avatars, portfolio images).

## Why Google Cloud Storage?

- **Scalable**: Handles unlimited file uploads without server storage limits
- **Fast**: Global CDN for fast image delivery
- **Cost-effective**: Pay only for what you use (~$0.02/GB/month)
- **Reliable**: 99.95% uptime SLA

## Prerequisites

- Google Cloud Platform account
- $300 free credits (available for new users)
- GCP project created

## Setup Steps

### 1. Create a GCS Bucket

```bash
# Install gcloud CLI if not already installed
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Create a bucket (choose a globally unique name)
gsutil mb -p YOUR_PROJECT_ID -c STANDARD -l us-central1 gs://deaddevelopers-media/

# Make the bucket publicly readable
gsutil iam ch allUsers:objectViewer gs://deaddevelopers-media/
```

### 2. Create a Service Account

```bash
# Create service account
gcloud iam service-accounts create deaddevelopers-storage \
    --display-name="DeadDevelopers Storage Service Account"

# Grant Storage Object Admin role
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:deaddevelopers-storage@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

# Create and download key
gcloud iam service-accounts keys create ~/deaddevelopers-gcs-key.json \
    --iam-account=deaddevelopers-storage@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 3. Configure Environment Variables

Add to your `.env` file (or Vercel environment variables):

```bash
GCS_BUCKET_NAME=deaddevelopers-media
GCS_PROJECT_ID=YOUR_PROJECT_ID
GCS_CREDENTIALS_PATH=/path/to/deaddevelopers-gcs-key.json
```

**For Vercel deployment:**

1. Go to your Vercel project settings
2. Navigate to Environment Variables
3. Add the three variables above
4. For `GCS_CREDENTIALS_PATH`, you can either:
   - Upload the JSON key file to Vercel and reference its path
   - Or set `GOOGLE_APPLICATION_CREDENTIALS` with the full JSON content

### 4. Test the Setup

```bash
# Install dependencies
pip install django-storages[google] google-cloud-storage

# Run Django shell
python manage.py shell

# Test upload
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User

user = User.objects.first()
user.avatar = SimpleUploadedFile("test.jpg", b"test content", content_type="image/jpeg")
user.save()

print(user.avatar.url)  # Should print GCS URL
```

## Cost Estimation

Based on typical usage:

| Resource | Usage | Cost/Month |
|----------|-------|------------|
| Storage (10GB) | User avatars & images | $0.20 |
| Network egress (50GB) | Image downloads | $5.00 |
| Operations (100K) | Uploads/downloads | $0.05 |
| **Total** | | **~$5.25/month** |

With $300 GCP credits, this gives you **57+ months** of free storage!

## Fallback to Local Storage

If GCS is not configured (missing environment variables), the system automatically falls back to local file storage in the `media/` directory. This is perfect for development.

## Security Best Practices

1. **Never commit** the service account JSON key to Git
2. Add `*.json` to `.gitignore`
3. Use separate service accounts for dev/staging/production
4. Rotate service account keys every 90 days
5. Set bucket lifecycle rules to delete old files

## Troubleshooting

### "Permission denied" errors

- Verify service account has `Storage Object Admin` role
- Check that bucket name matches environment variable
- Ensure JSON key file path is correct

### Images not loading

- Verify bucket has `allUsers:objectViewer` permission
- Check CORS settings if accessing from different domain
- Inspect browser network tab for 403/404 errors

### Slow uploads

- Consider using Cloud CDN for faster delivery
- Enable compression for image files
- Use signed URLs for temporary access

## Alternative: Vercel Blob Storage

If you prefer to stay within the Vercel ecosystem, you can use **Vercel Blob** instead:

```bash
# Install Vercel Blob SDK
npm install @vercel/blob

# Set environment variable
BLOB_READ_WRITE_TOKEN=your-vercel-blob-token
```

However, GCS is recommended for:
- Better pricing at scale
- More control over storage
- Existing GCP credits
