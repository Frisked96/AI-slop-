class ShopMenu:
    def __init__(self, game_state, title, options):
        self.game_state = game_state
        self.ui_manager = game_state.ui_manager
        self.title = title
        self.options = options

    def display(self):
        self.ui_manager.clear_screen()
        self.ui_manager.display_message(0, 0, f"--- {self.title} ---")
        for i, option in enumerate(self.options):
            self.ui_manager.display_message(i + 2, 0, f"{i+1}. {option}")
        self.ui_manager.display_message(len(self.options) + 2, 0, "-----------------------")

    def handle_input(self, choice):
        raise NotImplementedError


