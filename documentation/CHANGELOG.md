# Changelog

All notable changes to this project will be documented in this file.

## [0.0.3] - 2025-07-05

### Added
- Fog of War system to dungeon maps.
  - Tiles are now either Unseen, Explored, or Visible.
  - A line-of-sight (LOS) algorithm ensures walls correctly block vision.
  - City and sector maps remain fully visible.
- `is_transparent` attribute to all `Tile` subclasses to determine if they block line of sight.
- `fov.py` module containing the line-of-sight calculation logic.
- Trap tiles to dungeon levels (3 and above).
  - Traps are normally hidden ('.') but can be made visible ('$') via a debug setting (`debug_visible_traps` in `settings.json`).
  - Two traps spawn per eligible dungeon map.
  - Traps activate when the player is within a 1-tile radius (including stepping directly on them).
  - Activation reveals the trap as '+' and deals 2 HP damage to the player.
  - Each trap only triggers and damages the player once.
- `debug_visible_traps` setting to `settings.json` and `SettingsManager` to control trap visibility for testing.

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
  - Checks `debug_visible_traps` setting to determine initial trap character ('.' or '$').
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
