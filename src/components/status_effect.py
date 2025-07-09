from abc import ABC, abstractmethod

class StatusEffect(ABC):
    def __init__(self, name, duration, description=""):
        self.name = name
        self.duration = duration
        self.description = description

    @abstractmethod
    def apply(self, target_state):
        pass

    def tick(self, target_state):
        if self.duration > 0:
            self.duration -= 1

    @abstractmethod
    def remove(self, target_state):
        pass

    def is_expired(self):
        return self.duration == 0

    def to_dict(self):
        return {
            "effect_type": self.__class__.__name__,
            "duration": self.duration,
            **self._to_dict_subclass()
        }

    def _to_dict_subclass(self):
        return {}

class Poison(StatusEffect):
    def __init__(self, duration=5, damage_per_turn=2):
        super().__init__("Poisoned", duration, f"Losing {damage_per_turn} HP per turn.")
        self.damage_per_turn = damage_per_turn

    def apply(self, target_state):
        pass

    def tick(self, target_state):
        super().tick(target_state)
        target_state.take_damage(self.damage_per_turn)

    def remove(self, target_state):
        pass

    def _to_dict_subclass(self):
        return {"damage_per_turn": self.damage_per_turn}

class SeveredLimb(StatusEffect):
    def __init__(self, limb_name, stat_penalties):
        super().__init__(f"Severed {limb_name}", -1, f"The {limb_name} is gone.")
        self.limb_name = limb_name
        self.stat_penalties = stat_penalties

    def apply(self, target_state):
        for stat, penalty in self.stat_penalties.items():
            if hasattr(target_state, stat):
                setattr(target_state, stat, getattr(target_state, stat) + penalty)
                if hasattr(target_state, f"max_{stat}"):
                    setattr(target_state, f"max_{stat}", getattr(target_state, f"max_{stat}") + penalty)

    def remove(self, target_state):
        for stat, penalty in self.stat_penalties.items():
            if hasattr(target_state, stat):
                setattr(target_state, stat, getattr(target_state, stat) - penalty)
                if hasattr(target_state, f"max_{stat}"):
                    setattr(target_state, f"max_{stat}", getattr(target_state, f"max_{stat}") - penalty)

    def _to_dict_subclass(self):
        return {"limb_name": self.limb_name, "stat_penalties": self.stat_penalties}

EFFECT_CLASS_MAP = {
    "Poison": Poison,
    "SeveredLimb": SeveredLimb,
}

def from_dict(data):
    effect_type = data.pop("effect_type")
    cls = EFFECT_CLASS_MAP.get(effect_type)
    if cls:
        return cls(**data)
    raise ValueError(f"Unknown status effect type: {effect_type}")
