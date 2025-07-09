import curses
from ..world.tiles import TrapTile, FloorTile, GrassTile, MudTile, RockTile, RubbleTile
from .themes import init_colors, COLOR_PAIR_FLOOR, COLOR_PAIR_DEFAULT, COLOR_PAIR_EXPLORED, COLOR_PAIR_WALL, COLOR_PAIR_GRASS, COLOR_PAIR_MUD, COLOR_PAIR_ROCK, COLOR_PAIR_RUBBLE, COLOR_PAIR_NEXT_MAP_TILE, COLOR_PAIR_UNEXPLORED

class UIManager:
    def __init__(self, stdscr, camera_width, camera_height):
        self.stdscr = stdscr
        self.stdscr.keypad(True)
        self.camera_width = camera_width
        self.camera_height = camera_height
        # self.stdscr.nodelay(True) # Make getkey() blocking

    def init_ui(self):
        curses.start_color()
        curses.use_default_colors()
        init_colors() # Call init_colors here


    def clear_screen(self):
        self.stdscr.erase()

    def display_message(self, y, x, message):
        try:
            self.stdscr.addstr(y, x, message)
        except curses.error:
            pass

    def get_key_if_available(self):
        key_code = self.stdscr.getch()

        if key_code == -1:
            return None  # No input

        # A key was pressed. Immediately flush the rest of the input buffer
        # to prevent the "ghost movement" lag.
        curses.flushinp()

        # Convert the key code to a more usable string format
        if key_code == curses.KEY_UP:
            return 'w'
        elif key_code == curses.KEY_DOWN:
            return 's'
        elif key_code == curses.KEY_LEFT:
            return 'a'
        elif key_code == curses.KEY_RIGHT:
            return 'd'
        elif key_code in [curses.KEY_ENTER, 10, 13]:
            return '\n'
        elif 32 <= key_code <= 126:
            return chr(key_code)
        else:
            # For other special keys, you might want to return their names
            # This part can be expanded as needed.
            return str(key_code)

    def get_string(self, y, x, prompt=""):
        self.stdscr.addstr(y, x, prompt)
        self.stdscr.noutrefresh()
        curses.doupdate()

        s = ""
        curses.curs_set(1)
        max_y, max_x = self.stdscr.getmaxyx()
        prompt_len = len(prompt)

        while True:
            key = self.stdscr.getch()

            if key in [curses.KEY_ENTER, 10, 13]:
                break
            elif key in [curses.KEY_BACKSPACE, 127, 8]:
                if len(s) > 0:
                    s = s[:-1]
                    curr_y, curr_x = self.stdscr.getyx()
                    self.stdscr.move(curr_y, curr_x - 1)
                    self.stdscr.delch()
                    self.stdscr.noutrefresh()
                    curses.doupdate()
            elif 32 <= key <= 126:
                # Check if there is space to add the new character
                if x + prompt_len + len(s) < max_x - 1:
                    s += chr(key)
                    self.stdscr.addch(key)
                    self.stdscr.noutrefresh()
                    curses.doupdate()

        curses.curs_set(0)
        return s

    def display_map(self, game_map, player, game_state):
        # Calculate camera's top-left corner
        camera_x = max(0, min(player.x - self.camera_width // 2, game_map.width - self.camera_width))
        camera_y = max(0, min(player.y - self.camera_height // 2, game_map.height - self.camera_height))

        for y in range(self.camera_height):
            for x in range(self.camera_width):
                map_x, map_y = camera_x + x, camera_y + y
                tile = game_map.grid[map_y][map_x]
                is_visible = (map_x, map_y) in game_map.visible_tiles
                is_player_on = (map_x, map_y) == (player.x, player.y)
                
                tile.render(self.stdscr, y, x, is_visible, is_player_on, game_state, map_x, map_y)

    def display_player_stats(self, player, game_state):
        # Calculate starting X position for stats on the right side
        stats_start_x = self.camera_width + 2 # 2 columns of padding from the map
        current_y = 0
        state = player.state # Get the state object for easier access

        # Basic Stats
        self.display_message(current_y, stats_start_x, "--- Player Stats ---")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Class: {player.player_class_name or 'Ordinary Man'}")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Health: {state.health}/{state.max_health}")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Mana: {state.mana}/{state.max_mana}")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Stamina: {state.stamina}/{state.max_stamina}")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Attack: {state.attack}")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Defense: {state.defense}")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Level: {state.level}")
        current_y += 1

        # Vitals
        current_y += 1 
        self.display_message(current_y, stats_start_x, "--- Vitals ---")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Hunger: {state.hunger:.0f}%")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Thirst: {state.thirst:.0f}%")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Comfort: {state.comfort}%")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Heartrate: {state.heartrate} BPM")
        current_y += 1
        self.display_message(current_y, stats_start_x, f"Weight: {state.weight_carried:.1f} lbs")
        current_y += 1

        # Status Effects
        effects = player.get_status_effects()
        if effects:
            current_y += 1
            self.display_message(current_y, stats_start_x, "--- Effects ---")
            current_y += 1
            for effect in effects:
                self.display_message(current_y, stats_start_x, f"- {effect}")
                current_y += 1

        # Dungeon Level (if applicable)
        if game_state and game_state.game_map and game_state.game_map.current_map_type == "dungeon":
            current_y += 1 # Add a blank line for separation
            self.display_message(current_y, stats_start_x, f"Dungeon Level: {game_state.dungeon_level}")

    def display_log(self, messages, game_state):
        y_offset = 1
        self.display_message(self.camera_height + y_offset, 0, "--- Log ---")
        for i, msg in enumerate(messages):
            self.display_message(self.camera_height + y_offset + 1 + i, 0, msg)
        self.display_message(self.camera_height + y_offset + len(messages) + 1, 0, "-----------")

    def display_save_screen(self, saves):
        self.clear_screen()
        self.display_message(1, 0, "--- Available Saves ---")
        if not saves:
            self.display_message(3, 0, "No saves found.")
        else:
            for i, save_name in enumerate(saves):
                self.display_message(3 + i, 0, f"- {save_name}")
        self.display_message(self.camera_height + 1, 0, "Enter filename to save or load (or 'b' to go back):")

    def display_menu(self, menu_options, title=None):
        y_offset = 1
        if title:
            self.display_message(y_offset, 0, f"--- {title} ---")
            y_offset += 2
        for i, (key, value) in enumerate(menu_options.items()):
            self.display_message(y_offset + i, 0, f"{key}. {value}")

    def refresh(self):
        curses.doupdate()