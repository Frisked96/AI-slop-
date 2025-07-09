from .entity import Entity
from .player_state import PlayerState
from .player_class import BASELINE_STATS, get_class_by_name
from ..items.item import Item

class Player(Entity):
    def __init__(self, x, y, player_class_name=None):
        super().__init__(x, y, health=0, attack=0, defense=0) # Dummy values

        self.player_class_name = player_class_name
        self.player_class = get_class_by_name(player_class_name)

        # Start with baseline stats and apply class modifiers
        final_stats = BASELINE_STATS.copy()
        if self.player_class:
            modifiers = self.player_class.get_stat_modifiers()
            for stat, value in modifiers.items():
                final_stats[stat] = final_stats.get(stat, 0) + value
        
        self.state = PlayerState(
            health=final_stats["health"],
            attack=final_stats["attack"],
            defense=final_stats["defense"],
            mana=final_stats["mana"],
            stamina=final_stats["stamina"]
        )
        
        self.inventory = []
        self.moved = True
        self.last_direction = None

    def take_damage(self, amount):
        self.state.take_damage(amount)

    def is_alive(self):
        return self.state.is_alive()

    def _can_move_to(self, x, y, game_map):
        return not game_map.is_wall(x, y)

    def move(self, dx, dy, game_map):
        initial_x, initial_y = self.x, self.y
        target_x = self.x + dx
        target_y = self.y + dy

        if self._can_move_to(target_x, target_y, game_map):
            self.x = target_x
            self.y = target_y
        
        if self.x != initial_x or self.y != initial_y:
            self.moved = True

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "player_class_name": self.player_class_name,
            "state": self.state.to_dict(),
            "inventory": [item.to_dict() for item in self.inventory]
        }

    @classmethod
    def from_dict(cls, data):
        from ..items.item_factory import create_item_from_dict

        new_player = cls(data["x"], data["y"], data.get("player_class_name"))
        new_player.state = PlayerState.from_dict(data["state"])
        new_player.inventory = [create_item_from_dict(item_data) for item_data in data.get("inventory", [])]
        return new_player

    def add_to_inventory(self, item):
        self.inventory.append(item)
        self.state.weight_carried += item.weight

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.state.weight_carried -= item.weight
            return True
        return False

    def get_inventory_weight(self):
        return sum(item.weight for item in self.inventory)
        
    def update_wellbeing(self):
        self.state.update_wellbeing()
        
    def get_status_effects(self):
        return self.state.get_status_effects()
