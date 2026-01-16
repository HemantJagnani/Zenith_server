# Zenith - AI Mock Interview Platform

AI-powered mock interview application with voice interaction and performance analysis.

## Project Structure

```
C:\Zenith\
├── server/          # Backend (Python + Gemini API)
│   ├── main.py
│   ├── .env
│   ├── venv/
│   └── requirements.txt
│
└── app/             # Frontend (Flutter mobile app)
    ├── lib/
    ├── android/
    └── pubspec.yaml
```

## Server (Backend)

**Location**: `C:\Zenith\server`

Python backend with Gemini Live API for voice interviews.

**Run:**
```bash
cd server
.\venv\Scripts\Activate.ps1
python main.py
```

**Deploy to**: Cloudflare Workers / Google Cloud Run

## App (Frontend)

**Location**: `C:\Zenith\app`

Flutter mobile app with Duolingo + YouTube inspired design.

**Run:**
```bash
cd app
flutter run -d <device-id>
```

**Deploy to**: Google Play Store / Apple App Store

## Quick Start

### Server
```bash
cd C:\Zenith\server
.\venv\Scripts\Activate.ps1
python main.py
```

### App
```bash
cd C:\Zenith\app
flutter run
```

## Tech Stack

- **Backend**: Python, Gemini API, FastAPI (future)
- **Frontend**: Flutter, Dart, Material Design 3
- **Database**: PostgreSQL (future)
- **Hosting**: Cloudflare Workers, Google Play Store

## Features

- 🎤 Voice-based mock interviews
- 🤖 AI-powered interviewer (Gemini)
- 📊 Performance analysis & scoring
- 🔥 Gamification (streaks, levels, XP)
- 📱 Modern mobile UI
- 📈 Progress tracking

---

**Created**: January 2026
