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
logging.basicConfig(filename=log_path, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class VolumeSyncApp:
    def __init__(self):
        self.enabled = True
        self.running = True
        self.icon = None
        self._setup_icon()
        logging.info("App initialized.")

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
            MenuItem('Exit', self._on_exit)
        )
        self.icon = Icon("VolumeSync", self._create_image("blue"), "VolumeSync", menu)

    def _toggle_enabled(self, icon, item):
        self.enabled = not self.enabled
        new_color = "blue" if self.enabled else "gray"
        self.icon.icon = self._create_image(new_color)
        logging.info(f"Sync enabled: {self.enabled}")

    def _on_exit(self, icon, item):
        self.running = False
        self.icon.stop()
        logging.info("App exiting.")

    def sync_loop(self):
        """Background loop for volume synchronization with COM initialization."""
        logging.info("Sync thread started.")
        # CRITICAL: Initialize COM for this specific thread
        comtypes.CoInitialize()
        
        try:
            while self.running:
                if self.enabled:
                    try:
                        sessions = AudioUtilities.GetAllSessions()
                        for session in sessions:
                            # Try to sync sessions that have a simple audio volume interface
                            # We check if it has a process or if it's a system session we care about
                            try:
                                volume_control = session.SimpleAudioVolume
                                if volume_control:
                                    current_app_vol = volume_control.GetMasterVolume()
                                    target_app_vol = 1.0
                                    
                                    if abs(current_app_vol - target_app_vol) > 0.001:
                                        volume_control.SetMasterVolume(target_app_vol, None)
                                        # Use process name for logging if available
                                        name = session.Process.name() if session.Process else "System Session"
                                        logging.debug(f"Synced {name} to 1.0")
                            except Exception as ex:
                                # Ignore individual session errors
                                continue
                    except Exception as e:
                        logging.error(f"Error in sync cycle: {e}")

                time.sleep(1.0) # Increased sleep slightly for stability
        finally:
            comtypes.CoUninitialize()
            logging.info("Sync thread stopped.")

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
