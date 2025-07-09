import random
from .levels.dungeon_level import DungeonLevel
from .tiles import WallTile, FloorTile, TrapTile

class MapGenerator:
    _level_generators = {
        "dungeon": DungeonLevel,
    }

    @staticmethod
    def generate_map(width, height, map_type, entry_direction=None, game_state=None):
        grid = [[WallTile() for _ in range(width)] for _ in range(height)]
        room_centers = []
        next_map_tile_pos = None
        player_spawn_pos = None

        level_class = MapGenerator._level_generators.get(map_type)
        if level_class:
            level = level_class(width, height)
            grid, room_centers, next_map_tile_pos, player_spawn_pos, room_coords, corridor_coords = level.generate_map(grid, room_centers, next_map_tile_pos, game_state)
        else:
            dungeon_level = DungeonLevel(width, height)
            grid, room_centers, next_map_tile_pos, player_spawn_pos, room_coords, corridor_coords = dungeon_level.generate_map(grid, room_centers, next_map_tile_pos, game_state)

        return grid, room_centers, next_map_tile_pos, player_spawn_pos, room_coords, corridor_coords
