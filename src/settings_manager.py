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
            "autosave_interval": 10, # Steps
            "map_width": 80, # Default map width
            "map_height": 24, # Default map height
            "autosave_overwrite_behavior": "ask_once", # Default overwrite behavior
            "debug_visible_traps": False # Default for the new setting
        }

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            print(f"Error saving settings: {e}. Please check file permissions.")

    def get_setting(self, key, default=None):
        return self.settings.get(key, default if default is not None else self._get_default_settings().get(key))

    def set_setting(self, key, value):
        self.settings[key] = value
        self._save_settings()

class SettingsMenu:
    def __init__(self, game_state, is_in_game=False):
        self.game_state = game_state
        self.is_in_game = is_in_game
        self.options = {}
        self._build_options()

    def _build_options(self):
        self.options = {
            "1": "Toggle Autosave",
            "2": "Set Autosave Interval",
        }
        if not self.is_in_game:
            self.options["3"] = "Set Map Width"
            self.options["4"] = "Set Map Height"
            self.options["5"] = "Back"
        else:
            self.options["3"] = "Back"

    def display(self):
        self.game_state.ui_manager.display_settings_menu(self.game_state.settings_manager, self.options, self.is_in_game)

    def handle_input(self, choice):
        if choice == "1":
            current_status = self.game_state.settings_manager.get_setting("autosave_enabled")
            self.game_state.settings_manager.set_setting("autosave_enabled", not current_status)
            self.game_state.logger.add_message(f"Autosave is now {'Enabled' if not current_status else 'Disabled'}.")
        elif choice == "2":
            while True:
                try:
                    new_interval_str = self.game_state.ui_manager.get_input("Enter new autosave interval (steps): ")
                    if new_interval_str is None:  # Handle potential cancellation from get_input
                        break
                    new_interval = int(new_interval_str)
                    if new_interval > 0:
                        self.game_state.settings_manager.set_setting("autosave_interval", new_interval)
                        self.game_state.logger.add_message(f"Autosave interval set to {new_interval} steps.")
                        break
                    else:
                        self.game_state.logger.add_message("Interval must be a positive number.")
                except ValueError:
                    self.game_state.logger.add_message("Invalid input. Please enter a number.")
        elif choice == "3": # This will be "Set Map Width" or "Back" depending on is_in_game
            if not self.is_in_game:
                while True:
                    try:
                        new_width_str = self.game_state.ui_manager.get_input("Enter new map width: ")
                        if new_width_str is None:
                            break
                        new_width = int(new_width_str)
                        if new_width > 0:
                            self.game_state.settings_manager.set_setting("map_width", new_width)
                            self.game_state.logger.add_message(f"Map width set to {new_width}.")
                            break
                        else:
                            self.game_state.logger.add_message("Width must be a positive number.")
                    except ValueError:
                        self.game_state.logger.add_message("Invalid input. Please enter a number.")
            else:
                return True  # Back option when in-game
        elif choice == "4": # This will be "Set Map Height" or invalid depending on is_in_game
            if not self.is_in_game:
                while True:
                    try:
                        new_height_str = self.game_state.ui_manager.get_input("Enter new map height: ")
                        if new_height_str is None:
                            break
                        new_height = int(new_height_str)
                        if new_height > 0:
                            self.game_state.settings_manager.set_setting("map_height", new_height)
                            self.game_state.logger.add_message(f"Map height set to {new_height}.")
                            break
                        else:
                            self.game_state.logger.add_message("Height must be a positive number.")
                    except ValueError:
                        self.game_state.logger.add_message("Invalid input. Please enter a number.")
            else:
                self.game_state.logger.add_message("Invalid choice.") # Should not happen if options are built correctly
        elif choice == "5": # This will be "Back" or invalid depending on is_in_game
            if not self.is_in_game:
                return True  # Back option when not in-game
            else:
                self.game_state.logger.add_message("Invalid choice.") # Should not happen if options are built correctly
        return False
