# 🎯 Zenith - Gemini Live Voice Agent

## ✅ Ready to Use!

This is a **fully working** Gemini Live voice agent with:
- ✅ **Push-to-talk** (hold SPACE to speak)
- ✅ **Real-time audio streaming**
- ✅ **Automatic transcription** (both you and AI)
- ✅ **Conversation history** (saved to `conversation_history.json`)
- ✅ **Native audio model** (`gemini-2.5-flash-native-audio-preview`)

## 🚀 How to Run

### Step 1: Activate Virtual Environment
```powershell
cd "C:\Users\Hemant Jagnani\OneDrive\Desktop\Zenith-new"
.\venv\Scripts\Activate.ps1
```

### Step 2: Run the Voice Agent
```powershell
python main.py
```

### Step 3: Talk!
- **Hold SPACE** to speak
- **Release SPACE** when done
- Gemini waits ~1.5 seconds of silence before responding
- Press **Ctrl+C** to exit

## 📝 Features

### Push-to-Talk Mode
- Hold SPACE key to record your voice
- Audio streams in real-time to Gemini
- Release when you're done speaking
- Gemini processes and responds

### Automatic Transcription
- Your speech is transcribed automatically
- AI's responses are transcribed
- Everything displayed in terminal
- Full conversation saved to `conversation_history.json`

### Conversation History
- Previous conversations are loaded on startup
- AI remembers context from past sessions
- History file: `conversation_history.json`

## ⚙️ Configuration

Edit `.env` file to customize:
```env
GEMINI_API_KEY="your_api_key_here"
SYSTEM_INSTRUCTION="You are a helpful AI assistant."
```

Change the system instruction to customize AI behavior:
- "You are a professional interviewer..."
- "You are a coding tutor..."
- "You are a language teacher..."

## 📊 What You'll See

```
============================================================
          Gemini Live Voice Agent
       with Reduced VAD Sensitivity
============================================================
[Config] Model: gemini-2.5-flash-native-audio-preview-12-2025

[History] Loaded 10 previous entries.
[Connection] Connecting to Gemini Live API...
[Connection] Connected successfully!

------------------------------------------------------------
  PUSH-TO-TALK MODE:
  • Hold SPACE to talk (audio streams in real-time)
  • Release SPACE when done
  • Gemini waits 1.5 sec of silence before responding
  • Press Ctrl+C to exit
------------------------------------------------------------

Ready! Hold SPACE and speak...

[🎤 RECORDING] [✓ Done]
[You] Hello, how are you today?
[Agent] I'm doing well, thank you for asking! How can I help you?
```

## 🔧 Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure `.env` file exists
- Check that API key is properly set

### "pynput not installed"
- Run: `pip install pynput`
- Or it will fall back to continuous listening mode

### Microphone not working
- Check Windows microphone permissions
- Make sure default input device is set correctly

### API Quota Error
- This uses the newer `gemini-2.5-flash-native-audio-preview` model
- May still require billing for Live API
- Check: https://console.cloud.google.com/billing

## 📁 Files

- `main.py` - Main voice agent script
- `.env` - Configuration (API key, system instruction)
- `conversation_history.json` - Saved conversations
- `requirements.txt` - Python dependencies
- `venv/` - Virtual environment

## 🎓 Next Steps

Once this works, you can:
1. **Add PostgreSQL** - Save conversations to database
2. **Performance Analysis** - Use Gemini to analyze interview transcripts
3. **FastAPI Backend** - Create REST API for Flutter app
4. **Flutter Frontend** - Build mobile app UI

---

**Ready to test? Run `python main.py` and hold SPACE to speak!**