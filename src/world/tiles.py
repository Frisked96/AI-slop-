import curses
from ..ui.themes import COLOR_PAIR_CORRIDOR, COLOR_PAIR_EXPLORED, COLOR_PAIR_FLOOR, COLOR_PAIR_GRASS, COLOR_PAIR_MUD, COLOR_PAIR_NEXT_MAP_TILE, COLOR_PAIR_ROCK, COLOR_PAIR_RUBBLE, COLOR_PAIR_UNEXPLORED, COLOR_PAIR_WALL

class Tile:
    def __init__(self, character, is_walkable, is_transparent, description="an ordinary tile"):
        self.character = character
        self.is_walkable = is_walkable
        self.is_transparent = is_transparent
        self.is_explored = False
        self.description = description

    def render(self, stdscr, y, x, is_visible, is_player_on, game_state=None, map_x=None, map_y=None):
        # This method will be overridden by subclasses
        pass

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "character": self.character,
            "is_walkable": self.is_walkable,
            "is_transparent": self.is_transparent,
            "is_explored": self.is_explored
        }

class FloorTile(Tile):
    def __init__(self):
        super().__init__('.', True, True, "a stone floor")

    def render(self, stdscr, y, x, is_visible, is_player_on, game_state=None, map_x=None, map_y=None):
        char = self.character
        color_pair = curses.color_pair(COLOR_PAIR_FLOOR)
        if is_player_on:
            char = '@'
        elif is_visible:
            pass # Keep default char and color
        elif self.is_explored:
            char = '░'
            color_pair = curses.color_pair(COLOR_PAIR_EXPLORED)
        else:
            char = ' '
            color_pair = curses.color_pair(COLOR_PAIR_UNEXPLORED)
        
        try:
            stdscr.addch(y, x, char, color_pair)
        except curses.error:
            pass

class WallTile(Tile):
    # Define the box-drawing characters based on neighbors
    # (up, down, left, right) -> character
    _BOX_CHARS = {
        (False, False, False, False): '#', # Default if no neighbors (shouldn't happen much)
        (True, False, False, False): '│', # Up
        (False, True, False, False): '│', # Down
        (False, False, True, False): '─', # Left
        (False, False, False, True): '─', # Right

        (True, True, False, False): '│', # Up, Down
        (False, False, True, True): '─', # Left, Right

        (True, False, True, False): '┘', # Up, Left
        (True, False, False, True): '└', # Up, Right
        (False, True, True, False): '┐', # Down, Left
        (False, True, False, True): '┌', # Down, Right

        (True, True, True, False): '┤', # Up, Down, Left
        (True, True, False, True): '├', # Up, Down, Right
        (True, False, True, True): '┴', # Up, Left, Right
        (False, True, True, True): '┬', # Down, Left, Right

        (True, True, True, True): '┼', # All
    }

    def __init__(self):
        super().__init__('#', False, False, "a solid wall")

    def _get_wall_character(self, game_map, map_x, map_y):
        # Check neighbors
        up = (map_y > 0 and isinstance(game_map.grid[map_y - 1][map_x], WallTile))
        down = (map_y < game_map.height - 1 and isinstance(game_map.grid[map_y + 1][map_x], WallTile))
        left = (map_x > 0 and isinstance(game_map.grid[map_y][map_x - 1], WallTile))
        right = (map_x < game_map.width - 1 and isinstance(game_map.grid[map_y][map_x + 1], WallTile))

        # Return the appropriate character based on neighbors
        return self._BOX_CHARS.get((up, down, left, right), '#') # Default to '#' if not found

    def render(self, stdscr, y, x, is_visible, is_player_on, game_state=None, map_x=None, map_y=None):
        char = self.character
        color_pair = curses.color_pair(COLOR_PAIR_WALL)
        if is_visible:
            # If visible, determine the correct box-drawing character
            if game_state and game_state.game_map and map_x is not None and map_y is not None:
                char = self._get_wall_character(game_state.game_map, map_x, map_y)
            else:
                char = self.character # Fallback to default if game_map or map_coords not available
        elif self.is_explored:
            color_pair = curses.color_pair(COLOR_PAIR_EXPLORED)
            if game_state and game_state.game_map and map_x is not None and map_y is not None:
                char = self._get_wall_character(game_state.game_map, map_x, map_y)
            else:
                char = self.character # Fallback
        else:
            char = ' '
            color_pair = curses.color_pair(COLOR_PAIR_UNEXPLORED)

        try:
            stdscr.addch(y, x, char, color_pair)
        except curses.error:
            pass

class NextMapTile(Tile):
    def __init__(self):
        super().__init__('X', True, True, "an exit to the next area")

    def render(self, stdscr, y, x, is_visible, is_player_on, game_state=None, map_x=None, map_y=None):
        char = self.character
        color_pair = curses.color_pair(COLOR_PAIR_NEXT_MAP_TILE)
        if is_player_on:
            char = '@'
        elif is_visible:
            pass
        elif self.is_explored:
            char = '░'
            color_pair = curses.color_pair(COLOR_PAIR_EXPLORED)
        else:
            char = ' '
            color_pair = curses.color_pair(COLOR_PAIR_UNEXPLORED)

        try:
            stdscr.addch(y, x, char, color_pair)
        except curses.error:
            pass

class GrassTile(Tile):
    def __init__(self):
        super().__init__('.', True, True, "a patch of grass")

    def render(self, stdscr, y, x, is_visible, is_player_on, game_state=None, map_x=None, map_y=None):
        char = self.character
        color_pair = curses.color_pair(COLOR_PAIR_GRASS)
        if is_player_on:
            char = '@'
        elif is_visible:
            pass
        elif self.is_explored:
            char = '░'
            color_pair = curses.color_pair(COLOR_PAIR_EXPLORED)
        else:
            char = ' '
            color_pair = curses.color_pair(COLOR_PAIR_UNEXPLORED)

        try:
            stdscr.addch(y, x, char, color_pair)
        except curses.error:
            pass

class MudTile(Tile):
    def __init__(self):
        super().__init__('.', True, True, "a patch of mud")

    def render(self, stdscr, y, x, is_visible, is_player_on, game_state=None, map_x=None, map_y=None):
        char = self.character
        color_pair = curses.color_pair(COLOR_PAIR_MUD)
        if is_player_on:
            char = '@'
        elif is_visible:
            pass
        elif self.is_explored:
            char = '░'
            color_pair = curses.color_pair(COLOR_PAIR_EXPLORED)
        else:
            char = ' '
            color_pair = curses.color_pair(COLOR_PAIR_UNEXPLORED)

        try:
            stdscr.addch(y, x, char, color_pair)
        except curses.error:
            pass

class RockTile(Tile):
    def __init__(self):
        super().__init__('.', True, True, "a rocky area")

    def render(self, stdscr, y, x, is_visible, is_player_on, game_state=None, map_x=None, map_y=None):
        char = self.character
        color_pair = curses.color_pair(COLOR_PAIR_ROCK)
        if is_player_on:
            char = '@'
        elif is_visible:
            pass
        elif self.is_explored:
            char = '░'
            color_pair = curses.color_pair(COLOR_PAIR_EXPLORED)
        else:
            char = ' '
            color_pair = curses.color_pair(COLOR_PAIR_UNEXPLORED)

        try:
            stdscr.addch(y, x, char, color_pair)
        except curses.error:
            pass

class RubbleTile(Tile):
    def __init__(self):
        super().__init__('.', True, True, "a pile of rubble")

    def render(self, stdscr, y, x, is_visible, is_player_on, game_state=None, map_x=None, map_y=None):
        char = self.character
        color_pair = curses.color_pair(COLOR_PAIR_RUBBLE)
        if is_player_on:
            char = '@'
        elif is_visible:
            pass
        elif self.is_explored:
            char = '░'
            color_pair = curses.color_pair(COLOR_PAIR_EXPLORED)
        else:
            char = ' '
            color_pair = curses.color_pair(COLOR_PAIR_UNEXPLORED)

        try:
            stdscr.addch(y, x, char, color_pair)
        except curses.error:
            pass

class TrapTile(Tile):
    def __init__(self, character='.', is_walkable=True, is_triggered=False, is_revealed=False):
        super().__init__(character, is_walkable, True, "a suspicious-looking floor tile")
        self.is_triggered = is_triggered
        self.is_revealed = is_revealed
        if self.is_revealed:
            self.character = '+'
            self.description = "a triggered trap"

    def render(self, stdscr, y, x, is_visible, is_player_on, game_state=None, map_x=None, map_y=None):
        char = self.character
        color_pair = curses.color_pair(COLOR_PAIR_FLOOR)
        if is_player_on:
            char = '@'
        elif is_visible:
            if game_state and game_state.settings_manager.get_setting("debug_visible_traps"):
                color_pair = curses.color_pair(curses.COLOR_RED)
        elif self.is_explored:
            char = '░'
            color_pair = curses.color_pair(COLOR_PAIR_EXPLORED)
        else:
            char = ' '
            color_pair = curses.color_pair(COLOR_PAIR_UNEXPLORED)

        try:
            stdscr.addch(y, x, char, color_pair)
        except curses.error:
            pass

    def trigger(self, player, game_state):
        if not self.is_triggered:
            self.is_triggered = True
            player.take_damage(2)
            if game_state and game_state.logger:
                game_state.logger.add_message("A trap was triggered! You lost 2 HP.")
            self.reveal()
            return True
        return False

    def reveal(self):
        if not self.is_revealed:
            self.is_revealed = True
        self.character = '+'

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


import time

class WaterTile(Tile):
    def __init__(self):
        super().__init__('~', True, True, "deep water")

    def render(self, stdscr, y, x, is_visible, is_player_on, game_state=None, map_x=None, map_y=None):
        char = self.character
        color_pair = curses.color_pair(COLOR_PAIR_CORRIDOR)
        if is_player_on:
            char = '@'
        elif is_visible:
            pass
        elif self.is_explored:
            char = '░'
            color_pair = curses.color_pair(COLOR_PAIR_EXPLORED)
        else:
            char = ' '
            color_pair = curses.color_pair(COLOR_PAIR_UNEXPLORED)

        try:
            stdscr.addch(y, x, char, color_pair)
        except curses.error:
            pass


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
        return cls()

