from .map import Map
from .player import Player
from .settings_manager import SettingsMenu
from .ui_manager import UIManager
from .game_state import GameState

# Import GameEngine locally within methods that need it to avoid circular dependency

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

    def display_menu(self):
        self.game_state.ui_manager.display_menu(self.options, title="Main Menu")

    def get_choice(self):
        while True:
            choice = self.game_state.ui_manager.get_input("Enter your choice: ").strip()
            if choice in self.options:
                return self.options[choice]
            else:
                self.game_state.logger.add_message("Invalid choice. Please try again.")

    def start_new_game(self):
        from .game_engine import GameEngine # Local import to avoid circular dependency

        self.game_state.ui_manager.clear_screen()
        
        # Initialize player first, as SpawnManager needs access to game_state.player
        player = Player(0, 0) # Temporary player position
        self.game_state.player = player

        # Pass game_state to Map constructor so it can be used by MapGenerator and SpawnManager
        city_map = Map(self.map_width, self.map_height, map_type="city_center", game_state=self.game_state)
        self.game_state.game_map = city_map
        self.game_state.game_map.update_fov(self.game_state.player)

        self.game_state.is_running = True
        self.game_state.step_count = 0
        self.game_state.on_special_tile = False
        self.game_state.current_menu = None

        game_engine = GameEngine(self.game_state)
        game_engine.run()

    def _get_save_selection(self, available_saves):
        while True:
            try:
                selection = self.game_state.ui_manager.get_input("Enter the number of the save to load (or 'b' to go back): ").lower()
                if selection == 'b':
                    return None
                
                index = int(selection) - 1
                if 0 <= index < len(available_saves):
                    return index
                else:
                    self.game_state.logger.add_message("Invalid number. Please try again.")
            except ValueError:
                self.game_state.logger.add_message("Invalid input. Please enter a number or 'b'.")

    def load_game(self):
        self.game_state.ui_manager.clear_screen()
        self.game_state.logger.add_message("--- Load Game ---")
        available_saves = self.game_state.save_manager.list_saves()
        if not available_saves:
            self.game_state.logger.add_message("No saved games found.")
            self.game_state.ui_manager.get_input("Press Enter to continue...")
            return

        self.game_state.logger.add_message("Available saves:")
        for i, save_name in enumerate(available_saves):
            self.game_state.logger.add_message(f"{i+1}. {save_name}")
        
        selected_index = self._get_save_selection(available_saves)

        if selected_index is not None:
            loaded_player, loaded_map, map_width, map_height = self.game_state.save_manager.load_game(available_saves[selected_index], self.game_state.logger)
            if loaded_player and loaded_map:
                self.game_state.player = loaded_player
                self.game_state.game_map = loaded_map
                self.game_state.is_running = True
                self.game_state.step_count = 0
                self.game_state.on_special_tile = False
                self.game_state.current_menu = None

                from .game_engine import GameEngine # Local import to avoid circular dependency
                game_engine = GameEngine(self.game_state)
                game_engine.run()

    def open_settings(self):
        settings_menu = SettingsMenu(self.game_state, is_in_game=False)
        while True:
            settings_menu.display()
            choice = self.game_state.ui_manager.get_input("Enter choice: ").strip()
            if settings_menu.handle_input(choice):
                break

    def run(self):
        menu_actions = {
            "NEW GAME": self.start_new_game,
            "LOAD": self.load_game,
            "SETTINGS": self.open_settings,
            "QUIT": lambda: self.game_state.logger.add_message("Exiting game. Goodbye!") or True
        }

        while True:
            self.display_menu()
            choice = self.get_choice()

            action = menu_actions.get(choice)
            if action:
                if action() is True:
                    break
            else:
                self.game_state.logger.add_message("Invalid choice. Please try again.")

