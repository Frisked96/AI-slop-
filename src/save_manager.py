import json
import os
from .map import Map
from .player import Player
from .ui_manager import UIManager

SAVE_DIR = "saves"

class SaveManager:
    def __init__(self, ui_manager: UIManager, settings_manager):
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        self.ui_manager = ui_manager
        self.settings_manager = settings_manager
        self._autosave_overwrite_confirmed = None # None: not asked, True: confirmed, False: denied

    def _get_save_path(self, filename):
        return os.path.join(SAVE_DIR, filename + ".json")

    def save_game(self, game_state_data, filename, is_autosave=False):
        save_path = self._get_save_path(filename)

        if is_autosave and filename == "autosave":
            overwrite_behavior = self.settings_manager.get_setting("autosave_overwrite_behavior")
            if overwrite_behavior == "never_overwrite":
                return "Autosave skipped (never overwrite setting)."
            elif overwrite_behavior == "ask_once":
                if self._autosave_overwrite_confirmed is False:
                    return "Autosave skipped for this session."
                elif self._autosave_overwrite_confirmed is None and os.path.exists(save_path):
                    confirm = self.ui_manager.get_input(f"Autosave file '{filename}' already exists. Overwrite for this session? (y/n): ").lower()
                    if confirm == 'y':
                        self._autosave_overwrite_confirmed = True
                        return "Game Autosaved!"
                    else:
                        self._autosave_overwrite_confirmed = False
                        return "Autosave skipped for this session."
                elif self._autosave_overwrite_confirmed is True:
                    return "Game Autosaved!"
            elif overwrite_behavior == "always_overwrite":
                return "Game Autosaved!"
        else:
            if os.path.exists(save_path):
                confirm = self.ui_manager.get_input(f"Save file '{filename}' already exists. Overwrite? (y/n): ").lower()
                if confirm != 'y':
                    return "Save cancelled."

        with open(save_path, 'w') as f:
            json.dump(game_state_data, f, indent=4)
        return f"Game saved to {save_path}"

    def reset_autosave_confirmation(self):
        self._autosave_overwrite_confirmed = None

    def load_game(self, filename, logger):
        save_path = self._get_save_path(filename)
        if not os.path.exists(save_path):
            logger.add_message(f"Error: Save file {filename}.json not found.")
            return None, None, None, None

        with open(save_path, 'r') as f:
            game_state_data = json.load(f)

        loaded_player = Player.from_dict(game_state_data["player"])
        loaded_map = Map.from_dict(game_state_data["map"])
        loaded_map.update_fov(loaded_player)
        
        # Pass the logger to the GameState
        game_state = GameState.from_dict(game_state_data, self.settings_manager, self, self.ui_manager, logger)

        logger.add_message(f"Game loaded from {save_path}")
        return loaded_player, loaded_map, game_state_data["map_width"], game_state_data["map_height"]

    def list_saves(self):
        saves = []
        if os.path.exists(SAVE_DIR):
            for filename in os.listdir(SAVE_DIR):
                if filename.endswith(".json"):
                    saves.append(filename[:-5]) # Remove .json extension
        return saves
