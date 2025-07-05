from .entity import Entity
from .item import Item # Import necessary item classes

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, attack=10, defense=5) # Initial player stats
        self.inventory = [] # Initialize player inventory
        self.moved = True

    def _can_move_to(self, x, y, game_map):
        return not game_map.is_wall(x, y)

    def _attempt_move(self, dx, dy, game_map, num_steps):
        target_x = self.x + dx * num_steps
        target_y = self.y + dy * num_steps

        for s in range(1, num_steps + 1):
            check_x = self.x + dx * s
            check_y = self.y + dy * s
            if not self._can_move_to(check_x, check_y, game_map):
                return False
        
        self.x, self.y = target_x, target_y
        return True

    def _handle_horizontal_move(self, dx, game_map):
        if game_map.current_map_type == "dungeon":
            max_steps = 2
        elif game_map.current_map_type in ["city_center", "outer_city"]:
            max_steps = 4
        else:
            max_steps = 1

        # Check for interaction at the immediate next tile (1 step)
        next_tile_x = self.x + dx
        next_tile_y = self.y
        if game_map.next_map_tile_pos and next_tile_x == game_map.next_map_tile_pos[0] and next_tile_y == game_map.next_map_tile_pos[1]:
            if self._can_move_to(next_tile_x, next_tile_y, game_map):
                self.x, self.y = next_tile_x, next_tile_y
            return # Player stops for interaction

        # Now, handle multi-step movement
        for num_steps in range(max_steps, 0, -1):
            if self._attempt_move(dx, 0, game_map, num_steps):
                return

    def _handle_vertical_move(self, dy, game_map):
        max_steps = 1
        for num_steps in range(max_steps, 0, -1):
            if self._attempt_move(0, dy, game_map, num_steps):
                return

    def move(self, dx, dy, game_map):
        initial_x, initial_y = self.x, self.y
        if dx != 0 and dy == 0: # Horizontal movement
            self._handle_horizontal_move(dx, game_map)
        elif dy != 0 and dx == 0: # Vertical movement
            self._handle_vertical_move(dy, game_map)
        if self.x != initial_x or self.y != initial_y:
            self.moved = True

    def to_dict(self):
        data = super().to_dict()
        data["inventory"] = [item.to_dict() for item in self.inventory]
        return data

    @classmethod
    def from_dict(cls, data):
        from .item_factory import create_item_from_dict # Local import to avoid circular dependency

        player = super().from_dict(data)
        new_player = cls(player.x, player.y) # Initialize with x, y
        new_player.max_health = player.max_health
        new_player.health = player.health
        new_player.attack = player.attack
        new_player.defense = player.defense
        new_player.inventory = [create_item_from_dict(item_data) for item_data in data.get("inventory", [])]
        return new_player
