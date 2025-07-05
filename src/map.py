import random
from .map_generator import MapGenerator
from .tile_factory import create_tile_from_dict
from .fov import compute_fov

class Map:
    def __init__(self, width, height, map_type="dungeon", generate=True, entry_direction=None, game_state=None):
        self.width = width
        self.height = height
        self.current_map_type = map_type
        self.visible_tiles = set()

        if generate:
            self.grid, self.room_centers, self.next_map_tile_pos = MapGenerator.generate_map(width, height, map_type, entry_direction, game_state)
        else:
            # This part is used when loading a game
            from .tiles import WallTile # Local import to avoid circular dependency
            self.grid = [[WallTile() for _ in range(width)] for _ in range(height)]
            self.room_centers = []
            self.next_map_tile_pos = None

    def update_fov(self, player):
        self.visible_tiles.clear()
        if self.current_map_type == "dungeon":
            self.visible_tiles = compute_fov(self, player.x, player.y, radius=6)
            for x, y in self.visible_tiles:
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.grid[y][x].is_explored = True
        else:
            # For city and other non-dungeon maps, all tiles are visible
            for y in range(self.height):
                for x in range(self.width):
                    self.visible_tiles.add((x, y))

    def to_dict(self):
        grid_data = [[tile.to_dict() for tile in row] for row in self.grid]
        return {
            "width": self.width,
            "height": self.height,
            "grid": grid_data,
            "room_centers": self.room_centers,
            "next_map_tile_pos": self.next_map_tile_pos,
            "current_map_type": self.current_map_type
        }

    def get_random_room_center(self):
        if not self.room_centers:
            return self.width // 2, self.height // 2
        return random.choice(self.room_centers)

    def get_tile_type(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x].character
        return '#'

    def is_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return not self.grid[y][x].is_walkable
        return True

    @classmethod
    def from_dict(cls, data):
        map_type = data.get("current_map_type", "dungeon")
        game_map = cls(data["width"], data["height"], map_type=map_type, generate=False)
        game_map.grid = []
        for row_data in data["grid"]:
            row = []
            for tile_data in row_data:
                row.append(create_tile_from_dict(tile_data))
            game_map.grid.append(row)
        game_map.room_centers = data["room_centers"]
        game_map.next_map_tile_pos = tuple(data["next_map_tile_pos"]) if data["next_map_tile_pos"] else None
        return game_map
