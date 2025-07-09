from abc import ABC, abstractmethod

# Baseline stats for an "Ordinary Man"
BASELINE_STATS = {
    "health": 100,
    "attack": 10,
    "defense": 5,
    "mana": 10, # Base mana for all, allowing for basic skills/scrolls
    "stamina": 100 # Base stamina for all
}

class PlayerClass(ABC):
    """Abstract base class for all player classes."""
    @property
    @abstractmethod
    def name(self):
        """The name of the class."""
        pass

    @abstractmethod
    def get_stat_modifiers(self):
        """Returns a dictionary of stat modifiers for this class."""
        pass

    def to_dict(self):
        return {'class_name': self.name}

# --- Concrete Class Implementations ---

class Swordsman(PlayerClass):
    """A class focused on melee combat. Higher health, attack, and defense."""
    @property
    def name(self):
        return "Swordsman"

    def get_stat_modifiers(self):
        return {
            "health": 20,  # +20
            "attack": 5,   # +5
            "defense": 5,  # +5
            "stamina": 20 # +20
        }

class Mage(PlayerClass):
    """A class focused on arcane arts. Lower health, but has mana."""
    @property
    def name(self):
        return "Mage"

    def get_stat_modifiers(self):
        return {
            "health": -20, # -20
            "attack": -2,  # -2
            "defense": -2, # -2
            "mana": 50     # +50
        }

class Thief(PlayerClass):
    """A nimble class. Higher stamina, slightly better attack."""
    @property
    def name(self):
        return "Thief"

    def get_stat_modifiers(self):
        return {
            "health": -10,
            "attack": 2,
            "stamina": 30
        }

class Gambler(PlayerClass):
    """A class of chance. Stats can be unpredictable. (Future implementation)"""
    @property
    def name(self):
        return "Gambler"

    def get_stat_modifiers(self):
        # For now, a balanced but slightly fragile build
        return {
            "health": -15,
            "attack": 3,
            "defense": -2,
            "stamina": 10
        }

# --- Factory Function ---

# A mapping of class names to their class objects for the factory
CLASS_REGISTRY = {
    "Swordsman": Swordsman,
    "Mage": Mage,
    "Thief": Thief,
    "Gambler": Gambler
}

def get_class_by_name(class_name):
    """Returns an instance of a player class from its name."""
    if class_name is None or class_name == "Ordinary Man":
        return None # Represents the classless "Ordinary Man"
    
    cls = CLASS_REGISTRY.get(class_name)
    if cls:
        return cls()
    else:
        raise ValueError(f"Unknown player class: {class_name}")
