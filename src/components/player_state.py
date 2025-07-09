from .status_effect import StatusEffect, from_dict as effect_from_dict

class PlayerState:
    def __init__(self, health, attack, defense, mana, stamina, level=1, hunger=100, thirst=100, comfort=100, heartrate=70, weight_carried=0.0):
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.max_mana = mana
        self.mana = mana
        self.max_stamina = stamina
        self.stamina = stamina
        
        self.level = level
        self.hunger = hunger
        self.thirst = thirst
        self.comfort = comfort
        self.heartrate = heartrate
        self.weight_carried = weight_carried
        
        self.active_effects = []

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def to_dict(self):
        return {
            "max_health": self.max_health,
            "health": self.health,
            "attack": self.attack,
            "defense": self.defense,
            "max_mana": self.max_mana,
            "mana": self.mana,
            "max_stamina": self.max_stamina,
            "stamina": self.stamina,
            "level": self.level,
            "hunger": self.hunger,
            "thirst": self.thirst,
            "comfort": self.comfort,
            "heartrate": self.heartrate,
            "weight_carried": self.weight_carried,
            "active_effects": [effect.to_dict() for effect in self.active_effects]
        }

    @classmethod
    def from_dict(cls, data):
        state = cls(
            health=data.get("max_health", 100),
            attack=data.get("attack", 10),
            defense=data.get("defense", 5),
            mana=data.get("max_mana", 0),
            stamina=data.get("max_stamina", 100),
            level=data.get("level", 1),
            hunger=data.get("hunger", 100),
            thirst=data.get("thirst", 100),
            comfort=data.get("comfort", 100),
            heartrate=data.get("heartrate", 70),
            weight_carried=data.get("weight_carried", 0.0)
        )
        state.health = data.get("health", state.max_health)
        state.mana = data.get("mana", state.max_mana)
        state.stamina = data.get("stamina", state.max_stamina)
        state.active_effects = [effect_from_dict(effect_data) for effect_data in data.get("active_effects", [])]
        return state

    def add_effect(self, effect: StatusEffect):
        self.active_effects.append(effect)
        effect.apply(self)

    def remove_effect(self, effect: StatusEffect):
        if effect in self.active_effects:
            effect.remove(self)
            self.active_effects.remove(effect)

    def update_effects(self):
        expired_effects = [e for e in self.active_effects if e.is_expired()]
        for effect in expired_effects:
            self.remove_effect(effect)
        
        for effect in self.active_effects:
            effect.tick(self)

    def update_wellbeing(self):
        self.hunger = max(0, self.hunger - 0.1)
        self.thirst = max(0, self.thirst - 0.2)

    def get_status_effects(self):
        effects = [effect.name for effect in self.active_effects]
        if self.hunger < 20:
            effects.append("Starving")
        if self.thirst < 20:
            effects.append("Dehydrated")
        if self.health < 30:
            effects.append("Injured")
        return list(set(effects))
