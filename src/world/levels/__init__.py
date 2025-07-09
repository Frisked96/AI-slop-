from abc import ABC, abstractmethod

class Level(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @abstractmethod
    def generate_map(self, grid, room_centers, next_map_tile_pos, game_state=None):
        pass
