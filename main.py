"""
Gemini Live API Voice Agent with Native Transcription
Using the official google-genai SDK for low-latency bidirectional audio streaming.
Uses Gemini's built-in transcription for both user and AI speech.
Features: Push-to-talk with SPACE key, real-time streaming, adjusted VAD sensitivity
"""

import asyncio
import os
import sys
from datetime import datetime
import json

import pyaudio
from google import genai
from dotenv import load_dotenv

# Try to import pynput for push-to-talk
try:
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("[Warning] pynput not installed. Run: pip install pynput")
    print("[Warning] Push-to-talk disabled. Using continuous listening mode.")

load_dotenv()

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SYSTEM_INSTRUCTION = os.getenv("SYSTEM_INSTRUCTION", "You are a helpful AI assistant.")

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

# Live API config - native audio model
MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"

# History file
HISTORY_FILE = "conversation_history.json"

# Initialize PyAudio
pya = pyaudio.PyAudio()

# Queues for audio streaming
audio_queue_output = asyncio.Queue()
audio_queue_mic = asyncio.Queue(maxsize=5)

# Global state
audio_stream = None
is_recording = False


def load_history() -> list:
    """Load conversation history from file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[History] Could not load history: {e}")
    return []


def save_history(history: list):
    """Save conversation history to file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"[History] Could not save history: {e}")


def build_system_prompt_with_history(base_instruction: str, history: list) -> str:
    """Build system prompt with conversation history included."""
    if not history:
        return base_instruction
    
    history_lines = ["\n\n--- Previous Conversation History ---"]
    for entry in history[-20:]:
        role = entry.get("role", "unknown")
        text = entry.get("text", "")
        if text:
            if role == "user":
                history_lines.append(f"User: {text}")
            else:
                history_lines.append(f"Assistant: {text}")
    history_lines.append("--- End of History ---\n")
    
    return base_instruction + "\n".join(history_lines)


def on_key_press(key):
    """Handle key press for push-to-talk."""
    global is_recording
    try:
        if key == keyboard.Key.space and not is_recording:
            is_recording = True
            print("\n[🎤 RECORDING]", end="", flush=True)
    except:
        pass


def on_key_release(key):
    """Handle key release for push-to-talk."""
    global is_recording
    try:
        if key == keyboard.Key.space and is_recording:
            is_recording = False
            print(" [✓ Done]")
    except:
        pass


async def listen_audio():
    """Listens for audio from microphone and streams it in real-time."""
    global audio_stream, is_recording
    
    mic_info = pya.get_default_input_device_info()
    audio_stream = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=SEND_SAMPLE_RATE,
        input=True,
        input_device_index=mic_info["index"],
        frames_per_buffer=CHUNK_SIZE,
    )
    
    kwargs = {"exception_on_overflow": False}
    
    while True:
        data = await asyncio.to_thread(audio_stream.read, CHUNK_SIZE, **kwargs)
        
        # Send audio in real-time while recording (or always if no pynput)
        if is_recording or not PYNPUT_AVAILABLE:
            await audio_queue_mic.put({"data": data, "mime_type": "audio/pcm"})


async def send_realtime(session):
    """Sends audio from the mic queue to the GenAI session in real-time."""
    while True:
        msg = await audio_queue_mic.get()
        await session.send_realtime_input(audio=msg)


async def receive_audio(session, history: list):
    """Receives responses from GenAI and puts audio data into the speaker audio queue."""
    current_user_text = ""
    current_model_text = ""
    
    while True:
        turn = session.receive()
        async for response in turn:
            if response.server_content:
                content = response.server_content
                
                # Handle USER transcript
                if hasattr(content, 'input_transcription') and content.input_transcription:
                    if hasattr(content.input_transcription, 'text'):
                        user_text = content.input_transcription.text
                        if user_text:
                            current_user_text += user_text
                
                # Handle MODEL audio
                if content.model_turn:
                    for part in content.model_turn.parts:
                        if part.inline_data and isinstance(part.inline_data.data, bytes):
                            audio_queue_output.put_nowait(part.inline_data.data)
                        if hasattr(part, 'text') and part.text:
                            current_model_text += part.text
                
                # Handle output transcription
                if hasattr(content, 'output_transcription') and content.output_transcription:
                    if hasattr(content.output_transcription, 'text'):
                        model_text = content.output_transcription.text
                        if model_text:
                            current_model_text += model_text
                
                # Handle turn completion
                if content.turn_complete:
                    if current_user_text.strip():
                        print(f"\n[You] {current_user_text.strip()}")
                        history.append({
                            "role": "user",
                            "text": current_user_text.strip(),
                            "timestamp": datetime.now().isoformat()
                        })
                        current_user_text = ""
                    
                    if current_model_text.strip():
                        # Filter internal thinking
                        clean_text = current_model_text.strip()
                        lines = clean_text.split('\n')
                        filtered_lines = [l for l in lines if not l.strip().startswith('**') and not l.strip().startswith('I have acknowledged')]
                        clean_text = ' '.join(filtered_lines).strip()
                        
                        if clean_text:
                            print(f"[Agent] {clean_text}")
                            history.append({
                                "role": "model",
                                "text": clean_text,
                                "timestamp": datetime.now().isoformat()
                            })
                        current_model_text = ""
                    
                    save_history(history)
                
                # Handle interruption
                if content.interrupted:
                    print("\n[Agent] *Interrupted*")
                    while not audio_queue_output.empty():
                        audio_queue_output.get_nowait()
                    current_model_text = ""


async def play_audio():
    """Plays audio from the speaker audio queue."""
    stream = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=RECEIVE_SAMPLE_RATE,
        output=True,
    )
    
    while True:
        bytestream = await audio_queue_output.get()
        await asyncio.to_thread(stream.write, bytestream)


async def run():
    """Main function to run the audio loop."""
    global is_recording
    
    if not GEMINI_API_KEY:
        print("[Error] GEMINI_API_KEY not found in .env file!")
        sys.exit(1)
    
    print("=" * 60)
    print("          Gemini Live Voice Agent")
    print("       with Reduced VAD Sensitivity")
    print("=" * 60)
    print(f"[Config] Model: {MODEL}")
    print()
    
    # Load history
    history = load_history()
    if history:
        print(f"[History] Loaded {len(history)} previous entries.")
    
    # Build system prompt
    full_system_prompt = build_system_prompt_with_history(SYSTEM_INSTRUCTION, history)
    
    # Initialize client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Config with native transcription
    config = {
        "response_modalities": ["AUDIO"],
        "system_instruction": full_system_prompt,
        "input_audio_transcription": {},
        "output_audio_transcription": {},
    }
    
    # Start keyboard listener
    keyboard_listener = None
    if PYNPUT_AVAILABLE:
        keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
        keyboard_listener.start()
        is_recording = False
    else:
        is_recording = True
    
    try:
        print("[Connection] Connecting to Gemini Live API...")
        async with client.aio.live.connect(model=MODEL, config=config) as live_session:
            print("[Connection] Connected successfully!")
            print()
            print("-" * 60)
            if PYNPUT_AVAILABLE:
                print("  PUSH-TO-TALK MODE:")
                print("  • Hold SPACE to talk (audio streams in real-time)")
                print("  • Release SPACE when done")
                print("  • Gemini waits 1.5 sec of silence before responding")
                print("  • Press Ctrl+C to exit")
            else:
                print("  CONTINUOUS MODE:")
                print("  • Speak into your microphone")
                print("  • Gemini waits for silence before responding")
                print("  • Press Ctrl+C to exit")
            print("-" * 60)
            print()
            print("Ready! Hold SPACE and speak..." if PYNPUT_AVAILABLE else "Ready!")
            print()
            
            async with asyncio.TaskGroup() as tg:
                tg.create_task(send_realtime(live_session))
                tg.create_task(listen_audio())
                tg.create_task(receive_audio(live_session, history))
                tg.create_task(play_audio())
                
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"\n[Error] {e}")
        import traceback
        traceback.print_exc()
    finally:
        if keyboard_listener:
            keyboard_listener.stop()
        if audio_stream:
            audio_stream.close()
        pya.terminate()
        save_history(history)
        print("\n[Main] Connection closed. Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n[Main] Interrupted by user.")
