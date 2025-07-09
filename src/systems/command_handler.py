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
        max_y, max_x = self.game_state.ui_manager.stdscr.getmaxyx()
        prompt_y = max_y - 1
        filename = self.game_state.ui_manager.get_string(prompt_y, 0, "Enter filename to save (or 'b' to go back): ").strip().lower()
        if filename == 'b':
            self.game_state.logger.add_message("Save cancelled. Returning to game.")
            return False
        if not filename:
            self.game_state.logger.add_message("Save cancelled.")
            return False

        game_state_data = self.game_state.to_dict()
        message = self.game_state.save_manager.save_game(game_state_data, filename)
        self.game_state.logger.add_message(message)
        return True

    def _handle_inventory_command(self):
        # TODO: Implement inventory menu
        pass

    def _handle_settings_command(self):
        # TODO: Implement settings menu
        pass

    def _handle_minimap_command(self):
        # TODO: Implement minimap
        pass

    def _check_and_perform_autosave(self, moved, prev_x, prev_y):
        if not moved:
            return

        if self.game_state.settings_manager.get_setting("autosave_enabled"):
            self.game_state.step_count += 1
            if self.game_state.step_count >= self.game_state.settings_manager.get_setting("autosave_interval"):
                game_state_data = self.game_state.to_dict()
                message = self.game_state.save_manager.save_game(game_state_data, "autosave", is_autosave=True)
                self.game_state.logger.add_message(message)
                self.game_state.step_count = 0

    def handle_command(self, key):
        if key is None:
            return

        self.game_state.current_message = None
        moved = False
        prev_x, prev_y = self.game_state.player.x, self.game_state.player.y

        if key in ['w', 'a', 's', 'd']:
            self.game_state.player.last_direction = key
            moved, prev_x, prev_y = self._handle_movement_command(key)
        elif (key == '\n' or key == 'KEY_ENTER') and self.game_state.player.last_direction:
            moved, prev_x, prev_y = self._handle_movement_command(self.game_state.player.last_direction)
        elif key == 'y' and self.game_state.on_special_tile:
            self.game_state.interaction_manager.travel()
            return
        elif key == 'q':
            self._handle_quit_command()
            return
        elif key == 'p':
            self._handle_save_command()
            return
        elif key == 'i':
            self._handle_inventory_command()
            return
        elif key == 'o':
            self._handle_settings_command()
            return
        elif key == 'm':
            self._handle_minimap_command()
            return
        else:
            self.game_state.logger.add_message("Invalid command.")
            return

        self._check_and_perform_autosave(moved, prev_x, prev_y)
