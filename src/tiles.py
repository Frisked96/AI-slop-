class Tile:
    def __init__(self, character, is_walkable, is_transparent):
        self.character = character
        self.is_walkable = is_walkable
        self.is_transparent = is_transparent
        self.is_explored = False

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "character": self.character,
            "is_walkable": self.is_walkable,
            "is_transparent": self.is_transparent,
            "is_explored": self.is_explored
        }

    @classmethod
    def from_dict(cls, data):
        # This method will be called by subclasses to reconstruct themselves
        tile = cls(data["character"], data["is_walkable"], data.get("is_transparent", True))
        tile.is_explored = data.get("is_explored", False)
        return tile

class FloorTile(Tile):
    def __init__(self):
        super().__init__('.', True, True)

class WallTile(Tile):
    def __init__(self):
        super().__init__('#', False, False)

class NextMapTile(Tile):
    def __init__(self):
        super().__init__('X', True, True)

class NorthExitTile(Tile):
    def __init__(self):
        super().__init__('N', True, True)

class EastExitTile(Tile):
    def __init__(self):
        super().__init__('E', True, True)

class SouthExitTile(Tile):
    def __init__(self):
        super().__init__('S', True, True)

class WestExitTile(Tile):
    def __init__(self):
        super().__init__('W', True, True)

class CityCenterEntranceTile(Tile):
    def __init__(self):
        super().__init__('C', True, True)

class BlacksmithShopTile(Tile):
    def __init__(self, char='B'):
        super().__init__(char, True, True)

class DoorTile(Tile):
    def __init__(self):
        super().__init__('\\', True, False)



class TrapTile(Tile):
    def __init__(self, character='.', is_walkable=True, is_triggered=False, is_revealed=False): # Default initial character to '.'
        super().__init__(character, is_walkable, True) # Traps are transparent
        self.is_triggered = is_triggered
        self.is_revealed = is_revealed

        # Ensure correct character based on state, especially for loading saves
        if self.is_revealed:
            self.character = '+'
        else:
            # If not revealed, character should be what was passed ('.' or '$')
            if self.character == '+': # If for some reason an unrevealed trap has '+', reset it
                self.character = character # Reset to the intended initial char ('.' or '$')

    def trigger(self, player, game_state):
        if not self.is_triggered:
            self.is_triggered = True
            player.take_damage(2)
            if game_state and game_state.logger:
                game_state.logger.add_message("A trap was triggered! You lost 2 HP.")
            self.reveal() # Reveal when triggered
            return True # Indicate successful trigger
        return False # Already triggered

    def reveal(self):
        if not self.is_revealed: # Only change character and set flag if not already revealed
            self.is_revealed = True
        self.character = '+' # Change character when revealed

    def to_dict(self):
        data = super().to_dict()
        data["is_triggered"] = self.is_triggered
        data["is_revealed"] = self.is_revealed
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            character=data.get("character", '.'),
            is_walkable=data.get("is_walkable", True),
            is_triggered=data.get("is_triggered", False),
            is_revealed=data.get("is_revealed", False)
        )
