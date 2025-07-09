import random
from ..world.tiles import FloorTile, WallTile, GrassTile, MudTile, RockTile, RubbleTile

class SpawnManager:
    def __init__(self, game_state):
        self.game_state = game_state

    def find_spawn_position(self, grid, entity_type="player", avoid_tiles=None, preferred_tiles=None, min_distance_from_player=0):
        if avoid_tiles is None:
            avoid_tiles = [WallTile]
        
        if preferred_tiles is None:
            preferred_tiles = [FloorTile, GrassTile, MudTile, RockTile, RubbleTile]

        potential_spawns = []
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        for y in range(height):
            for x in range(width):
                tile = grid[y][x]
                is_suitable = True

                if any(isinstance(tile, avoid_class) for avoid_class in avoid_tiles):
                    continue

                if preferred_tiles and not any(isinstance(tile, pref_class) for pref_class in preferred_tiles):
                    continue

                if self.game_state.player and min_distance_from_player > 0:
                    distance = ((x - self.game_state.player.x)**2 + (y - self.game_state.player.y)**2)**0.5
                    if distance < min_distance_from_player:
                        continue

                potential_spawns.append((x, y))

        return random.choice(potential_spawns) if potential_spawns else None
