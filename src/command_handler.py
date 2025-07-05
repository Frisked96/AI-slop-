




class CommandHandler:
    def __init__(self, game_state):
        self.game_state = game_state

    def _handle_movement_command(self, key):
        prev_x, prev_y = self.game_state.player.x, self.game_state.player.y
        moved = False
        if key == 'w':
            self.game_state.player.move(0, -1, self.game_state.game_map)
            moved = True
        elif key == 's':
            self.game_state.player.move(0, 1, self.game_state.game_map)
            moved = True
        elif key == 'a':
            self.game_state.player.move(-1, 0, self.game_state.game_map)
            moved = True
        elif key == 'd':
            self.game_state.player.move(1, 0, self.game_state.game_map)
            moved = True
        return moved, prev_x, prev_y

    def _handle_quit_command(self):
        self.game_state.is_running = False
        return False

    def _handle_save_command(self):
        available_saves = self.game_state.save_manager.list_saves()
        self.game_state.ui_manager.display_save_screen(available_saves)
        filename = self.game_state.ui_manager.get_input("").strip().lower()
        if filename == 'b':
            self.game_state.logger.add_message("Save cancelled. Returning to game.")
            return False
        if not filename:
            self.game_state.logger.add_message("Save cancelled.")
            return False

        game_state_data = {
            "player": self.game_state.player.to_dict(),
            "map": self.game_state.game_map.to_dict(),
            "map_width": self.game_state.game_map.width,
            "map_height": self.game_state.game_map.height,
            "log": self.game_state.logger.get_messages()
        }
        message = self.game_state.save_manager.save_game(game_state_data, filename)
        self.game_state.logger.add_message(message)
        return False

    def _handle_blacksmith_command(self):
        if self.game_state.interaction_manager.is_player_in_blacksmith_shop():
            self.game_state.current_menu = self.game_state.blacksmith_menu
        return False

    def _handle_inventory_command(self):
        self.game_state.current_menu = self.game_state.inventory_menu
        return False

    def _handle_settings_command(self):
        self.game_state.game_engine.display_settings_menu()
        return False

    def _handle_special_tile_command(self, key, tile_char):
        if key == 'y':
            self.game_state.interaction_manager.travel()
            return False
        return False

    def _check_and_perform_autosave(self, moved, prev_x, prev_y):
        if moved and (self.game_state.player.x != prev_x or self.game_state.player.y != prev_y):
            self.game_state.step_count += 1
            if self.game_state.settings_manager.get_setting("autosave_enabled") and \
               self.game_state.step_count >= self.game_state.settings_manager.get_setting("autosave_interval"):
                game_state_data = {
                    "player": self.game_state.player.to_dict(),
                    "map": self.game_state.game_map.to_dict(),
                    "map_width": self.game_state.game_map.width,
                    "map_height": self.game_state.game_map.height,
                    "log": self.game_state.logger.get_messages()
                }
                message = self.game_state.save_manager.save_game(game_state_data, "autosave", is_autosave=True)
                self.game_state.logger.add_message(message)
                self.game_state.step_count = 0
            return True
        return False

    def handle_command(self):
        # Clear any previous temporary message at the start of a new command handling cycle
        self.game_state.current_message = None

        moved = False
        prev_x, prev_y = self.game_state.player.x, self.game_state.player.y

        # Display blacksmith prompt if applicable
        if self.game_state.interaction_manager.is_player_in_blacksmith_shop() and not self.game_state.current_menu:
            self.game_state.ui_manager.display_blacksmith_shop_prompt()

        if self.game_state.on_special_tile:
            tile_char = self.game_state.interaction_manager.current_interaction_tile.character
            prompt_message = ""
            if tile_char == 'X':
                prompt_message = "(y to go to dungeon)"
            elif tile_char == 'N':
                prompt_message = "(y to travel to North Sector)"
            elif tile_char == 'E':
                prompt_message = "(y to travel to East Sector)"
            elif tile_char == 'S':
                prompt_message = "(y to travel to South Sector)"
            elif tile_char == 'W':
                prompt_message = "(y to travel to West Sector)"
            elif tile_char == 'C':
                prompt_message = "(y to return to City Center)"

            key = self.game_state.ui_manager.get_input(f"Enter a command (w/a/s/d to move, {prompt_message}): ").lower()
            if key == 'y':
                self.game_state.interaction_manager.travel()
                return
            elif key in ['w', 'a', 's', 'd']:
                moved, prev_x, prev_y = self._handle_movement_command(key)
            else:
                self.game_state.logger.add_message("Invalid command. Please use w/a/s/d to move or y to advance.")
                return
        else:
            key = self.game_state.ui_manager.get_input("Enter a command (w/a/s/d to move, q to quit, p to save, i for inventory, o for settings): ").lower()

            if key in ['w', 'a', 's', 'd']:
                moved, prev_x, prev_y = self._handle_movement_command(key)
            elif key == 'q':
                self._handle_quit_command()
                return
            elif key == 'p':
                self._handle_save_command()
                return
            elif key == 'b':
                self._handle_blacksmith_command()
                return
            elif key == 'i':
                self._handle_inventory_command()
                return
            elif key == 'o':
                self._handle_settings_command()
                return
            else:
                self.game_state.logger.add_message("Invalid command. Please use w/a/s/d to move, q to quit, p to save, b for blacksmith, i for inventory, or o for settings.")
                return

        self._check_and_perform_autosave(moved, prev_x, prev_y)
