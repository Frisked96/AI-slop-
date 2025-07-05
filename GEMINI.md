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
    *   `utils.py`: Provides general utility functions, such as clearing the console screen.
    *   `entity.py`: Defines the base `Entity` class, from which all game characters (player, enemies, NPCs) inherit core attributes like health, attack, and defense.
    *   `command_handler.py`: Centralizes the processing of player input, translating raw commands into game actions.
    *   `interaction_manager.py`: Manages interactions with special map elements and objects (e.g., the next map tile).
    *   `tiles.py`: Defines various tile types (`FloorTile`, `WallTile`, `NextMapTile`, `NorthExitTile`, `EastExitTile`, `SouthExitTile`, `WestExitTile`, `CityCenterEntranceTile`) and their properties (character representation, walkability).
*   `settings.json`: Configuration file for game settings (e.g., autosave interval).
*   `documentation/`: Contains project documentation.
    *   `CHANGELOG.md`: Documents all notable changes.
    *   `progress.md`: Tracks daily progress and game state.
    *   `notebook.md`: Personal notes and tasks.

## 2. Key Design Decisions & Conventions

*   **Object-Oriented Design**: The project heavily utilizes an object-oriented approach, with distinct classes for different game components to promote modularity and reusability.
*   **Modularization**: Functionality is consistently being broken down into smaller, more focused files and classes (e.g., `command_handler`, `interaction_manager`, `tiles`) to improve maintainability and facilitate future expansion.
*   **Text-Based User Interface**: The game renders its environment and information using ASCII characters directly to the console.
*   **Logging System**:
    *   A `Logger` class in `src/logger.py` is responsible for managing all in-game messages.
    *   The `GameState` holds a single instance of the `Logger`.
    *   All parts of the game that need to display a message to the player should do so by calling `game_state.logger.add_message("Your message")`.
    *   The `UIManager` is responsible for *displaying* the log, but not for managing its content. The `GameEngine` calls `ui_manager.display_log()` on each frame.
*   **Player Movement**:
    *   **Vertical Movement**: The player moves 1 tile per input in the vertical direction.
    *   **Horizontal Movement**: The player attempts to move 3 tiles per input in the horizontal direction. If the full 3-tile move is blocked, it attempts a 2-tile move, then a 1-tile move. This ensures the player moves as far as possible in the intended direction.
    *   **Interaction with Special Tiles**: If the first step of a horizontal move lands on a special tile (like the 'X' tile), the player stops on that tile to trigger interaction.
*   **Autosave System**:
    *   Autosave is enabled by default and occurs at a configurable interval (currently 3 steps, defined in `settings.json`).
    *   Autosave notifications are displayed in-game as temporary messages, designed not to interrupt gameplay.
*   **Next Map Tile ('X')**:
    *   Represented by the character 'X' on the map for increased visibility.
    *   When the player lands on the 'X' tile, an action menu is presented via the `InteractionManager`, allowing the player to choose between advancing to the next map or staying on the current map.
    *   The 'X' tile is designed to spawn at a significant distance from the player's initial spawn point (distance > (map width + map height) / 3).
*   **City Map and Navigation**:
    *   The game now starts in a 'city_center' map.
    *   **Exit Tiles (N, E, S, W)**: Placed 3 steps from the edge of the city_center map, these tiles allow travel to corresponding 'outer_city' sectors.
    *   **City Center Entrance Tile (C)**: Placed in 'outer_city' sectors, this tile allows return to the 'city_center' map.
    *   Interaction with these tiles triggers a dynamic prompt and uses the `InteractionManager`'s `travel` method to load the appropriate map and reposition the player.
*   **Player Attributes**: The `Player` class now inherits from the `Entity` base class, providing core attributes such as `health`, `max_health`, `attack`, and `defense`. These are displayed on the game screen.
*   **Settings Menu**:
    *   The settings menu is now managed by the `GameEngine` and `UIManager`, ensuring a consistent look and feel with other menus.
    *   The settings menu allows the player to toggle autosave, set the autosave interval, and set the map width and height.
*   **Item System**:
    *   `item.py`: Defines the base `Item` class and its subclasses (e.g., `Weapon`, `Sword`).
    *   `item_factory.py`: Centralizes the creation of item instances from data.
*   **Spawn Management**:
    *   `spawn_manager.py`: Provides a centralized and reusable system for finding suitable spawn positions for entities on a map.
*   **Debug Features**: A temporary debug flag `DEBUG_FORCE_X_TILE_NEAR_PLAYER` exists in `map.py`. When set to `True`, it forces the 'X' tile to spawn one step horizontally from the player's starting position for easier testing of interactions. This flag should generally remain `False` unless actively debugging.

## 3. Future Expansion Considerations

*   **Item System**: Planned for `item.py` to manage collectible and usable items.
*   **Enemy System**: Planned for `enemy.py` to define various enemy types and their behaviors.
*   **Enhanced UI**: Potential for a dedicated message log area to prevent screen clutter.
*   **Structured Game Data**: Further externalization of game content (e.g., enemy stats, item properties) into data files.
*   **Event System**: Consideration for a more advanced event handling mechanism for complex game interactions.

