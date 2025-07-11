from .ui.ui_manager import UIManager
from .utils.logger import Logger
from .systems.save_manager import SaveManager



class GameState:
    def __init__(self, player=None, game_map=None, settings_manager=None, save_manager=None, ui_manager:UIManager =None, command_handler=None, interaction_manager=None, inventory_menu=None, minimap_menu=None, logger: Logger = None, game_engine=None, spawn_manager=None, event_manager=None):
        self.player = player
        self.game_map = game_map
        self.settings_manager = settings_manager
        self.save_manager = save_manager
        self.ui_manager = ui_manager
        self.command_handler = command_handler
        self.interaction_manager = interaction_manager
        self.inventory_menu = inventory_menu
        self.minimap_menu = minimap_menu
        self.logger = logger
        self.game_engine = game_engine
        self.spawn_manager = spawn_manager
        self.event_manager = event_manager # Added event_manager
        self.current_menu = None
        self.is_running = True
        self.step_count = 0
        self.on_special_tile = False
        self.dungeon_level = 1  # Initialize dungeon level

    def to_dict(self):
        return {
            "player": self.player.to_dict() if self.player else None,
            "game_map": self.game_map.to_dict() if self.game_map else None,
            "current_menu": self.current_menu.__class__.__name__ if self.current_menu else None,
            "is_running": self.is_running,
            "step_count": self.step_count,
            "on_special_tile": self.on_special_tile,
            "dungeon_level": self.dungeon_level,  # Add dungeon_level to dictionary
            "log": self.logger.get_messages() if self.logger else []
        }

    @classmethod
    def from_dict(cls, data, settings_manager, save_manager, ui_manager, logger, event_manager=None, player=None, game_map=None):
        # Note: Player and Map will be reconstructed by SaveManager
        game_state = cls(
            settings_manager=settings_manager,
            save_manager=save_manager,
            ui_manager=ui_manager,
            logger=logger,
            event_manager=event_manager, # Pass event_manager to from_dict
            player=player, # Pass player to from_dict
            game_map=game_map # Pass game_map to from_dict
        )
        game_state.is_running = data.get("is_running", True)
        game_state.step_count = data.get("step_count", 0)
        game_state.on_special_tile = data.get("on_special_tile", False)
        game_state.dungeon_level = data.get("dungeon_level", 1)  # Load dungeon_level, default to 1
        if logger and "log" in data:
            for msg in data["log"]:
                logger.add_message(msg)
        # current_menu will be set by GameEngine based on context
        return game_state