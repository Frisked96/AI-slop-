from src.menu import Menu
from src.save_manager import SaveManager
from src.settings_manager import SettingsManager
from src.ui_manager import UIManager
from src.game_engine import GameEngine
from src.game_state import GameState
from src.map import Map
from src.player import Player
from src.logger import Logger
from src.spawn_manager import SpawnManager

def main():
    ui_manager = UIManager()
    settings_manager = SettingsManager()
    save_manager = SaveManager(ui_manager, settings_manager)
    logger = Logger(settings_manager)

    # Create a placeholder for spawn_manager first
    spawn_manager = SpawnManager(None) # Will be updated later

    # Load map dimensions from settings
    map_width = settings_manager.get_setting("map_width", 80) # Default to 80 if not found
    map_height = settings_manager.get_setting("map_height", 20) # Default to 20 if not found

    # Initialize GameState with managers, including the placeholder spawn_manager
    initial_game_state = GameState(
        settings_manager=settings_manager,
        save_manager=save_manager,
        ui_manager=ui_manager,
        logger=logger,
        spawn_manager=spawn_manager # Pass the placeholder
    )

    # Now, set the game_state for the spawn_manager
    spawn_manager.game_state = initial_game_state

    menu = Menu(initial_game_state, map_width, map_height)
    menu.run()

    menu = Menu(initial_game_state, map_width, map_height)
    menu.run()

if __name__ == "__main__":
    main()