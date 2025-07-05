from .levels.city_center import CityCenterLevel
from .levels.east_sector import EastSectorLevel
from .levels.west_sector import WestSectorLevel
from .levels.south_sector import SouthSectorLevel
from .levels.north_sector import NorthSectorLevel
from .levels.dungeon_level import DungeonLevel
from .tiles import WallTile

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

        return grid, room_centers, next_map_tile_pos
