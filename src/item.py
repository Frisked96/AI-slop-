class Item:
    def __init__(self, item_id, name, description, value, item_type, stackable=False, max_stack_size=1, current_stack_size=1, weight=0.1):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.value = value  # Renamed from price
        self.item_type = item_type
        self.stackable = stackable
        self.max_stack_size = max_stack_size
        self.current_stack_size = current_stack_size # Replaces count
        self.weight = weight

    def __str__(self):
        if self.stackable and self.current_stack_size > 1:
            return f"{self.name} (x{self.current_stack_size}) - {self.description} ({self.value} Gold, {self.weight*self.current_stack_size:.1f} lbs)"
        return f"{self.name} - {self.description} ({self.value} Gold, {self.weight:.1f} lbs)"

    def use(self, target): # Placeholder method for item usage
        # This method should be overridden by subclasses (e.g., Potion, Weapon)
        raise NotImplementedError("This item does not have a 'use' action defined.")

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "description": self.description,
            "value": self.value,
            "item_type": self.item_type,
            "stackable": self.stackable,
            "max_stack_size": self.max_stack_size,
            "current_stack_size": self.current_stack_size,
            "weight": self.weight
        }

    @classmethod
    def from_dict(cls, data):
        # This method will be called by item_factory to create specific item instances
        # It should only reconstruct the base Item properties. Subclasses will add their own.
        return cls(
            item_id=data["item_id"],
            name=data["name"],
            description=data["description"],
            value=data["value"],
            item_type=data["item_type"],
            stackable=data.get("stackable", False),
            max_stack_size=data.get("max_stack_size", 1),
            current_stack_size=data.get("current_stack_size", 1),
            weight=data.get("weight", 0.1)
        )

class Weapon(Item):
    def __init__(self, item_id, name, description, value, weapon_type, damage, weight=1.0):
        super().__init__(item_id, name, description, value, "weapon", stackable=False, weight=weight)
        self.weapon_type = weapon_type
        self.damage = damage

    def use(self, target): # In a real game, 'use' might equip the weapon
        # For now, we'll just print a message. Equipping logic would go elsewhere.
        return f"You equip the {self.name}. It deals {self.damage} damage."

    def to_dict(self):
        data = super().to_dict()
        data["weapon_type"] = self.weapon_type
        data["damage"] = self.damage
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            item_id=data["item_id"],
            name=data["name"],
            description=data["description"],
            value=data["value"],
            weapon_type=data["weapon_type"],
            damage=data["damage"],
            weight=data.get("weight", 1.0)
        )

class Sword(Weapon):
    def __init__(self, item_id, name, description, value, damage, weight=1.0):
        super().__init__(item_id, name, description, value, "sword", damage, weight)