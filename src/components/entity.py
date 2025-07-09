class Entity:
    def __init__(self, x, y, health, attack, defense):
        self.x = x
        self.y = y
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "max_health": self.max_health,
            "health": self.health,
            "attack": self.attack,
            "defense": self.defense
        }

    @classmethod
    def from_dict(cls, data):
        # Note: When loading, we pass max_health as health to the constructor
        # as the constructor expects initial health. The actual current health
        # is then set from data['health'].
        entity = cls(data["x"], data["y"], data["max_health"], data["attack"], data["defense"])
        entity.health = data["health"]
        return entity
