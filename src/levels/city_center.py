import random
from ..tiles import FloorTile, WallTile, NextMapTile, NorthExitTile, EastExitTile, SouthExitTile, WestExitTile, CityCenterEntranceTile, DoorTile, BlacksmithShopTile
from .__init__ import Level

class CityCenterLevel(Level):
    def __init__(self, width, height):
        super().__init__(width, height)

    def generate_map(self, grid, room_centers, next_map_tile_pos, entry_direction=None, game_state=None):
        # Fill the entire map with floor tiles
        for y in range(self.height):
            for x in range(self.width):
                grid[y][x] = FloorTile()

        # Place the 'X' tile to enter the dungeon (still exists in city center)
        dungeon_entrance_x = self.width // 2
        dungeon_entrance_y = self.height // 2
        grid[dungeon_entrance_y][dungeon_entrance_x] = NextMapTile()
        next_map_tile_pos = (dungeon_entrance_x, dungeon_entrance_y)

        # Place North exit (N)
        grid[2][self.width // 2] = NorthExitTile()
        # Place East exit (E)
        grid[self.height // 2][self.width - 3] = EastExitTile()
        # Place South exit (S)
        grid[self.height - 3][self.width // 2] = SouthExitTile()
        # Place West exit (W)
        grid[self.height // 2][2] = WestExitTile()

        # --- Blacksmith Shop ---
        # Top-left corner of the shop
        shop_start_x = 1
        shop_start_y = 1
        shop_width = 12 # Increased width for "BLACKSMITH"
        shop_height = 7 # Increased height for more space

        # Place top and bottom walls
        for x in range(shop_start_x, shop_start_x + shop_width):
            grid[shop_start_y][x] = WallTile() # Top wall
            grid[shop_start_y + shop_height - 1][x] = WallTile() # Bottom wall

        # Place side walls
        for y in range(shop_start_y, shop_start_y + shop_height):
            grid[y][shop_start_x] = WallTile() # Left wall
            grid[y][shop_start_x + shop_width - 1] = WallTile() # Right wall

        # Place the word "BLACKSMITH" inside the shop using BlacksmithShopTile
        blacksmith_word = "BLACKSMITH"
        word_start_x = shop_start_x + 1 # Start one tile in from the left wall
        word_start_y = shop_start_y + 3 # Place it roughly in the middle vertically

        for i, char in enumerate(blacksmith_word):
            grid[word_start_y][word_start_x + i] = BlacksmithShopTile(char=char) # Use BlacksmithShopTile with specific character

        # Place the Blacksmith Shop entrance tile
        grid[shop_start_y + 3][shop_start_x + shop_width - 1] = FloorTile() # Changed to FloorTile

        # Place the doorway (East exit from the shop)
        grid[shop_start_y + 3][shop_start_x + shop_width] = DoorTile() # Changed to DoorTile

        # Fixed player spawn position near the 'X' tile
        player_spawn_pos = (dungeon_entrance_x + 1, dungeon_entrance_y)
        room_centers.append(player_spawn_pos)

        return grid, room_centers, next_map_tile_pos, player_spawn_pos