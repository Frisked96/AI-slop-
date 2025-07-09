# Project Context for Dungeon Crawler Python

This `GEMINI.md` file stores project-specific information and conventions to assist the Gemini CLI agent in providing accurate and context-aware support for the `dungeon_crawler_python` project.

## 1. Project Structure & Key Files

*   `main.py`: The primary entry point for starting the game.
*   `src/`: Contains the core game logic and modules.
    *   `game_engine.py`: Contains the core game loop, handles rendering, and orchestrates main game logic.
    *   `map.py`: Responsible for dungeon generation, including room and corridor creation, and managing tile objects.
    *   `player.py`: Defines the player character, including movement logic and attributes.
    *   `save_manager.py`: Manages saving and loading game states.
    *   `settings_manager.py`: Handles game settings, loading from and saving to `settings.json`.
    *   `logger.py`: Contains the `Logger` class for managing game messages.
    *   `entity.py`: Defines the base `Entity` class, from which all game characters (player, enemies, NPCs) inherit core attributes like health, attack, and defense.
    *   `command_handler.py`: Centralizes the processing of player input, translating raw commands into game actions.
    *   `interaction_manager.py`: Manages interactions with special map elements and objects (e.g., the next map tile).
    *   `tiles.py`: Defines various tile types (`FloorTile`, `WallTile`, `NextMapTile`, `TrapTile`) and their properties.
    *   `shop_menus.py`: Defines the base `ShopMenu` class and its subclasses.
    *   `item.py`: Defines the base `Item` class and its subclasses (e.g., `Weapon`, `Sword`).
    *   `item_factory.py`: Centralizes the creation of item instances from data.
    *   `spawn_manager.py`: Provides a centralized and reusable system for finding suitable spawn positions for entities on a map.
    *   `fov.py`: Contains the line-of-sight calculation logic for the Fog of War system.
    *   `event_manager.py`: Implements a basic event system for decoupled communication between game components.
*   `test/`: Contains test builds and custom builds for experimental features.
    *   `test.py`: The entry point for running test builds.
    *   `test_diary.md`: Documents tests, findings, and results.
*   `settings.json`: Configuration file for game settings.
*   `documentation/`: Contains project documentation.
    *   `CHANGELOG.md`: Documents all notable changes.
    *   `progress.md`: Tracks daily progress and game state.
    *   `notebook.md`: Personal notes and tasks.

## 2. Key Design Decisions & Conventions

*   **Object-Oriented Design**: The project heavily utilizes an object-oriented approach, with distinct classes for different game components.
*   **Modularization**: Functionality is broken down into smaller, focused files and classes.
*   **Text-Based User Interface**: The game renders its environment and information using ASCII characters, now utilizing the `curses` library for flicker-free screen updates.
*   **Input Handling**: Implemented a debouncing mechanism to ensure turn-based input, preventing continuous movement when a key is held down. Input is now processed one key press at a time.
*   **Player Movement**: Vertical movement is 1 tile per input. Horizontal movement is 1 tile per input in dungeons.
*   **Dungeon Only**: The game now exclusively features procedurally generated dungeon maps. Players start directly in a dungeon and continue descending.
*   **Camera System**: A camera system is implemented to follow the player, displaying only a portion of the larger map.
*   **Shop System**:
    *   A base `ShopMenu` class is defined in `src/shop_menus.py`.
    
*   **Trap System**:
    *   `TrapTile` objects are placed in dungeons.
    *   They are hidden by default and trigger when the player moves within a 1-tile radius.
    *   A debug flag `debug_visible_traps` in `settings.json` can make them visible for testing.
*   **Fog of War**:
    *   A line-of-sight (LOS) based fog of war system is implemented for dungeon maps.
    *   Tiles can be in one of three states: Unseen, Explored, or Visible.
*   **Map Generation**:
    *   Dungeon maps are now generated using a combination of Minimum Spanning Tree (MST) and K-Nearest Neighbors (KNN) algorithms for corridor creation, ensuring full connectivity and more varied layouts.
    *   Map generation parameters (`num_rooms`, `min_room_size`, `max_room_size`) are configurable via `settings.json`.
*   **Event System**: A basic event manager is implemented to allow for decoupled communication between various game components.
*   **Debug Features**: A `DEBUG_FORCE_X_TILE_NEAR_PLAYER` flag in `map.py` allows for easier testing of the 'X' tile interaction.

## 3. Future Expansion Considerations

*   **Enemy System**: Planned for `enemy.py` to define various enemy types and their behaviors.
*   **Enhanced UI**: Potential for a dedicated message log area to prevent screen clutter.
*   **Natural Map Features**: Addition of rivers, lakes, and varied terrain.
*   **Structured Game Data**: Further externalization of game content (e.g., enemy stats, item properties) into data files.
