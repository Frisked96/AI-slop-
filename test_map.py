from src.map import Map
import msvcrt # For Windows-specific non-blocking input
import time # For a small delay
import os # For clearing the console

# Mock classes to satisfy dependencies for map generation
class MockSpawnManager:
    def find_spawn_position(self, grid, entity_type):
        # Return a dummy spawn position for testing purposes
        return (1, 1)  # A safe default position

class MockPlayer:
    def __init__(self):
        self.x = 0
        self.y = 0

class MockSettingsManager:
    def __init__(self):
        self.debug_visible_traps = False # Add any settings attributes that are accessed
        self.num_rooms = 20
        self.min_room_size = 5
        self.max_room_size = 10

    def get_setting(self, setting_name, default_value):
        return getattr(self, setting_name, default_value)

class MockGameState:
    def __init__(self):
        self.spawn_manager = MockSpawnManager()
        self.player = MockPlayer()
        self.dungeon_level = 1
        self.settings_manager = MockSettingsManager() # Added settings_manager attribute

def generate_and_display_map():
    # Create a mock game_state object
    mock_game_state = MockGameState()

    # Create a map instance, passing the mock game_state
    game_map = Map(width=80, height=25, map_type="dungeon", generate=True, game_state=mock_game_state)

    # Clear console before printing new map
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Generated Map:")
    for y in range(game_map.height):
        row_str = ""
        for x in range(game_map.width):
            row_str += game_map.grid[y][x].character
        print(row_str)

if __name__ == "__main__":
    print("Press 'w' to generate a new map, 'q' to quit.")
    generate_and_display_map()

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'w':
                print("\nGenerating new map...")
                generate_and_display_map()
            elif key == 'q':
                print("Exiting.")
                break
        time.sleep(0.1) # Small delay to prevent busy-waiting
