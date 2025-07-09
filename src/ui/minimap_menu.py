import curses
from .themes import COLOR_PAIR_FLOOR, COLOR_PAIR_WALL, COLOR_PAIR_EXPLORED, COLOR_PAIR_NEXT_MAP_TILE, COLOR_PAIR_DEFAULT, COLOR_PAIR_GRASS, COLOR_PAIR_MUD, COLOR_PAIR_ROCK, COLOR_PAIR_RUBBLE, COLOR_PAIR_CORRIDOR
from ..world.tiles import WallTile, NextMapTile, TrapTile, FloorTile, GrassTile, MudTile, RockTile, RubbleTile

class MinimapMenu:
    def __init__(self, game_state):
        self.game_state = game_state
        self.title = "Minimap"
        self.minimap_grid = []
        self.x_scale = 1
        self.y_scale = 1
        self._generate_initial_minimap_grid()

    def _generate_initial_minimap_grid(self):
        game_map = self.game_state.game_map
        ui_manager = self.game_state.ui_manager

        self.x_scale = max(1, game_map.width // ui_manager.camera_width)
        self.y_scale = max(1, game_map.height // ui_manager.camera_height)

        self.minimap_grid = [[{'char': ' ', 'color': curses.color_pair(COLOR_PAIR_DEFAULT), 'explored': False} for _ in range(ui_manager.camera_width)] for _ in range(ui_manager.camera_height)]

        for my in range(len(self.minimap_grid)):
            for mx in range(len(self.minimap_grid[0])):
                start_x, start_y = mx * self.x_scale, my * self.y_scale
                block_tiles = []
                for y_offset in range(self.y_scale):
                    for x_offset in range(self.x_scale):
                        map_x, map_y = start_x + x_offset, start_y + y_offset
                        if 0 <= map_x < game_map.width and 0 <= map_y < game_map.height:
                            block_tiles.append((game_map.grid[map_y][map_x], map_x, map_y))

                char, color_pair, is_explored = ' ', curses.color_pair(COLOR_PAIR_DEFAULT), False
                tile_types = {type(t) for t, _, _ in block_tiles}
                coords = {(tx, ty) for _, tx, ty in block_tiles}

                if NextMapTile in tile_types:
                    char, color_pair = 'X', curses.color_pair(COLOR_PAIR_NEXT_MAP_TILE)
                elif coords & game_map.room_coords:
                    char, color_pair = '█', curses.color_pair(COLOR_PAIR_FLOOR)
                elif coords & game_map.corridor_coords:
                    char, color_pair = '.', curses.color_pair(COLOR_PAIR_CORRIDOR)
                elif WallTile in tile_types:
                    char, color_pair = '#', curses.color_pair(COLOR_PAIR_WALL)
                elif any(t in tile_types for t in [FloorTile, GrassTile, MudTile, RockTile, RubbleTile]):
                    char, color_pair = '.', curses.color_pair(COLOR_PAIR_FLOOR)
                
                if any(t.is_explored for t, _, _ in block_tiles):
                    is_explored = True

                self.minimap_grid[my][mx] = {'char': char, 'color': color_pair, 'explored': is_explored}

    def update_minimap_explored_status(self, map_x, map_y):
        mm_x, mm_y = map_x // self.x_scale, map_y // self.y_scale
        if 0 <= mm_y < len(self.minimap_grid) and 0 <= mm_x < len(self.minimap_grid[0]):
            self.minimap_grid[mm_y][mm_x]['explored'] = True

    def display(self):
        self.game_state.ui_manager.clear_screen()
        self.game_state.ui_manager.display_message(0, 0, f"--- {self.title} ---")
        player, ui_manager = self.game_state.player, self.game_state.ui_manager
        player_mm_x, player_mm_y = player.x // self.x_scale, player.y // self.y_scale

        for my, row in enumerate(self.minimap_grid):
            for mx, cell in enumerate(row):
                char, color = ('@', curses.color_pair(COLOR_PAIR_DEFAULT)) if my == player_mm_y and mx == player_mm_x else (cell['char'], cell['color'])
                if not cell['explored']:
                    char, color = ('#', curses.color_pair(COLOR_PAIR_EXPLORED)) if cell['char'] == '#' else (' ', color)
                
                try:
                    ui_manager.stdscr.addch(my + 2, mx, char, color)
                except curses.error:
                    pass
        self.game_state.ui_manager.display_message(ui_manager.camera_height - 1, 0, "Press 'm' or 'q' to exit minimap.")

    def handle_input(self, key):
        if key in ['m', 'q']:
            self.game_state.current_menu = None
            return True
        return False
