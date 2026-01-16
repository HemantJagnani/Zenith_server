# Zenith Server Setup Guide

## Prerequisites

1. **Python 3.9+** installed
2. **Supabase account** (free tier)
3. **Google Cloud account** (for OAuth)

---

## Step 1: Supabase Setup (5 minutes)

### 1.1 Create Project
1. Go to https://supabase.com
2. Click "New Project"
3. Name: `zenith-mock-interview`
4. Set database password (save it!)
5. Wait for project to be ready

### 1.2 Run Database Schema
1. In Supabase dashboard → SQL Editor
2. Copy contents of `database_schema.sql`
3. Click "Run"
4. Verify tables created: `users`, `interviews`

### 1.3 Get Connection String
1. Settings → Database
2. Copy "Connection string" (URI format)
3. Replace `[YOUR-PASSWORD]` with your password
4. Save for `.env` file

---

## Step 2: Google OAuth Setup (10 minutes)

### 2.1 Create Google Cloud Project
1. Go to https://console.cloud.google.com
2. Create new project: "Zenith Mock Interview"

### 2.2 Enable Google+ API
1. APIs & Services → Library
2. Search "Google+ API"
3. Click "Enable"

### 2.3 Create OAuth Credentials

**For Android (Flutter app):**
1. APIs & Services → Credentials
2. Create OAuth 2.0 Client ID
3. Application type: **Android**
4. Package name: `com.zenith.mock_interview_app`
5. SHA-1: Get from Flutter (see Flutter setup)
6. Save **Client ID**

**For Web (Backend verification):**
1. Create another OAuth 2.0 Client ID
2. Application type: **Web application**
3. Save **Client ID** and **Client Secret**

---

## Step 3: Server Setup (5 minutes)

### 3.1 Install Dependencies

```bash
cd C:\Zenith\server

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3.2 Configure Environment

```bash
# Copy example env file
copy .env.example .env

# Edit .env file with your values
```

**Update `.env` with:**
```env
# From Supabase
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT.supabase.co:5432/postgres

# From Google Cloud (Web credentials)
GOOGLE_CLIENT_ID=your_web_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_web_client_secret

# Generate JWT secret
JWT_SECRET_KEY=run_this_command_openssl_rand_hex_32

# Keep these
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### 3.3 Generate JWT Secret

```bash
# Windows (PowerShell)
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})

# Or use online: https://generate-secret.vercel.app/32
```

---

## Step 4: Run Server

```bash
cd C:\Zenith\server

# Activate venv
.\venv\Scripts\Activate.ps1

# Run server
python api_main.py
```

**Server will start at:** http://localhost:8000

**Test it:**
- Open browser: http://localhost:8000
- Should see: `{"message": "Zenith Mock Interview API", "status": "running"}`

---

## Step 5: Test API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
Open: http://localhost:8000/docs

You'll see interactive API documentation (Swagger UI)

---

## API Endpoints

### Authentication
- `POST /auth/google` - Login with Google ID token
- `GET /auth/me` - Get current user info

### Interviews
- `POST /api/interviews` - Save interview result
- `GET /api/interviews` - Get user's interview history
- `GET /api/interviews/{id}` - Get specific interview
- `GET /api/stats` - Get user statistics

---

## Deployment (Later)

### Option 1: Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Option 2: Render
1. Connect GitHub repo
2. Select `server` folder
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn api_main:app --host 0.0.0.0 --port $PORT`

### Option 3: Google Cloud Run
```bash
gcloud run deploy zenith-api --source .
```

---

## Troubleshooting

### Database Connection Error
- Check Supabase is running
- Verify DATABASE_URL in `.env`
- Check password is correct

### Google OAuth Error
- Verify Client ID/Secret in `.env`
- Check OAuth consent screen is configured
- Ensure Google+ API is enabled

### Import Errors
- Activate virtual environment
- Run `pip install -r requirements.txt`

---

## Next Steps

1. ✅ Server running locally
2. → Set up Flutter app (see `app/` folder)
3. → Test OAuth flow
4. → Deploy to production

---

**Server is ready!** 🚀

Now configure the Flutter app to connect to this server.
