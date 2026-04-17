# VolumeSync

A utility to synchronize Windows application volumes with the system master volume. It runs in the system tray and allows users to toggle synchronization.

## Project Goal
Ensure that all applications in the Windows Volume Mixer are synchronized with the master volume level (100% relative volume).

## Features
- **System Tray Icon:** Runs in the background without a console window.
- **Toggle Enabled:** Right-click the tray icon to enable or disable continuous synchronization (default: disabled).
- **Sync Now:** A menu option for a one-time synchronization pass.
- **Visual Feedback:** The icon changes color (Blue = Enabled, Gray = Disabled).
- **Standalone EXE:** Can be built into a single executable file for easy distribution.

## Technical Details
- **Language:** Python 3.9
- **Key Libraries:** 
    - `pycaw`: Windows Core Audio API wrapper.
    - `pystray`: System tray icon and menu.
    - `Pillow`: Image generation for the tray icon.
    - `pyinstaller`: Executable bundling.

## Development & Build
1. **Setup Environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install pycaw pystray Pillow pyinstaller
   ```

2. **Run Script (for testing):**
   ```bash
   python syncvolume.py
   ```

3. **Build Executable:**
   Run the following command to generate `dist/VolumeSync.exe`:
   ```bash
   .\venv\Scripts\pyinstaller.exe --onefile --noconsole --name VolumeSync syncvolume.py
   ```

## Usage
- **Start:** Run `VolumeSync.exe`.
- **Toggle:** Right-click the blue square in the system tray and click "Enabled".
- **Exit:** Right-click and select "Exit".
