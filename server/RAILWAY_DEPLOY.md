# Railway Deployment Guide

## Quick Deploy Steps

### 1. Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Verify email

### 2. Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your GitHub account
4. Select the Zenith repository
5. Choose the `server` folder as root directory

### 3. Add Environment Variables
In Railway dashboard, go to Variables tab and add:

```
DATABASE_URL=your_supabase_connection_string
GOOGLE_CLIENT_ID=47229444672-ricp7gavae72...
GOOGLE_CLIENT_SECRET=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
JWT_SECRET_KEY=d5M8znN4QHy0kep9Z7G2ilJvWSVY1POA
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
HOST=0.0.0.0
DEBUG=False
CORS_ORIGINS=*
```

### 4. Deploy
1. Railway will automatically deploy
2. Wait for build to complete (~2-3 minutes)
3. Get your deployment URL (e.g., `https://zenith-production.up.railway.app`)

### 5. Update Flutter App
Update `C:\Zenith\app\lib\services\auth_service.dart`:

```dart
static const String BASE_URL = 'https://YOUR-RAILWAY-URL';
```

### 6. Update Google OAuth
1. Go to Google Cloud Console
2. Add Railway URL to authorized redirect URIs:
   - `https://YOUR-RAILWAY-URL/auth/google`

### 7. Test
1. Rebuild Flutter app
2. Try logging in
3. Should work!

## Troubleshooting

### Build Fails
- Check Railway logs
- Verify `requirements.txt` is correct
- Ensure Python version matches

### App Crashes
- Check environment variables are set
- Verify Supabase connection string
- Check Railway logs for errors

### OAuth Fails
- Verify Google OAuth redirect URIs
- Check CORS_ORIGINS includes your app
- Verify Google Client ID/Secret

## Cost
- Free $5 credit per month
- Should be enough for development
- ~$5-10/month for production

## Next Steps
1. Set up custom domain (optional)
2. Enable auto-deploy on push
3. Set up monitoring
4. Add health checks
