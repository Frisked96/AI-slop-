class Logger:
    def __init__(self, settings_manager):
        self.messages = []
        self.settings_manager = settings_manager
        self.max_messages = self.settings_manager.get_setting("log_max_messages", 5)

    def add_message(self, message):
        if len(self.messages) >= self.max_messages:
            self.messages.pop(0)
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def log_tile_info(self, tile):
        if tile:
            self.add_message(f"You are standing on {tile.description}.")
        else:
            self.add_message("You are in the void.")
