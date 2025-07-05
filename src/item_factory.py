from .item import Item, Weapon, Sword

def create_item_from_dict(item_data):
    item_type = item_data.get("item_type")
    if item_type == "weapon":
        weapon_type = item_data.get("weapon_type")
        if weapon_type == "sword":
            return Sword.from_dict(item_data)
    # Add more item types here as they are created
    return Item.from_dict(item_data) # Fallback to base Item if type is unknown