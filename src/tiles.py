class Tile:
    def __init__(self, character, is_walkable):
        self.character = character
        self.is_walkable = is_walkable

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "character": self.character,
            "is_walkable": self.is_walkable
        }

    @classmethod
    def from_dict(cls, data):
        # This method will be called by subclasses to reconstruct themselves
        return cls(data["character"], data["is_walkable"])

class FloorTile(Tile):
    def __init__(self):
        super().__init__('.', True)

class WallTile(Tile):
    def __init__(self):
        super().__init__('#', False)

class NextMapTile(Tile):
    def __init__(self):
        super().__init__('X', True)

class NorthExitTile(Tile):
    def __init__(self):
        super().__init__('N', True)

class EastExitTile(Tile):
    def __init__(self):
        super().__init__('E', True)

class SouthExitTile(Tile):
    def __init__(self):
        super().__init__('S', True)

class WestExitTile(Tile):
    def __init__(self):
        super().__init__('W', True)

class CityCenterEntranceTile(Tile):
    def __init__(self):
        super().__init__('C', True)

class BlacksmithShopTile(Tile):
    def __init__(self, char='B'):
        super().__init__(char, True)

class DoorTile(Tile):
    def __init__(self):
        super().__init__('\\', True)