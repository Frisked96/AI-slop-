import time
from .systems.command_handler import CommandHandler
from .systems.interaction_manager import InteractionManager
from .ui.inventory_menu import InventoryMenu
from .systems.settings_manager import SettingsManager
from .ui.ui_manager import UIManager
from .game_state import GameState

from .world.tiles import WaterTile

class GameEngine:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.game_state.game_engine = self
        self.game_state.command_handler = CommandHandler(self.game_state)
        self.game_state.interaction_manager = InteractionManager(self.game_state)
        self.game_state.inventory_menu = InventoryMenu(self.game_state.player, self.game_state)
        self.last_move_time = 0

    def run(self):
        self.game_state.ui_manager.init_ui()
        self.game_state.ui_manager.stdscr.nodelay(True)  # Set non-blocking mode

        while self.game_state.is_running:
            self.game_state.ui_manager.clear_screen()

            if self.game_state.current_menu:
                self.game_state.current_menu.display()
            else:
                self.render_game_world()

            self.game_state.ui_manager.refresh()
            
            self.process_input()

            if not self.game_state.current_menu:
                self.game_state.interaction_manager.handle_interactions()
                if self.game_state.player.moved:
                    # A turn has passed, update player state
                    self.game_state.player.[ state.update_effects()
                    self.game_state.player.update_wellbeing() # Also update hunger/thirst

                    self.game_state.game_map.update_fov(self.game_state.player)
                    current_tile = self.game_state.game_map.grid[self.game_state.player.y][self.game_state.player.x]
                    self.game_state.logger.log_tile_info(current_tile)
                    self.game_state.player.moved = False
            
            time.sleep(0.05) # Add a small delay to the loop to prevent high CPU usage

    def process_input(self):
        if self.game_state.current_menu:
            self.game_state.ui_manager.stdscr.nodelay(False) # Disable non-blocking for menu input

            if isinstance(self.game_state.current_menu, MinimapMenu):
                # For MinimapMenu, we just need a single key press to exit
                key = self.game_state.ui_manager.get_key_if_available()
                if key:
                    if self.game_state.current_menu.handle_input(key):
                        self.game_state.current_menu = None
            else:
                # For other menus (with options and string input)
                prompt_y = len(self.game_state.current_menu.options) + 3
                choice = self.game_state.ui_manager.get_string(prompt_y, 0, "Enter choice: ")
                if self.game_state.current_menu.handle_input(choice):
                    self.game_state.current_menu = None
            
            self.game_state.ui_manager.stdscr.nodelay(True) # Re-enable non-blocking
        else:
            key = self.game_state.ui_manager.get_key_if_available()
            if key:
                current_time = time.time()
                if key in ['w', 'a', 's', 'd']:
                    if current_time - self.last_move_time > 0.2: # Cooldown for held keys
                        self.game_state.command_handler.handle_command(key)
                        self.last_move_time = current_time
                else:
                    self.game_state.command_handler.handle_command(key)

    def display_settings_menu(self):
        pass

    def render_game_world(self):
        self.game_state.ui_manager.display_map(self.game_state.game_map, self.game_state.player, self.game_state)
        self.game_state.ui_manager.display_player_stats(self.game_state.player, self.game_state)
        if self.game_state.logger:
            self.game_state.ui_manager.display_log(self.game_state.logger.get_messages(), self.game_state)

    # ... (rest of the class)