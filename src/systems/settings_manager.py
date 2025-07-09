import json
import os

SETTINGS_FILE = 'settings.json'

class SettingsManager:
    def __init__(self):
        self.settings = self._load_settings()

    def _load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading settings: {e}. Using default settings.")
        return self._get_default_settings()

    def _get_default_settings(self):
        return {
            "autosave_enabled": True,
            "autosave_interval": 10,
            "map_width": 80,
            "map_height": 24,
            "autosave_overwrite_behavior": "ask_once",
            "debug_visible_traps": False
        }

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            print(f"Error saving settings: {e}. Please check file permissions.")

    def get_setting(self, key, default=None):
        return self.settings.get(key, self._get_default_settings().get(key) if default is None else default)

    def set_setting(self, key, value):
        self.settings[key] = value
        self._save_settings()
