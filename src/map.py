import random
from .map_generator import MapGenerator
from .tile_factory import create_tile_from_dict

class Map:
    def __init__(self, width, height, map_type="dungeon", generate=True, entry_direction=None, game_state=None):
        self.width = width
        self.height = height
        self.current_map_type = map_type # Store the current map type

        if generate:
            self.grid, self.room_centers, self.next_map_tile_pos = MapGenerator.generate_map(width, height, map_type, entry_direction, game_state)
        else:
            self.grid = [[WallTile() for _ in range(width)] for _ in range(height)]
            self.room_centers = []
            self.next_map_tile_pos = None

    def to_dict(self):
        # Convert grid of Tile objects to their dictionary representations
        grid_data = [[tile.to_dict() for tile in row] for row in self.grid]
        return {
            "width": self.width,
            "height": self.height,
            "grid": grid_data,
            "room_centers": self.room_centers,
            "next_map_tile_pos": self.next_map_tile_pos
        }

    def get_random_room_center(self):
        if not self.room_centers:
            # Fallback for dungeons, or default for city
            return self.width // 2, self.height // 2
        return random.choice(self.room_centers)

    def get_tile_type(self, x, y):
        """Returns the character at the given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x].character # Return character property
        return '#' # Treat out-of-bounds as walls

    def is_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return not self.grid[y][x].is_walkable # Check is_walkable property
        return True # Treat out-of-bounds as walls

    @classmethod
    def from_dict(cls, data):
        game_map = cls(data["width"], data["height"], generate=False) # Pass generate=False
        # Reconstruct Tile objects from their dictionary representations
        game_map.grid = []
        for row_data in data["grid"]:
            row = []
            for tile_data in row_data:
                row.append(create_tile_from_dict(tile_data))
            game_map.grid.append(row)

        game_map.room_centers = data["room_centers"]
        game_map.next_map_tile_pos = tuple(data["next_map_tile_pos"]) if data["next_map_tile_pos"] else None
        return game_map
