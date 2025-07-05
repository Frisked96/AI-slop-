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

class TrapTile(Tile):
    def __init__(self, character='.', is_walkable=True, is_triggered=False, is_revealed=False): # Default initial character to '.'
        super().__init__(character, is_walkable) # Initialize with character passed by MapGenerator
        self.is_triggered = is_triggered
        self.is_revealed = is_revealed

        # Ensure correct character based on state, especially for loading saves
        if self.is_revealed:
            self.character = '+'
        else:
            # If not revealed, character should be what was passed ('.' or '$'), not '+'
            # This also handles loading a trap that was saved as '$' or '.'
            if self.character == '+': # If for some reason an unrevealed trap has '+', reset it
                self.character = character # Reset to the intended initial char ('.' or '$')
            # No specific 'else' needed here, self.character is already set by super().__init__


    def trigger(self, player, game_state):
        if not self.is_triggered:
            self.is_triggered = True
            player.health -= 2
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
        # Call the parent's from_dict to get a base Tile object or handle character/is_walkable
        # Then, create a TrapTile instance, potentially passing these base attributes
        # or setting them after creation.
        # For simplicity, we'll re-initialize, ensuring new default '$' is considered
        # if 'character' is not in data (e.g. loading very old save)
        # However, if 'character' is in data, respect it (it could be '.' from a previous save, or '+')
        # The __init__ method will then handle adjusting the character based on is_revealed state.
        # Default to '.' if no character is found in save data (very old saves).
        return cls(
            character=data.get("character", '.'), # Use saved character, or default to '.'
            is_walkable=data.get("is_walkable", True),
            is_triggered=data.get("is_triggered", False),
            is_revealed=data.get("is_revealed", False)
        )