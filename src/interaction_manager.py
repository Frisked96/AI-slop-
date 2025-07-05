from .map import Map
from .tiles import NextMapTile, NorthExitTile, EastExitTile, SouthExitTile, WestExitTile, CityCenterEntranceTile, BlacksmithShopTile, DoorTile

class InteractionManager:
    def __init__(self, game_state):
        self.game_state = game_state
        self.current_interaction_tile = None # Store the tile being interacted with

        self._tile_interactions = {
            NextMapTile: self._handle_next_map_tile,
            NorthExitTile: self._handle_north_exit_tile,
            EastExitTile: self._handle_east_exit_tile,
            SouthExitTile: self._handle_south_exit_tile,
            WestExitTile: self._handle_west_exit_tile,
            CityCenterEntranceTile: self._handle_city_center_entrance_tile,
            DoorTile: self._handle_door_tile,
        }

    def _transition_map(self, message, map_type, entry_direction=None):
        self.game_state.logger.add_message(message)
        self.game_state.game_map = Map(self.game_state.game_map.width, self.game_state.game_map.height, map_type=map_type, entry_direction=entry_direction, game_state=self.game_state)

    def _handle_next_map_tile(self):
        if self.game_state.game_map.current_map_type == "dungeon":
            self.game_state.dungeon_level += 1
            self.game_state.logger.add_message(f"Descending to Dungeon Level {self.game_state.dungeon_level}...")
        self._transition_map("Generating new dungeon map...", "dungeon")

    def _handle_north_exit_tile(self):
        self._transition_map("Traveling to North Sector...", "outer_city", "north")

    def _handle_east_exit_tile(self):
        self._transition_map("Traveling to East Sector...", "outer_city", "east")

    def _handle_south_exit_tile(self):
        self._transition_map("Traveling to South Sector...", "outer_city", "south")

    def _handle_west_exit_tile(self):
        self._transition_map("Traveling to West Sector...", "outer_city", "west")

    def _handle_city_center_entrance_tile(self):
        self._transition_map("Returning to City Center...", "city_center")

    def _handle_door_tile(self):
        self.game_state.current_menu = self.game_state.blacksmith_menu

    def handle_interactions(self):
        player_x, player_y = self.game_state.player.x, self.game_state.player.y
        current_tile = self.game_state.game_map.grid[player_y][player_x]

        if type(current_tile) in self._tile_interactions:
            self.game_state.on_special_tile = True
            self.current_interaction_tile = current_tile
        else:
            self.game_state.on_special_tile = False
            self.current_interaction_tile = None

    def is_player_in_blacksmith_shop(self):
        if self.game_state.game_map.current_map_type != "city_center":
            return False
        shop_start_x = 1
        shop_start_y = 1
        shop_width = 12
        shop_height = 7
        return shop_start_x <= self.game_state.player.x < shop_start_x + shop_width and \
               shop_start_y <= self.game_state.player.y < shop_start_y + shop_height

    def travel(self):
        if self.current_interaction_tile:
            handler = self._tile_interactions.get(type(self.current_interaction_tile))
            if handler:
                handler()
