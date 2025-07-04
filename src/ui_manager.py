import os
from .tiles import TrapTile # Ensure TrapTile is imported at the top

class UIManager:
    def __init__(self):
        pass

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_message(self, message):
        print(message)

    def get_input(self, prompt):
        return input(prompt)

    def display_map(self, game_map, player):
        self.clear_screen()
        for y in range(game_map.height):
            row_str = ""
            for x in range(game_map.width):
                tile = game_map.grid[y][x]
                if (x, y) in game_map.visible_tiles:
                    if x == player.x and y == player.y:
                        row_str += '@'
                    else:
                        row_str += tile.character
                elif tile.is_explored:
                    # Render explored tiles with a shaded character
                    row_str += '░'
                else:
                    row_str += ' '  # Unseen tiles
            print(row_str)

    def display_player_stats(self, player, game_state):
        stats_string = f"Health: {player.health}/{player.max_health} Attack: {player.attack} Defense: {player.defense}"
        if game_state and game_state.game_map and game_state.game_map.current_map_type == "dungeon":
            stats_string += f" Dungeon Level: {game_state.dungeon_level}"
        print(stats_string)

    def display_log(self, messages):
        print("\n--- Log ---")
        for msg in messages:
            print(msg)
        print("-----------")

    def display_menu(self, menu_options, title=None):
        self.clear_screen()
        if title:
            print(f"\n--- {title} ---")
        for key, value in menu_options.items():
            print(f"{key}. {value}")

    def display_save_screen(self, existing_saves):
        self.clear_screen()
        print("--- Save Game ---")
        if existing_saves:
            print("Existing saves:")
            for save_name in existing_saves:
                print(f"  - {save_name}")
        else:
            print("No existing saves.")
        print("-----------------")
        print("Enter save filename (or 'b' to go back to game): ")

    def display_blacksmith_shop_prompt(self):
        print("Blacksmith Shop")
        print("Press 'b' to enter Blacksmith Shop.")

    def display_settings_menu(self, settings_manager, options, is_in_game=False):
        self.clear_screen()
        print("\n--- Settings ---")
        print(f"Autosave Enabled: {settings_manager.get_setting('autosave_enabled')}")
        print(f"Autosave Interval: {settings_manager.get_setting('autosave_interval')} steps")
        if not is_in_game:
            print(f"Map Width: {settings_manager.get_setting('map_width')}")
            print(f"Map Height: {settings_manager.get_setting('map_height')}")
        for key, value in options.items():
            print(f"{key}. {value}")
