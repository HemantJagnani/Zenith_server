# Running Flutter App on Your Physical Phone 📱

## For Android Phone

### Step 1: Enable Developer Options

1. **Open Settings** on your phone
2. Go to **About Phone**
3. Find **Build Number** (usually at the bottom)
4. **Tap Build Number 7 times** rapidly
5. You'll see a message: "You are now a developer!"

### Step 2: Enable USB Debugging

1. Go back to **Settings**
2. Find **Developer Options** (usually in System or Additional Settings)
3. Turn on **USB Debugging**
4. Turn on **Install via USB** (if available)

### Step 3: Connect Phone to Computer

1. **Connect your phone** to your computer using a USB cable
2. On your phone, you'll see a popup: **"Allow USB debugging?"**
3. Check **"Always allow from this computer"**
4. Tap **OK**

### Step 4: Verify Connection

Open PowerShell/Terminal and run:

```powershell
cd "C:\Users\Hemant Jagnani\OneDrive\Desktop\Zenith\frontend"
flutter devices
```

You should see your phone listed like:
```
Found 2 connected devices:
  SM G991B (mobile) • RFCR123ABC • android-arm64 • Android 13 (API 33)
  Windows (desktop) • windows • windows-x64 • Microsoft Windows
```

### Step 5: Run the App

```powershell
flutter run
```

Flutter will automatically detect your phone and ask:
```
[1]: SM G991B (RFCR123ABC)
[2]: Windows (windows)
Please choose one (or "q" to quit):
```

**Type `1` and press Enter**

The app will build and install on your phone!

---

## For iPhone (iOS)

### Requirements:
- Mac computer (required for iOS development)
- Apple Developer Account (free or paid)
- Xcode installed

### Steps:

1. **Connect iPhone** to Mac via USB
2. **Trust the computer** on iPhone when prompted
3. **Open Xcode** → Preferences → Accounts → Add Apple ID
4. **Run:**
   ```bash
   cd frontend
   flutter run
   ```

---

## Troubleshooting

### Phone Not Detected?

**Try these:**

1. **Use a different USB cable** (some cables are charge-only)
2. **Try different USB ports** on your computer
3. **Restart ADB:**
   ```powershell
   adb kill-server
   adb start-server
   flutter devices
   ```

4. **Check USB connection mode:**
   - On phone, pull down notification shade
   - Tap on "USB" notification
   - Select **"File Transfer"** or **"MTP"** mode

### "Unauthorized Device" Error?

1. **Disconnect and reconnect** the phone
2. The authorization popup should appear again
3. Tap **"Always allow"** and **OK**

### Build Failed?

1. **Make sure phone has enough storage** (at least 500MB free)
2. **Update phone to latest Android version**
3. **Try:**
   ```powershell
   flutter clean
   flutter pub get
   flutter run
   ```

---

## Quick Commands

### See Connected Devices
```powershell
flutter devices
```

### Run on Specific Device
```powershell
flutter run -d <device-id>
```

### Install Release Build (Faster)
```powershell
flutter run --release
```

### Hot Reload (While App is Running)
- Press **`r`** in terminal = Hot reload
- Press **`R`** in terminal = Hot restart
- Press **`q`** in terminal = Quit

---

## Wireless Debugging (Android 11+)

### Setup Once:

1. **Connect phone via USB** first
2. **Enable Wireless Debugging** in Developer Options
3. **Run:**
   ```powershell
   adb tcpip 5555
   ```

4. **Find phone's IP address:**
   - Settings → About Phone → Status → IP Address
   - Example: `192.168.1.100`

5. **Connect wirelessly:**
   ```powershell
   adb connect 192.168.1.100:5555
   ```

6. **Disconnect USB cable**

7. **Run app:**
   ```powershell
   flutter run
   ```

### Next Time:
Just run `adb connect <phone-ip>:5555` and then `flutter run`!

---

## Performance Tips

### For Faster Builds:

1. **Use Release Mode:**
   ```powershell
   flutter run --release
   ```
   - Faster performance
   - No hot reload
   - Optimized build

2. **Use Profile Mode:**
   ```powershell
   flutter run --profile
   ```
   - Good performance
   - Can measure performance
   - For testing

3. **Debug Mode** (default):
   ```powershell
   flutter run
   ```
   - Hot reload enabled
   - Slower performance
   - For development

---

## Building APK for Sharing

### Debug APK (Quick):
```powershell
flutter build apk --debug
```
APK location: `build/app/outputs/flutter-apk/app-debug.apk`

### Release APK (Optimized):
```powershell
flutter build apk --release
```
APK location: `build/app/outputs/flutter-apk/app-release.apk`

**Share this APK** with others to install on their phones!

---

## Your Next Steps

1. **Enable Developer Options** on your phone (tap Build Number 7 times)
2. **Enable USB Debugging** in Developer Options
3. **Connect phone** to computer via USB
4. **Allow USB debugging** when prompted
5. **Run:**
   ```powershell
   cd "C:\Users\Hemant Jagnani\OneDrive\Desktop\Zenith\frontend"
   flutter devices
   ```
6. **Verify** your phone appears in the list
7. **Run:**
   ```powershell
   flutter run
   ```
8. **Choose your phone** from the list
9. **Wait** for build to complete (first time takes 2-3 minutes)
10. **Enjoy** your app on your phone! 🎉

---

**Pro Tip:** Once installed, you can disconnect the USB cable and the app will stay on your phone. To update it, just connect and run `flutter run` again!
