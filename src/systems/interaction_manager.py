from ..world.map import Map
from ..world.tiles import NextMapTile, TrapTile
from ..world.map_generator import MapGenerator
from ..utils.logger import Logger 

class InteractionManager:
    def __init__(self, game_state):
        self.game_state = game_state
        self.current_interaction_tile = None

        self._tile_interactions = {
            NextMapTile: self._handle_next_map_tile,
        }

    def _transition_map(self, message, map_type, entry_direction=None):
        self.game_state.logger.add_message(message)
        new_grid, room_centers, next_map_tile_pos, player_spawn_pos, room_coords, corridor_coords = MapGenerator.generate_map(
            self.game_state.game_map.width, self.game_state.game_map.height, map_type, entry_direction, self.game_state
        )
        self.game_state.game_map = Map(
            self.game_state.game_map.width, self.game_state.game_map.height, map_type=map_type, 
            generate=False, grid=new_grid, room_centers=room_centers, 
            next_map_tile_pos=next_map_tile_pos, room_coords=room_coords, 
            corridor_coords=corridor_coords, game_state=self.game_state
        )
        if player_spawn_pos:
            self.game_state.player.x, self.game_state.player.y = player_spawn_pos
        self.game_state.minimap_menu.update_map_data(self.game_state.game_map)

    def _handle_next_map_tile(self):
        if self.game_state.game_map.current_map_type == "dungeon":
            self.game_state.dungeon_level += 1
            self.game_state.logger.add_message(f"Descending to Dungeon Level {self.game_state.dungeon_level}...")
        self._transition_map("Generating new dungeon map...", "dungeon")

    def handle_interactions(self):
        player_x, player_y = self.game_state.player.x, self.game_state.player.y
        game_map = self.game_state.game_map
        player_on_special_tile_this_turn = False

        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                check_x, check_y = player_x + x_offset, player_y + y_offset
                if 0 <= check_y < game_map.height and 0 <= check_x < game_map.width:
                    tile_to_check = game_map.grid[check_y][check_x]
                    if isinstance(tile_to_check, TrapTile):
                        if not tile_to_check.is_revealed:
                            tile_to_check.reveal()
                        tile_to_check.trigger(self.game_state.player, self.game_state)
                        if check_x == player_x and check_y == player_y:
                            player_on_special_tile_this_turn = True
                            self.current_interaction_tile = tile_to_check

        current_tile_at_player_pos = game_map.grid[player_y][player_x]
        if not player_on_special_tile_this_turn and type(current_tile_at_player_pos) in self._tile_interactions:
            player_on_special_tile_this_turn = True
            self.current_interaction_tile = current_tile_at_player_pos

        self.game_state.on_special_tile = player_on_special_tile_this_turn
        if not player_on_special_tile_this_turn:
            self.current_interaction_tile = None
