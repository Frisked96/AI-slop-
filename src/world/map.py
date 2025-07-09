import random
from .map_generator import MapGenerator
from .tile_factory import create_tile_from_dict
from ..systems.fov import compute_fov

class Map:
    def __init__(self, width, height, map_type="dungeon", generate=True, entry_direction=None, game_state=None, grid=None, room_centers=None, next_map_tile_pos=None, room_coords=None, corridor_coords=None):
        self.width = width
        self.height = height
        self.current_map_type = map_type
        self.visible_tiles = set()
        self.game_state = game_state
        self.room_coords = set()
        self.corridor_coords = set()

        if generate:
            self.grid, self.room_centers, self.next_map_tile_pos, _, self.room_coords, self.corridor_coords = MapGenerator.generate_map(width, height, map_type, entry_direction, game_state)
        elif grid is not None:
            self.grid = grid
            self.room_centers = room_centers if room_centers is not None else []
            self.next_map_tile_pos = next_map_tile_pos
            self.room_coords = room_coords if room_coords is not None else set()
            self.corridor_coords = corridor_coords if corridor_coords is not None else set()
        else:
            from .tiles import WallTile
            self.grid = [[WallTile() for _ in range(width)] for _ in range(height)]
            self.room_centers = []
            self.next_map_tile_pos = None

    def update_fov(self, player):
        self.visible_tiles.clear()
        if self.current_map_type == "dungeon":
            self.visible_tiles = compute_fov(self, player.x, player.y, radius=6, last_direction=player.last_direction)
            for x, y in self.visible_tiles:
                if 0 <= x < self.width and 0 <= y < self.height:
                    if not self.grid[y][x].is_explored:
                        self.grid[y][x].is_explored = True
                        if self.game_state and self.game_state.minimap_menu:
                            self.game_state.minimap_menu.update_minimap_explored_status(x, y)
        else:
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
            "current_map_type": self.current_map_type,
            "room_coords": list(self.room_coords),
            "corridor_coords": list(self.corridor_coords)
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
    def from_dict(cls, data, settings_manager):
        map_type = data.get("current_map_type", "dungeon")
        game_map = cls(data["width"], data["height"], map_type=map_type, generate=False)
        game_map.grid = [[create_tile_from_dict(tile_data) for tile_data in row_data] for row_data in data["grid"]]
        game_map.room_centers = data["room_centers"]
        game_map.next_map_tile_pos = tuple(data["next_map_tile_pos"]) if data["next_map_tile_pos"] else None
        game_map.room_coords = set(map(tuple, data.get("room_coords", [])))
        game_map.corridor_coords = set(map(tuple, data.get("corridor_coords", [])))
        return game_map
