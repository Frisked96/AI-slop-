import curses
from src.ui.menu import Menu
from src.systems.save_manager import SaveManager
from src.systems.settings_manager import SettingsManager
from src.ui.ui_manager import UIManager
from src.ui.themes import init_colors
from src.game_engine import GameEngine
from src.game_state import GameState
from src.utils.logger import Logger
from src.systems.spawn_manager import SpawnManager
from src.systems.event_manager import EventManager
from src.ui.static_menus import WarningMenu

def main(stdscr):
    curses.curs_set(0)

    settings_manager = SettingsManager()
    # Load map dimensions from settings
    map_width = settings_manager.get_setting("map_width", 80) # Default to 80 if not found
    map_height = settings_manager.get_setting("map_height", 20) # Default to 20 if not found
    camera_width = settings_manager.get_setting("camera_width", 80)
    camera_height = settings_manager.get_setting("camera_height", 24)

    warning_menu = WarningMenu(stdscr)
    warning_menu.display()
    
    ui_manager = UIManager(stdscr, camera_width, camera_height)
    save_manager = SaveManager(ui_manager, settings_manager)
    logger = Logger(settings_manager)
    event_manager = EventManager() # Initialize EventManager

    # Create a placeholder for spawn_manager first
    spawn_manager = SpawnManager(None) # Will be updated later

    # Initialize GameState with managers, including the placeholder spawn_manager and event_manager
    initial_game_state = GameState(
        settings_manager=settings_manager,
        save_manager=save_manager,
        ui_manager=ui_manager,
        logger=logger,
        spawn_manager=spawn_manager,
        event_manager=event_manager, # Pass the event_manager
        minimap_menu=None # Will be initialized later in Menu.start_new_game
    )

    # Now, set the game_state for the spawn_manager
    spawn_manager = initial_game_state

    # Subscribe logger to relevant events (example)
    event_manager.subscribe("game_message", logger.add_message)

    menu = Menu(initial_game_state, map_width, map_height)
    menu_result = menu.run()

    if menu_result == "start_game":
        game_engine = GameEngine(initial_game_state)
        game_engine.run()
    elif menu_result == "quit":
        pass # Exit the game

if __name__ == "__main__":
    curses.wrapper(main)
