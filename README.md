# VolumeSync 🔊

VolumeSync is a lightweight Windows utility that automatically synchronizes individual application volumes with the system's master volume. It runs in the system tray, providing a seamless and hands-off way to ensure all your apps stay at the same relative volume level as your hardware output.

## 🚀 Features

- **Automatic Sync:** Snaps application volumes to 100% relative to the master volume.
- **Sync Now:** Perform a one-time synchronization without running a continuous loop.
- **System Tray Integration:** Runs quietly in the background.
- **Visual Feedback:** The tray icon changes color based on the sync status (Blue = Enabled, Gray = Disabled).
- **Toggle Control:** Easily enable or disable synchronization via a right-click menu.
- **Low Resource Usage:** Minimal CPU and memory footprint.

## 🚀 Usage

1. **Start:** Run `VolumeSync.exe`. The icon will be **gray** (disabled) by default.
2. **Toggle:** Right-click the icon and click "Enabled" to start continuous synchronization. The icon will turn **blue**.
3. **One-time Sync:** Right-click the icon and select "Sync Now" to perform a single synchronization pass without enabling the continuous loop.
4. **Exit:** Right-click and select "Exit" to close the application.

## 🛠️ Installation

### Using the Executable (Recommended)
1. Download `VolumeSync.exe` from the [Releases](https://github.com/Wavewash/volumesync/releases) page (if available) or build it yourself.
2. Run the executable.
3. Look for the blue square icon in your system tray.

### Running from Source
If you prefer to run the Python script directly:
1. Clone the repository:
   ```bash
   git clone https://github.com/Wavewash/volumesync.git
   cd volumesync
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python syncvolume.py
   ```

## 🏗️ Building the Executable

To bundle the application into a standalone `.exe`:
1. Ensure you have installed the development dependencies:
   ```bash
   pip install pyinstaller
   ```
2. Run the build command:
   ```bash
   pyinstaller --onefile --noconsole --name VolumeSync syncvolume.py
   ```
3. The generated file will be in the `dist/` folder.

## 📝 Technical Details

- **Language:** Python 3.9+
- **APIs:** Windows Core Audio API (via `pycaw`)
- **System Tray:** `pystray`
- **Icon Generation:** `Pillow`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
