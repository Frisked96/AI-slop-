class Logger:
    def __init__(self, settings_manager):
        self.messages = []
        self.settings_manager = settings_manager
        self.max_messages = self.settings_manager.get_setting("log_max_messages", 5)

    def add_message(self, message):
        """Adds a new message to the log."""
        if len(self.messages) >= self.max_messages:
            self.messages.pop(0)
        self.messages.append(message)

    def get_messages(self):
        """Returns the list of messages."""
        return self.messages
