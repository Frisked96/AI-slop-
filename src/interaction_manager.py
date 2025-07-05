from .map import Map
from .tiles import NextMapTile, NorthExitTile, EastExitTile, SouthExitTile, WestExitTile, CityCenterEntranceTile, BlacksmithShopTile, DoorTile, TrapTile

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
        game_map = self.game_state.game_map
        player_on_special_tile_this_turn = False # Flag to track if player ends up on a special tile

        # Proximity Trap Activation Logic (반경 1타일 내 함정 활성화 및 발동)
        # Iterate through a 3x3 grid around the player
        for y_offset in range(-1, 2):  # -1, 0, 1
            for x_offset in range(-1, 2):  # -1, 0, 1
                check_x, check_y = player_x + x_offset, player_y + y_offset

                # Check map boundaries
                if 0 <= check_y < game_map.height and 0 <= check_x < game_map.width:
                    tile_to_check = game_map.grid[check_y][check_x]
                    if isinstance(tile_to_check, TrapTile):
                        # Reveal the trap if it's not already (changes char to '+')
                        if not tile_to_check.is_revealed:
                            tile_to_check.reveal()
                            # Optional: Log trap reveal if distinct from trigger
                            # self.game_state.logger.add_message(f"Trap at ({check_x}, {check_y}) revealed by proximity!")

                        # Attempt to trigger the trap. The trap itself ensures it only triggers once.
                        # This will also handle damage and logging if it's the first time.
                        tile_to_check.trigger(self.game_state.player, self.game_state)

                        # If the player is currently ON this (now revealed/triggered) trap tile
                        if check_x == player_x and check_y == player_y:
                            player_on_special_tile_this_turn = True
                            self.current_interaction_tile = tile_to_check


        # Standard Tile Interactions (Doors, Exits, etc.)
        # This needs to be checked for the tile the player is CURRENTLY standing on,
        # if it wasn't already handled as a trap.
        current_tile_at_player_pos = game_map.grid[player_y][player_x]
        if not player_on_special_tile_this_turn and type(current_tile_at_player_pos) in self._tile_interactions:
            player_on_special_tile_this_turn = True
            self.current_interaction_tile = current_tile_at_player_pos

        # Update game_state based on whether the player landed on any special tile
        if player_on_special_tile_this_turn:
            self.game_state.on_special_tile = True
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
