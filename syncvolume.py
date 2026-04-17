import time
import threading
import logging
import os
import sys
import ctypes
import comtypes
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from pycaw.pycaw import AudioUtilities

# Setup logging to a file in the same directory as the executable
log_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "volumesync.log")
logging.basicConfig(filename=log_path, level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class VolumeSyncApp:
    def __init__(self):
        self.enabled = False
        self.running = True
        self.icon = None
        self._setup_icon()

    def _create_image(self, color="blue"):
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        dc = ImageDraw.Draw(image)
        dc.rectangle([width // 4, height // 4, width * 3 // 4, height * 3 // 4], fill=color)
        return image

    def _setup_icon(self):
        menu = Menu(
            MenuItem('Enabled', self._toggle_enabled, checked=lambda item: self.enabled),
            MenuItem('Sync Now', self._on_sync_now),
            MenuItem('Exit', self._on_exit)
        )
        # Initial state is disabled, so use gray icon
        self.icon = Icon("VolumeSync", self._create_image("gray"), "VolumeSync", menu)

    def _toggle_enabled(self, icon, item):
        self.enabled = not self.enabled
        new_color = "blue" if self.enabled else "gray"
        self.icon.icon = self._create_image(new_color)

    def _on_sync_now(self, icon, item):
        """Trigger a one-time sync in a separate thread to avoid blocking the UI."""
        def run_once():
            comtypes.CoInitialize()
            try:
                self.perform_sync()
            finally:
                comtypes.CoUninitialize()

        threading.Thread(target=run_once, daemon=True).start()

    def _on_exit(self, icon, item):
        self.running = False
        self.icon.stop()

    def perform_sync(self):
        """Perform a single synchronization pass. Assumes COM is initialized."""
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                try:
                    volume_control = session.SimpleAudioVolume
                    if volume_control:
                        current_app_vol = volume_control.GetMasterVolume()
                        target_app_vol = 1.0

                        if abs(current_app_vol - target_app_vol) > 0.001:
                            volume_control.SetMasterVolume(target_app_vol, None)
                except Exception:
                    continue
        except Exception as e:
            logging.error(f"Error in perform_sync: {e}")

    def sync_loop(self):
        """Background loop for volume synchronization with COM initialization."""
        # CRITICAL: Initialize COM for this specific thread
        comtypes.CoInitialize()

        try:
            while self.running:
                if self.enabled:
                    self.perform_sync()
                time.sleep(1.0) # Increased sleep slightly for stability
        finally:
            comtypes.CoUninitialize()
    def run(self):
        sync_thread = threading.Thread(target=self.sync_loop, daemon=True)
        sync_thread.start()
        self.icon.run()

if __name__ == "__main__":
    try:
        app = VolumeSyncApp()
        app.run()
    except Exception as e:
        logging.critical(f"Main app crash: {e}")
