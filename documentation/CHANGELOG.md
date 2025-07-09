# Changelog

**RULE: All updates on the same day should be added to the same version.**
**RULE: Changes made within the `test` directory will not be logged here. Only features or fixes integrated from `test` into the main application will be documented.**

All notable changes to this project will be documented in this file.

## [0.0.6] - 2025-07-08

### Added
- Minimap feature: `MinimapMenu` class for displaying a scaled-down, explored view of the dungeon.
- Minimap integration: Added 'm' command to `src/command_handler.py` to access the minimap.
- Minimap rendering: Minimap now shows rooms as blocks and corridors as brown paths.
- Minimap exploration: Minimap updates as the player explores the main map.
- Load game functionality: Implemented `load_game` method in `src/menu.py` to load saved games.
- Player stats and wellbeing: Added `level`, `hunger`, `thirst`, `comfort`, `heartrate`, and `weight_carried` attributes to `Player` class.
- Player stats display: Implemented display of new player stats and wellbeing on the right side of the screen in `UIManager.display_player_stats`.
- Unexplored map background: Set background of unexplored areas on the map to dark blue.

### Changed
- `MinimapMenu` initialization: Adjusted initialization order to ensure `MinimapMenu` is created after `game_map`.
- `Map` constructor: Re-added `game_state` parameter to `Map` constructor and ensured it's passed correctly.
- `Map` `from_dict`: Updated to load `room_coords` and `corridor_coords`.
- `SaveManager.load_game`: Modified to return `GameState` object directly.
- `SettingsManager.get_setting`: Simplified default value logic.
- `SettingsManager` error logging: Replaced `print` statements with `logger.add_message`.
- `SettingsMenu.handle_input`: Extracted repetitive input loops into a helper method.
- `ShopMenu.display`: Added `y` and `x` coordinates to `display_message` calls.
- `SpawnManager.find_spawn_position`: Updated default `preferred_tiles` and adjusted logic.
- `UIManager.init_ui`: Moved `init_colors()` call into `UIManager.init_ui()`.
- `UIManager.display_map`: Adjusted player color to match tile background.
- `Menu.run`: Removed `curses.napms` call for better responsiveness.
- `UIManager.clear_screen`: Changed to `erase()` for potentially smoother updates.
- `UIManager.refresh`: Changed to `curses.doupdate()` for optimized screen updates.
- `UIManager.get_string`: Modified to use `noutrefresh()` and `doupdate()` for flicker-free input.
- `themes.py`: Added `COLOR_DARK_BLUE` and `COLOR_PAIR_UNEXPLORED`.

### Removed
- Blacksmith shop: All related code and references (imports, instantiations, command handling, interaction logic, `BlacksmithMenu` class, `DoorTile`).
- `Player._attempt_move`: Removed unused method.
- `CommandHandler._handle_special_tile_command`: Removed unused method.
- `COLOR_PAIR_DEFAULT` import from `main.py`.
- `Map` and `Player` imports from `main.py`.
- `MinimapMenu` redundant initialization from `GameEngine.__init__` and `Menu.load_game`.
- `map_width` and `map_height` return from `SaveManager.load_game`.
- `WarningMenu.display` return value.
- Redundant `COLOR_CORRIDOR_BROWN` definition.

### Fixed
- `AttributeError: 'MinimapMenu' object has no attribute 'options'` in `src/game_engine.py`.
- `TypeError: UIManager.get_string() missing 1 required positional argument: 'x'` in `src/command_handler.py`.
- `NameError: name 'game_state' is not defined` in `src/map.py`.
- `NameError: name 'MinimapMenu' is not defined` in `src/menu.py`.
- `TypeError: Player.__init__() takes 3 positional arguments but 6 were given` when loading a game.
- `NameError: name 'GameState' is not defined` in `src/save_manager.py`.
- `AttributeError: 'WallTile' object has no attribute 'x'` in `minimap_menu.py`.
- Tiles not having color due to incorrect `curses` initialization order.
- Pylance warnings related to `None` attributes and `get_input` vs `get_string`.
- Screen tearing: Implemented `noutrefresh()` and `doupdate()` pattern to reduce screen tearing.

## [0.0.5] - 2025-07-07

### Added
- Map generation parameters (`num_rooms`, `min_room_size`, `max_room_size`) added to `settings.json` for configurable dungeon layouts.
- Implemented combined Minimum Spanning Tree (MST) and K-Nearest Neighbors (KNN) algorithms for corridor generation in `src/levels/dungeon_level.py` to ensure full map connectivity and more varied layouts.
- Implemented a basic Event System (`src/event_manager.py`) to facilitate decoupled communication between game components.
- `EventManager` integrated into `main.py` and `GameState`.
- `Logger` now subscribes to a 'game_message' event, demonstrating basic event system usage.
- Implemented a camera system to display a portion of the larger map, following the player.
    - `camera_width` and `camera_height` settings added to `settings.json`.
    - `UIManager` updated to render map and position UI elements based on camera view.

### Changed
- `DungeonLevel.generate_map` now retrieves map generation parameters from `settings.json`.
- `DungeonLevel.generate_map` now uses MST for guaranteed room connectivity and KNN for additional corridor paths.
- `NextMapTile` placement logic updated to ensure it spawns furthest from the player's initial position in dungeon levels.
- Initial player spawn location confirmed to be in the city (`city_center` map type).
- Floor tile foreground color changed to `COLOR_CREAM` for better visibility.
- Wall tile color changed to `COLOR_DARK_GRAY` for improved visual distinction.
- Game flow modified to be a pure dungeon-descending experience.
    - New game starts directly in a dungeon, bypassing city and sector maps.
    - `MapGenerator` updated to only generate dungeon levels.
    - `Menu` updated to initiate dungeon directly.
- Map generation parameters (`num_rooms`) in `settings.json` increased to 50.

### Removed
- City and sector map files (`src/levels/city_center.py`, `src/levels/east_sector.py`, `src/levels/north_sector.py`, `src/levels/south_sector.py`, `src/levels/west_sector.py`).
- All related code for city and sector maps, including:
    - References in `src/map_generator.py`.
    - Unused tile classes (`NorthExitTile`, `EastExitTile`, `SouthExitTile`, `WestExitTile`, `CityCenterEntranceTile`, `BlacksmithShopTile`) from `src/tiles.py` and `src/tile_factory.py`.
    - Interaction logic for city/sector exits and blacksmith shop from `src/interaction_manager.py`.
    - Blacksmith command handling from `src/command_handler.py`.
- Obsolete `_check_terminal_size` method from `src/menu.py`.
- Unused `last_key_pressed`, `key_held_down`, `last_horizontal_move_time`, and `last_vertical_move_time` attributes from `src/game_state.py`.
- Redundant `get_key` method from `src/ui/ui_manager.py`.

### Fixed
- `AttributeError: 'FloorTile' object has no attribute 'transparent'` by correcting the attribute name to `is_transparent` in the FOV check.
- `SyntaxError: unmatched ')'` in `src/tiles.py` caused by corrupted code.
- Player no longer spawns in complete darkness; the initial view is now correctly rendered.
- Walls outside the player's view are no longer incorrectly revealed.
- `AttributeError: 'NoneType' object has no attribute 'current_map_type'` during initial map generation by correctly using the `map_type` parameter in `MapGenerator` for trap spawning conditions.
- `AttributeError: 'InteractionManager' object has no attribute 'is_player_in_blacksmith_shop'` by removing the obsolete call in `src/command_handler.py`.
- `_curses.error: addwstr() returned ERR` by correcting positioning logic in `src/ui/ui_manager.py` and `src/menu.py`.
- `UnboundLocalError` by correcting the initialization order of `settings_manager` and camera dimensions in `main.py`.
- Missing `display_save_screen` and `display_blacksmith_shop_prompt` methods in `src/ui/ui_manager.py`.

### Refactored
- Moved trap spawning logic from `src/map_generator.py` to `src/levels/dungeon_level.py` to better align with project conventions.
- Changed `TrapTile.trigger` to use `player.take_damage()` method for consistency.
- Moved `BlacksmithMenu` from its own file to `src/shop_menus.py`.
- Renamed `BlacksmithMenu` to `ShopMenu` and created a `BlacksmithMenu` subclass.

## [0.0.4] - 2025-07-06

### Added
- Map generation parameters (`num_rooms`, `min_room_size`, `max_room_size`) added to `settings.json` for configurable dungeon layouts.
- Implemented combined Minimum Spanning Tree (MST) and K-Nearest Neighbors (KNN) algorithms for corridor generation in `src/levels/dungeon_level.py` to ensure full map connectivity and more varied layouts.
- Implemented a basic Event System (`src/event_manager.py`) to facilitate decoupled communication between game components.
- `EventManager` integrated into `main.py` and `GameState`.
- `Logger` now subscribes to a 'game_message' event, demonstrating basic event system usage.

### Changed
- `DungeonLevel.generate_map` now retrieves map generation parameters from `settings.json`.
- `DungeonLevel.generate_map` now uses MST for guaranteed room connectivity and KNN for additional corridor paths.
- `NextMapTile` placement logic updated to ensure it spawns furthest from the player's initial position in dungeon levels.
- Initial player spawn location confirmed to be in the city (`city_center` map type).
- Floor tile foreground color changed to `COLOR_CREAM` for better visibility.
- Wall tile color changed to `COLOR_DARK_GRAY` for improved visual distinction.

## [0.0.4] - 2025-07-06

### Added
- Integration of `curses` library for screen refreshing to eliminate flickering.
- `UIManager.get_key()` for single key press input.
- `UIManager.get_string()` for string input with manual echoing and line clearing.
- `last_key_pressed` and `key_held_down` attributes to `GameState` for input debouncing.

### Changed
- Player horizontal movement in dungeons changed back to one tile per move.
- `main.py` updated to initialize `curses` and use `curses.halfdelay(1)` for non-blocking input with a timeout.
- `UIManager` updated to use `curses` functions for drawing and input, and to explicitly clear input lines in `get_string()`.
- `Menu` and `SettingsMenu` updated to use `UIManager.get_string()` for menu input.
- `GameEngine` updated to use `UIManager.get_key()` and implement input debouncing logic to prevent continuous movement.
- Implemented continuous movement with different delays for horizontal (0.3s) and vertical (0.5s) movement.
- Player's background color now matches the tile they are on.
- Explored tiles (out of FOV) now have a light black background.

### Fixed
- Flickering screen issue due to `print`-based rendering.
- Continuous movement/teleporting issue when holding down movement keys.
- Main menu UI prompt appearing on the same line as the last option.
- `TypeError: UIManager.__init__() missing 1 required positional argument: 'stdscr'` in `ShopMenu` by ensuring it uses the existing `UIManager` instance from `game_state`.
- `AttributeError: 'UIManager' object has no attribute 'get_input'` in `SaveManager` by updating to `get_string()`.
- `AttributeError: '_curses.window' object has no attribute 'halfdelay'` by calling `curses.halfdelay()` directly.
- Flickering white box with '?' in input prompts by manually handling echoing and clearing input lines in `UIManager.get_string()`.
- `ModuleNotFoundError` for `src/ui/tiles` by correcting import path.
- `NameError` for `COLOR_PAIR_DEFAULT` by importing it into `ui_manager.py`.
- `NameError` for `FloorTile` by importing it into `ui_manager.py`.

### Other
- Increased the number of traps spawned to 10 and made them start spawning from dungeon level 1.
- Created `src/ui/` directory and `src/ui/themes.py` for color management.
- `curses` color initialization and color pairs for default, floor, and explored tiles.

## [0.0.3] - 2025-07-05

### Added
- Fog of War system to dungeon levels.
  - Tiles are now either Unseen, Explored, or Visible.
  - A line-of-sight (LOS) algorithm ensures walls correctly block vision.
  - City and sector maps remain fully visible.
- `is_transparent` attribute to all `Tile` subclasses to determine if they block line of sight.
- `fov.py` module containing the line-of-sight calculation logic.
- Trap tiles to dungeon levels (3 and above).
  - Traps are normally hidden ('.') but can be made visible ('$') via a debug setting (`debug_visible_traps` in `settings.json`).
  - Two traps spawn per eligible dungeon map.
  - Traps activate when the player moves within a 1-tile radius (including stepping directly on them).
  - Each trap only triggers and damages the player once.
- `debug_visible_traps` setting to `settings.json` and `SettingsManager` to control trap visibility for testing.
- Added a movement system comparison table to `documentation/notebook.md`.

### Changed
- `Map` class now manages the visibility grid and updates the Field of View (FOV) when the player moves.
- `UIManager` now renders the map based on the tile's visibility state (Visible, Explored, or Unseen).
- `Player` class now initializes with `moved=True` to ensure the initial FOV is calculated on the first frame.
- `SaveManager` now correctly saves and loads the `is_explored` state of tiles.
- `TrapTile` class in `src/tiles.py`:
  - Character defaults to `.` but can be set to `'$'` for debug mode via `MapGenerator`.
  - Manages its own revealed state and appearance ('+').
  - Trigger logic ensures it only activates once.
- `MapGenerator` in `src/map_generator.py`:
  - Spawns trap tiles on valid floor locations in dungeon levels 3+.
  - Checks `debug_visible_traps` setting to determine initial trap character ('.', or '$').
  - Removed logging of trap placement coordinates.
- `InteractionManager` in `src/interaction_manager.py`:
  - Handles proximity-based activation of trap tiles.
  - Triggers trap reveal and damage when player is within 1-tile radius.
- `UIManager` in `src/ui_manager.py`:
  - Simplified map display logic to rely on `tile.character` for all tiles, as `TrapTile` now manages its own character display.

### Fixed
- `AttributeError: 'FloorTile' object has no attribute 'transparent'` by correcting the attribute name to `is_transparent` in the FOV check.
- `SyntaxError: unmatched ')'` in `src/tiles.py` caused by corrupted code.
- Player no longer spawns in complete darkness; the initial view is now correctly rendered.
- Walls outside the player's view are no longer incorrectly revealed.
- `AttributeError: 'NoneType' object has no attribute 'current_map_type'` during initial map generation by correctly using the `map_type` parameter in `MapGenerator` for trap spawning conditions.

### Refactored
- Moved trap spawning logic from `src/map_generator.py` to `src/levels/dungeon_level.py` to better align with project conventions.
- Changed `TrapTile.trigger` to use `player.take_damage()` method for consistency.
- Moved `BlacksmithMenu` from its own file to `src/shop_menus.py`.
- Renamed `BlacksmithMenu` to `ShopMenu` and created a `BlacksmithMenu` subclass.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2025-07-04

### Added
- In-game settings menu, accessible by pressing 'o' during gameplay.
- Re-implemented the `DEBUG_FORCE_X_TILE_NEAR_PLAYER` flag in `src/levels/dungeon_level.py` for testing purposes.
- Added map width and height settings to the in-game settings menu.
- Implemented `Weapon` superclass in `src/item.py`.
- Implemented `Sword` class in `src/item.py`.
- Updated `item_factory.py` to handle `Weapon` and `Sword` creation.
- Created `SpawnManager` for centralized entity spawning logic.

### Changed
- The save game screen now displays a list of existing saves before prompting for a filename, improving user experience.
- The `DEBUG_FORCE_X_TILE_NEAR_PLAYER` flag is now passed through the map generation process to ensure it works correctly.
- Refactored `SettingsMenu` to integrate with `GameEngine` and `UIManager` for consistent menu handling.
- Updated `GameEngine`, `UIManager`, `GameState`, and `Menu` to support the refactored settings menu.
- Modified `SettingsMenu` to prevent changing map dimensions while in-game.
- Refactored player spawn logic to use `SpawnManager` for robust placement in both city and dungeon maps.
- Modified `InteractionManager._transition_map` to correctly pass `game_state` to `Map` constructor.

### Fixed
- Corrected a `TypeError` that occurred when starting a new game due to a missing `player_spawn` argument in the `CityCenterLevel.generate_map` method.
- The `DEBUG_FORCE_X_TILE_NEAR_PLAYER` functionality now correctly places the 'X' tile next to the player's spawn point in the dungeon.
- Corrected the settings menu not displaying properly while in-game.
- Fixed `SyntaxError` in `src/settings_manager.py` due to incorrect triple-quoted string usage.
- Fixed `NameError: name 'Weapon' is not defined` by reordering class definitions in `src/item.py`.
- Fixed player spawning on walls in city and dungeon maps.
- Fixed "ghost blacksmith" issue by checking map type in `is_player_in_blacksmith_shop()`.
- Fixed `AttributeError: 'NoneType' object has no attribute 'spawn_manager'` by correcting initialization order in `main.py`.
- Fixed `NameError: map_width not defined` by re-adding `map_width` and `map_height` definitions in `main.py`.
- Fixed `ValueError: too many values to unpack` by adjusting return values in `MapGenerator.generate_map` and level `generate_map` methods.
- Fixed `AttributeError: 'NoneType' object has no attribute 'player'` by ensuring `game_state.player` is initialized before map generation.
- Fixed `TypeError: Map.__init__() got an unexpected keyword argument 'player_spawn'` by updating `InteractionManager._transition_map`.
- Added option to go back to game from save menu.

## [0.0.1] - 2025-07-03

### Added
- Initial project structure with core modules for game engine, map, player, and save management.
- Text-based user interface using ASCII characters.
- Player movement mechanics (1 tile vertical, up to 3 tiles horizontal).
- Configurable autosave system with in-game notifications.
- 'X' tile for advancing to the next map, with a special interaction menu.
- City map (`city_center`) with exits to outer sectors.
- Player attributes (`health`, `attack`, `defense`) inherited from a base `Entity` class.
- `GameState` class to centralize game state management.
- `UIManager` to handle all UI interactions.
- `CommandHandler` to process player input.
- `InteractionManager` to manage interactions with special tiles.
- `Logger` for in-game messages.
- `BlacksmithMenu` and `InventoryMenu`.
- `CHANGELOG.md` and `GEMINI.md` for project documentation.

### Changed
- Refactored map generation logic into `map_generator.py`.
- Centralized tile creation in `tile_factory.py`.
- Refactored `CommandHandler` and `Player.move` for better readability.
- Centralized UI interactions into the `UIManager`.
- Improved autosave logic with an `autosave_overwrite_behavior` setting.

### Removed
- `utils.py` file, with its functionality absorbed into `UIManager`.
- The original `DEBUG_FORCE_X_TILE_NEAR_PLAYER` flag (before it was re-added).