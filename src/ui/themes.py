import curses

# Define color constants
COLOR_CREAM = 250  # A light, off-white color
COLOR_BROWN = 94   # A dark brown color
COLOR_DARK_GRAY = 235 # Hex for a very dark gray
COLOR_GRASS_GREEN = 22 # A green color for grass
COLOR_MUD_BROWN = 58 # A darker brown for mud
COLOR_ROCK_GRAY = 242 # A medium gray for rock
COLOR_RUBBLE_GRAY = 248 # A lighter gray for rubble
COLOR_BLACK = curses.COLOR_BLACK # Define black for clarity
COLOR_DARK_BLUE = 17 # A dark blue color

def init_colors():
    curses.init_pair(1, curses.COLOR_BLACK, COLOR_CREAM) # Default background
    curses.init_pair(2, COLOR_CREAM, COLOR_BROWN) # Floor tiles
    curses.init_pair(3, curses.COLOR_WHITE, COLOR_BLACK) # Explored tiles (light black background)
    curses.init_pair(4, curses.COLOR_WHITE, COLOR_DARK_GRAY) # Wall tiles
    curses.init_pair(5, curses.COLOR_BLACK, COLOR_GRASS_GREEN) # Grass tiles
    curses.init_pair(6, curses.COLOR_BLACK, COLOR_MUD_BROWN) # Mud tiles
    curses.init_pair(7, curses.COLOR_BLACK, COLOR_ROCK_GRAY) # Rock tiles
    curses.init_pair(8, curses.COLOR_CYAN, COLOR_DARK_BLUE) # Water tiles
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK) # Next Map Tile (X) - Red on Black
    curses.init_pair(10, curses.COLOR_WHITE, COLOR_BROWN) # Corridor tiles
    curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_BLACK) # Unexplored tiles - now uses BLACK as background
    curses.init_pair(12, curses.COLOR_BLACK, COLOR_RUBBLE_GRAY) # Rubble tiles (moved from 8)

# Define color pair constants
COLOR_PAIR_DEFAULT = 1
COLOR_PAIR_FLOOR = 2
COLOR_PAIR_EXPLORED = 3
COLOR_PAIR_WALL = 4
COLOR_PAIR_GRASS = 5
COLOR_PAIR_MUD = 6
COLOR_PAIR_ROCK = 7
COLOR_PAIR_WATER = 8 # Water is now color pair 8
COLOR_PAIR_NEXT_MAP_TILE = 9
COLOR_PAIR_CORRIDOR = 10
COLOR_PAIR_UNEXPLORED = 11
COLOR_PAIR_RUBBLE = 12 # Rubble is now color pair 12