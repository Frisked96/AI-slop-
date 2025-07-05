import random
from .tiles import FloorTile, WallTile # Import necessary tile types

class SpawnManager:
    def __init__(self, game_state):
        self.game_state = game_state

    def find_spawn_position(self, grid, entity_type="player", avoid_tiles=None, preferred_tiles=None, min_distance_from_player=0):
        """Finds a suitable spawn position for an entity on the given grid.

        Args:
            grid: The 2D list representing the map grid.
            entity_type (str): The type of entity to spawn (e.g., "player", "enemy").
            avoid_tiles (list): A list of tile classes to avoid spawning on.
            preferred_tiles (list): A list of tile classes to prefer spawning on.
            min_distance_from_player (int): Minimum distance from the player (if player exists).

        Returns:
            tuple: (x, y) coordinates of the spawn position, or None if no suitable position is found.
        """
        if avoid_tiles is None:
            avoid_tiles = [WallTile]
        if preferred_tiles is None:
            preferred_tiles = [FloorTile]

        potential_spawns = []
        # Get dimensions from the grid
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        for y in range(height):
            for x in range(width):
                tile = grid[y][x]
                is_suitable = True

                # Check avoid tiles
                for avoid_tile_class in avoid_tiles:
                    if isinstance(tile, avoid_tile_class):
                        is_suitable = False
                        break
                if not is_suitable:
                    continue

                # Check preferred tiles
                is_preferred = False
                for preferred_tile_class in preferred_tiles:
                    if isinstance(tile, preferred_tile_class):
                        is_preferred = True
                        break
                if not is_preferred:
                    continue # Only consider preferred tiles for now

                # Check distance from player if applicable
                if entity_type != "player" and self.game_state.player and min_distance_from_player > 0:
                    player_x, player_y = self.game_state.player.x, self.game_state.player.y
                    distance = ((x - player_x)**2 + (y - player_y)**2)**0.5
                    if distance < min_distance_from_player:
                        is_suitable = False

                if is_suitable:
                    potential_spawns.append((x, y))

        if potential_spawns:
            return random.choice(potential_spawns)
        return None
