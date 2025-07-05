import os

class InventoryMenu:
    def __init__(self, player, game_state):
        self.player = player
        self.game_state = game_state
        self.update_options()

    def update_options(self):
        self.options = [
            (f"{item.name} - {item.description}", self.use_item, item) for item in self.player.inventory
        ]
        self.options.append(("Back", self.deactivate, None))

    def use_item(self, item):
        if item:
            item.use(self.player)
            self.player.inventory.remove(item)
            self.update_options() # Refresh menu after using an item

    def deactivate(self):
        self.game_state.current_menu = None

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Inventory")
        print("=========")
        if not self.player.inventory:
            print("Your inventory is empty.")
        for i, (option_text, _, _) in enumerate(self.options):
            print(f"{i + 1}. {option_text}")
        print("\nUse number keys to select an option.")

    def handle_input(self, key):
        try:
            choice = int(key)
            if 1 <= choice <= len(self.options):
                _, action, item = self.options[choice - 1]
                if item:
                    action(item)
                else:
                    action() # For "Back" option
        except (ValueError, IndexError):
            pass # Ignore invalid input
