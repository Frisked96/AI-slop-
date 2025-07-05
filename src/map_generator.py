import random
from .levels.city_center import CityCenterLevel
from .levels.east_sector import EastSectorLevel
from .levels.west_sector import WestSectorLevel
from .levels.south_sector import SouthSectorLevel
from .levels.north_sector import NorthSectorLevel
from .levels.dungeon_level import DungeonLevel
from .tiles import WallTile, FloorTile, TrapTile

class MapGenerator:
    _level_generators = {
        "dungeon": DungeonLevel,
        "city_center": CityCenterLevel,
        "north": NorthSectorLevel,
        "east": EastSectorLevel,
        "south": SouthSectorLevel,
        "west": WestSectorLevel,
    }

    @staticmethod
    def generate_map(width, height, map_type, entry_direction=None, game_state=None):
        grid = [[WallTile() for _ in range(width)] for _ in range(height)]
        room_centers = []
        next_map_tile_pos = None
        player_spawn_pos = None

        if map_type == "outer_city":
            level_class = MapGenerator._level_generators.get(entry_direction, CityCenterLevel) # Fallback to CityCenterLevel
            level = level_class(width, height)
            grid, room_centers, next_map_tile_pos, player_spawn_pos = level.generate_map(grid, room_centers, next_map_tile_pos, entry_direction, game_state)
        else:
            level_class = MapGenerator._level_generators.get(map_type)
            if level_class:
                level = level_class(width, height)
                grid, room_centers, next_map_tile_pos, player_spawn_pos = level.generate_map(grid, room_centers, next_map_tile_pos, game_state)
            else:
                # Handle unknown map_type, perhaps raise an error or default to dungeon
                dungeon_level = DungeonLevel(width, height)
                grid, room_centers, next_map_tile_pos, player_spawn_pos = dungeon_level.generate_map(grid, room_centers, next_map_tile_pos, game_state)
        
        # Set player position after map generation is complete
        if player_spawn_pos:
            game_state.player.x, game_state.player.y = player_spawn_pos

        # Spawn trap tiles
        # Use the 'map_type' argument directly, as game_state.game_map might not be set yet during initial map creation.
        if game_state and map_type == "dungeon" and game_state.dungeon_level >= 3:
            placed_traps = 0
            max_trap_spawns = 2 # As per requirement

            # Create a list of possible spawn locations (walkable floor tiles)
            possible_spawn_points = []
            for y in range(height):
                for x in range(width):
                    # Check if it's a FloorTile, not player spawn, and not next map tile
                    is_floor = isinstance(grid[y][x], FloorTile)
                    is_player_spawn = (player_spawn_pos and x == player_spawn_pos[0] and y == player_spawn_pos[1])
                    is_next_map_tile = (next_map_tile_pos and x == next_map_tile_pos[0] and y == next_map_tile_pos[1])

                    if is_floor and not is_player_spawn and not is_next_map_tile:
                        possible_spawn_points.append((x, y))

            random.shuffle(possible_spawn_points)

            for _ in range(max_trap_spawns):
                if not possible_spawn_points:
                    break # No more valid spots to place traps

                spawn_x, spawn_y = possible_spawn_points.pop()
                trap_char = '.' # Default character
                if game_state and game_state.settings_manager:
                    if game_state.settings_manager.get_setting("debug_visible_traps", False):
                        trap_char = '$'
                grid[spawn_y][spawn_x] = TrapTile(character=trap_char)
                placed_traps += 1
                # Removed logging of trap placement to keep them hidden
                # if game_state.logger:
                #     game_state.logger.add_message(f"Placed trap at ({spawn_x}, {spawn_y}) on level {game_state.dungeon_level}")


        return grid, room_centers, next_map_tile_pos
