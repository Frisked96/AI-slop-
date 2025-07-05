from abc import ABC, abstractmethod

import random

class Level(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @abstractmethod
    def generate_map(self, grid, room_centers, next_map_tile_pos, game_state=None):
        pass

    def is_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return not self.grid[y][x].is_walkable
        return True

    def get_tile_type(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x].character
        return '#'

    def get_random_room_center(self):
        if not self.room_centers:
            return self.width // 2, self.height // 2
        return random.choice(self.room_centers)
