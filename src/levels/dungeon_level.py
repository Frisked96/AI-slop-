import random
from ..tiles import FloorTile, NextMapTile, TrapTile
from .__init__ import Level

# Debug flag to force the 'X' tile to spawn near the player
DEBUG_FORCE_X_TILE_NEAR_PLAYER = False

class DungeonLevel(Level):
    def __init__(self, width, height):
        super().__init__(width, height)

    def generate_map(self, grid, room_centers, next_map_tile_pos, game_state=None):
        rooms = []
        for _ in range(10):
            room_width = random.randint(5, 12)
            room_height = random.randint(5, 12)
            room_x = random.randint(1, self.width - room_width - 1)
            room_y = random.randint(1, self.height - room_height - 1)

            for y in range(room_y, room_y + room_height):
                for x in range(room_x, room_x + room_width):
                    grid[y][x] = FloorTile()
            
            center_x = room_x + room_width // 2
            center_y = room_y + room_height // 2
            rooms.append((center_x, center_y))
            room_centers.append((center_x, center_y))

        for i in range(len(rooms) - 1):
            self._create_corridor(grid, rooms[i], rooms[i+1])

        # Place the next map tile ('?') far from the player's initial spawn
        player_spawn_pos = game_state.spawn_manager.find_spawn_position(grid=grid, entity_type="player")
        if not player_spawn_pos:
            # Fallback if spawn_manager can't find a spot
            player_spawn_pos = (self.width // 2, self.height // 2)
        game_state.player.x, game_state.player.y = player_spawn_pos

        if DEBUG_FORCE_X_TILE_NEAR_PLAYER:
            # Place 'X' tile one step horizontally from the player for debugging
            next_map_tile_pos = (player_spawn_pos[0] + 1, player_spawn_pos[1])
            grid[player_spawn_pos[1]][player_spawn_pos[0] + 1] = NextMapTile()
        else:
            grid, next_map_tile_pos = self._place_random_x_tile(grid, next_map_tile_pos, player_spawn_pos[0], player_spawn_pos[1])

        # Spawn trap tiles
        if game_state and game_state.dungeon_level >= 3:
            self._place_traps(grid, game_state, player_spawn_pos, next_map_tile_pos)

        return grid, room_centers, next_map_tile_pos, player_spawn_pos

    def _place_traps(self, grid, game_state, player_spawn_pos, next_map_tile_pos):
        placed_traps = 0
        max_trap_spawns = 2 # As per requirement

        # Create a list of possible spawn locations (walkable floor tiles)
        possible_spawn_points = []
        for y in range(self.height):
            for x in range(self.width):
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

    def _place_random_x_tile(self, grid, next_map_tile_pos, player_spawn_x, player_spawn_y):
        max_attempts = 1000
        for _ in range(max_attempts):
            tile_x = random.randint(1, self.width - 2)
            tile_y = random.randint(1, self.height - 2)

            if grid[tile_y][tile_x].is_walkable and \
               self._distance((tile_x, tile_y), (player_spawn_x, player_spawn_y)) > (self.width + self.height) / 3:
                next_map_tile_pos = (tile_x, tile_y)
                grid[tile_y][tile_x] = NextMapTile()
                return grid, next_map_tile_pos # Success

        # Fallback: If a distant spot isn't found, place it on the first available floor tile.
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if grid[y][x].is_walkable:
                    next_map_tile_pos = (x, y)
                    grid[y][x] = NextMapTile()
                    return grid, next_map_tile_pos
        return grid, next_map_tile_pos # Should not happen if map is properly initialized

    def _distance(self, p1, p2):
        """Calculates the Euclidean distance between two points."""
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

    def _create_corridor(self, grid, start, end):
        x1, y1 = start
        x2, y2 = end

        # Randomly choose to go horizontal then vertical, or vice versa
        if random.random() < 0.5:
            # Horizontal first
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[y1][x] = FloorTile()
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[y][x2] = FloorTile()
        else:
            # Vertical first
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[y][x1] = FloorTile()
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[y2][x] = FloorTile()