from .ui_manager import UIManager

class BlacksmithMenu:
    def __init__(self, game_state):
        self.game_state = game_state
        self.ui_manager = UIManager()
        self.options = [
            "Buy",
            "Sell",
            "Upgrade",
            "Exit"
        ]

    def display(self):
        self.ui_manager.clear_screen()
        self.ui_manager.display_message("\n--- Blacksmith Shop ---")
        for i, option in enumerate(self.options):
            self.ui_manager.display_message(f"{i+1}. {option}")
        self.ui_manager.display_message("-----------------------")

    def handle_input(self, choice):
        if choice == "1":
            self.game_state.logger.add_message("You browse the wares.")
        elif choice == "2":
            self.game_state.logger.add_message("You offer items for sale.")
        elif choice == "3":
            self.game_state.logger.add_message("You consider upgrading your gear.")
        elif choice == "4":
            self.game_state.logger.add_message("You leave the blacksmith shop.")
            self.game_state.current_menu = None # Exit the blacksmith menu
        else:
            self.game_state.logger.add_message("Invalid choice.")