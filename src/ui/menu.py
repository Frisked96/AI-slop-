from ..world.map import Map
from ..components.player import Player
from ..systems.settings_manager import SettingsManager
from .ui_manager import UIManager
from ..game_state import GameState
import curses
from .static_menus import ErrorMenu
from .minimap_menu import MinimapMenu

REQUIRED_SIDE_MENU_WIDTH = 25
REQUIRED_STATS_HEIGHT = 1
REQUIRED_LOG_HEIGHT = 10

class Menu:
    def __init__(self, game_state: GameState, map_width, map_height):
        self.game_state = game_state
        self.map_width = map_width
        self.map_height = map_height
        self.options = {
            "1": "NEW GAME",
            "2": "LOAD",
            "3": "SETTINGS",
            "4": "QUIT"
        }

    def run(self):
        menu_actions = {
            "NEW GAME": self.start_new_game,
            "LOAD": self.load_game,
            "SETTINGS": self.open_settings,
            "QUIT": lambda: "quit"
        }

        while True:
            self.game_state.ui_manager.clear_screen()
            self.game_state.ui_manager.display_menu(self.options, title="Main Menu")
            
            prompt_y = len(self.options) + 3
            choice_key = self.game_state.ui_manager.get_string(prompt_y, 0, "Enter your choice: ").strip()
            
            choice_action = self.options.get(choice_key)

            if choice_action:
                action = menu_actions.get(choice_action)
                if action:
                    result = action()
                    if result == "start_game":
                        return "start_game"
                    elif result == "quit":
                        return "quit"
            else:
                self.game_state.ui_manager.display_message(prompt_y + 1, 0, "Invalid choice. Please try again.")
                self.game_state.ui_manager.refresh()
                

    def start_new_game(self):
        self.game_state.ui_manager.clear_screen()
        
        player = Player(0, 0)
        self.game_state.player = player

        dungeon_map = Map(self.map_width, self.map_height, map_type="dungeon", game_state=self.game_state)
        self.game_state.game_map = dungeon_map
        self.game_state.game_map.update_fov(self.game_state.player)

        self.game_state.minimap_menu = MinimapMenu(self.game_state)

        self.game_state.is_running = True
        self.game_state.current_menu = None

        return "start_game"

    def load_game(self):
        available_saves = self.game_state.save_manager.list_saves()
        self.game_state.ui_manager.display_save_screen(available_saves)

        max_y, max_x = self.game_state.ui_manager.stdscr.getmaxyx()
        prompt_y = max_y - 1

        filename = self.game_state.ui_manager.get_string(prompt_y, 0, "Enter filename to load (or 'b' to go back): ").strip().lower()

        if filename == 'b':
            self.game_state.logger.add_message("Load cancelled. Returning to main menu.")
            return None

        if not filename:
            self.game_state.logger.add_message("Load cancelled.")
            return None

        loaded_game_state = self.game_state.save_manager.load_game(filename, self.game_state.logger)

        if loaded_game_state:
            self.game_state.player = loaded_game_state.player
            self.game_state.game_map = loaded_game_state.game_map
            self.game_state.game_map.game_state = loaded_game_state
            self.game_state.game_map.update_fov(self.game_state.player)
            self.game_state.is_running = True
            self.game_state.current_menu = None

            return "start_game"
        else:
            self.game_state.logger.add_message(f"Failed to load game: {filename}")
            return None

    def open_settings(self):
        return False
