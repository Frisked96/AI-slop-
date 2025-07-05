from .command_handler import CommandHandler
from .interaction_manager import InteractionManager
from .blacksmith_menu import BlacksmithMenu
from .inventory_menu import InventoryMenu
from .settings_manager import SettingsMenu
from .ui_manager import UIManager
from .game_state import GameState # Import GameState

class GameEngine:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.game_state.game_engine = self
        # Initialize managers and assign them to game_state
        self.game_state.command_handler = CommandHandler(self.game_state)
        self.game_state.interaction_manager = InteractionManager(self.game_state)
        self.game_state.blacksmith_menu = BlacksmithMenu(self.game_state)
        self.game_state.inventory_menu = InventoryMenu(self.game_state.player, self.game_state)

    

    def run(self):
        while self.game_state.is_running:
            self.render()
            if self.game_state.current_menu:
                self.game_state.current_menu.display()
            self.process_input()
            self.game_state.interaction_manager.handle_interactions()

    def process_input(self):
        if self.game_state.current_menu:
            choice = self.game_state.ui_manager.get_input("Enter choice: ").strip()
            if self.game_state.current_menu.handle_input(choice):
                self.game_state.current_menu = None
        else:
            self.game_state.command_handler.handle_command()

    def display_blacksmith_menu(self):
        self.game_state.current_menu = self.game_state.blacksmith_menu

    def display_settings_menu(self):
        self.game_state.current_menu = SettingsMenu(self.game_state, is_in_game=True)

    

    def render(self):
        self.game_state.ui_manager.display_map(self.game_state.game_map, self.game_state.player)
        self.game_state.ui_manager.display_player_stats(self.game_state.player)
        if self.game_state.logger:
            self.game_state.ui_manager.display_log(self.game_state.logger.get_messages())
