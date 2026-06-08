# Deploy FocusAI to Render

Complete guide to deploy your FocusAI Pomodoro app to Render.

## Prerequisites

1. GitHub account with your code pushed
2. Render account (free tier works)
3. OpenAI API key (or Hugging Face API key)

## Step 1: Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **PostgreSQL**
3. Configure:
   - **Name**: `focusai-db`
   - **Database**: `focusai`
   - **User**: (auto-generated)
   - **Region**: Choose closest to you
   - **Plan**: Free
4. Click **Create Database**
5. **Important**: Copy the **Internal Database URL** (starts with `postgresql://`)

## Step 2: Create Web Service on Render

1. Click **New +** → **Web Service**
2. Connect your GitHub repository: `https://github.com/Dhivakar49/pomodoro`
3. Configure:

### Basic Settings
- **Name**: `focusai-pomodoro`
- **Region**: Same as database
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn backend.wsgi:application`

### Advanced Settings - Environment Variables

Click **Add Environment Variable** for each:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate a new secret key* |
| `DATABASE_URL` | Paste the Internal Database URL from Step 1 |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `AI_PROVIDER` | `openai` |

*Generate secret key with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Plan
- Select **Free** tier

4. Click **Create Web Service**

## Step 3: Wait for Deployment

- First deployment takes 5-10 minutes
- Watch the logs for any errors
- Once you see "Starting gunicorn", your app is live!

## Step 4: Access Your App

Your app will be available at:
```
https://focusai-pomodoro.onrender.com
```

## Step 5: Update ALLOWED_HOSTS (Optional but Recommended)

After deployment, update `backend/settings.py`:

```python
ALLOWED_HOSTS = ["focusai-pomodoro.onrender.com", "127.0.0.1", "localhost"]
```

Then commit and push:
```bash
git add backend/settings.py
git commit -m "Update ALLOWED_HOSTS for production"
git push origin main
```

Render will auto-redeploy.

## Troubleshooting

### Database Connection Errors
- Verify `DATABASE_URL` is correctly set
- Make sure it's the **Internal** URL, not External

### Static Files Not Loading
- Check build logs for `collectstatic` errors
- Verify `STATIC_ROOT` is set in settings.py

### 502 Bad Gateway
- Check application logs in Render dashboard
- Verify gunicorn command is correct
- Ensure all dependencies in requirements.txt

### Application Errors
- Set `DEBUG=True` temporarily to see detailed errors
- Check logs in Render dashboard
- Remember to set `DEBUG=False` after debugging

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DEBUG` | Yes | Set to `False` for production |
| `SECRET_KEY` | Yes | Django secret key (keep secret!) |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `OPENAI_API_KEY` | No | For AI summarization & quiz features |
| `AI_PROVIDER` | No | `openai` or `huggingface` |
| `HF_API_KEY` | No | Hugging Face API key (alternative to OpenAI) |

## Free Tier Limitations

- Database: 1GB storage, 97 hours/month uptime
- Web Service: 750 hours/month, spins down after 15min inactivity
- First request after spin-down takes ~30 seconds

## Post-Deployment

1. Create a superuser:
   - Go to Render Shell (from your service dashboard)
   - Run: `python manage.py createsuperuser`
   
2. Access admin panel:
   - Visit: `https://focusai-pomodoro.onrender.com/admin`

## Support

For issues, check:
- [Render Docs](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

## Note About OCR/Pytesseract

This app uses `pytesseract` for OCR. If you experience issues:

1. Add a `render.yaml` file to install Tesseract:

```yaml
services:
  - type: web
    name: focusai-pomodoro
    env: python
    buildCommand: |
      apt-get update
      apt-get install -y tesseract-ocr
      ./build.sh
    startCommand: gunicorn backend.wsgi:application
```

2. Or remove pytesseract dependency if not needed for your use case
