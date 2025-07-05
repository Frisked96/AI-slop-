from ..tiles import FloorTile, CityCenterEntranceTile
from .__init__ import Level

class NorthSectorLevel(Level):
    def __init__(self, width, height):
        super().__init__(width, height)

    def generate_map(self, grid, room_centers, next_map_tile_pos, entry_direction=None, game_state=None):
        # Fill the entire map with floor tiles
        for y in range(self.height):
            for x in range(self.width):
                grid[y][x] = FloorTile()

        # Place the City Center Entrance tile ('C') based on entry_direction
        grid[self.height - 3][self.width // 2] = CityCenterEntranceTile()
        
        # Fixed player spawn position for North Sector
        player_spawn_pos = (self.width // 2, self.height - 4) # Spawn just above 'C'
        room_centers.append(player_spawn_pos)

        return grid, room_centers, next_map_tile_pos, player_spawn_pos