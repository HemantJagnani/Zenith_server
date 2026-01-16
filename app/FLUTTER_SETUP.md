# Flutter App Setup for Local Testing

## Step 1: Update Configuration

### 1.1 Find Your Computer's IP Address
```powershell
ipconfig
```
Look for **IPv4 Address** (e.g., `192.168.1.100`)

### 1.2 Update auth_service.dart
Open `C:\Zenith\app\lib\services\auth_service.dart`

**Line 9** - Replace with your IP:
```dart
static const String BASE_URL = 'http://YOUR_IP_HERE:8000';
```
Example:
```dart
static const String BASE_URL = 'http://192.168.1.100:8000';
```

**Line 13** - Replace with your Android Client ID from Google Cloud:
```dart
static const String GOOGLE_CLIENT_ID = 'YOUR_ANDROID_CLIENT_ID.apps.googleusercontent.com';
```

---

## Step 2: Add Dependencies

Update `C:\Zenith\app\pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  provider: ^6.1.1
  intl: ^0.18.1
  shared_preferences: ^2.2.2
  flutter_animate: ^4.5.0
  lottie: ^3.0.0
  confetti: ^0.7.0
  shimmer: ^3.0.0
  google_fonts: ^6.1.0
  fl_chart: ^0.66.0
  percent_indicator: ^4.2.3
  page_transition: ^2.1.0
  
  # NEW - Add these:
  google_sign_in: ^6.1.5
  http: ^1.1.0
```

Then run:
```bash
cd C:\Zenith\app
flutter pub get
```

---

## Step 3: Update main.dart

Update `C:\Zenith\app\lib\main.dart` to add login screen:

```dart
import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'screens/interview_screen.dart';
import 'screens/history_screen.dart';
import 'screens/analysis_screen.dart';
import 'services/auth_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mock Interview',
      theme: AppTheme.lightTheme,
      home: const AuthWrapper(),
      routes: {
        '/login': (context) => const LoginScreen(),
        '/home': (context) => const HomeScreen(),
        '/interview': (context) => const InterviewScreen(),
        '/history': (context) => const HistoryScreen(),
        '/analysis': (context) => const AnalysisScreen(),
      },
    );
  }
}

class AuthWrapper extends StatelessWidget {
  const AuthWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: AuthService().isLoggedIn(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }
        
        if (snapshot.data == true) {
          return const HomeScreen();
        }
        
        return const LoginScreen();
      },
    );
  }
}
```

---

## Step 4: Start Backend Server

```powershell
cd C:\Zenith\server
.\venv\Scripts\Activate.ps1
python api_main.py
```

Keep this running!

---

## Step 5: Connect Phone to Same WiFi

**IMPORTANT**: Your phone and computer must be on the **same WiFi network**!

---

## Step 6: Run Flutter App

```powershell
cd C:\Zenith\app
flutter run -d YOUR_DEVICE_ID
```

---

## Testing the Flow

1. **App opens** → Shows Login Screen
2. **Tap "Sign in with Google"** → Google Sign-In appears
3. **Sign in** → App sends token to backend
4. **Backend verifies** → Creates user in Supabase
5. **Backend returns JWT** → App stores it
6. **App navigates** → Home Screen

---

## Troubleshooting

### "Connection refused"
- Check backend is running (`python api_main.py`)
- Verify IP address in `auth_service.dart`
- Ensure phone and computer on same WiFi

### "Google Sign-In failed"
- Verify Android Client ID in `auth_service.dart`
- Check Google Cloud OAuth is configured
- Try signing out of Google on phone and retry

### "Backend authentication failed"
- Check backend logs for errors
- Verify `.env` has correct Google credentials
- Check Supabase connection string

---

## What's Next?

After login works:
1. Test saving interview results
2. Test viewing history
3. Deploy backend to Railway/Render
4. Update Flutter to use production URL

---

**You're ready to test!** 🚀
