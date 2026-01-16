# Mock Interview App - Flutter Frontend

A modern Flutter mobile application for conducting AI-powered mock interviews.

## Features

- **Home Screen**: Welcome page with quick stats and navigation
- **Interview Screen**: Real-time interview with push-to-talk functionality
- **History Screen**: View past interviews with scores and details
- **Analysis Screen**: Detailed performance analysis with strengths, weaknesses, and suggestions

## Getting Started

### Prerequisites

- Flutter SDK (>=3.0.0)
- Dart SDK
- Android Studio / VS Code with Flutter extensions
- Android Emulator or iOS Simulator

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   flutter pub get
   ```

3. Run the app:
   ```bash
   flutter run
   ```

## Project Structure

```
lib/
├── main.dart                    # App entry point
├── theme/
│   └── app_theme.dart          # App theming
├── models/
│   ├── message.dart            # Message data model
│   └── interview.dart          # Interview data model
└── screens/
    ├── home_screen.dart        # Landing page
    ├── interview_screen.dart   # Interview interface
    ├── history_screen.dart     # Past interviews
    └── analysis_screen.dart    # Performance analysis
```

## Current Status

✅ **Implemented:**
- Complete UI for all 4 main screens
- Navigation between screens
- Mock data for demonstration
- Material Design 3 theming
- Responsive layouts

🔄 **Coming Next:**
- Backend API integration (FastAPI)
- Real audio recording
- Actual interview analysis with Gemini API
- User authentication
- Local data persistence

## Design

- **Color Scheme**: Professional blue and teal
- **Typography**: Clean and readable
- **UI Style**: Material Design 3 with custom touches

## Testing

Run the app on an emulator or physical device:

```bash
flutter run
```

For hot reload during development, press `r` in the terminal.

## Notes

- Currently uses mock data for demonstration
- Backend integration will be added in Phase 4
- Audio recording will integrate with Python backend via API

---

**Built with Flutter** 💙
