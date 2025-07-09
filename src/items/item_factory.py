from .item import Item, Weapon, Sword

def create_item_from_dict(item_data):
    item_type = item_data.get("item_type")
    if item_type == "weapon":
        weapon_type = item_data.get("weapon_type")
        if weapon_type == "sword":
            return Sword.from_dict(item_data)
    return Item.from_dict(item_data)

def load_items_from_json(filepath):
    import json
    with open(filepath, 'r') as f:
        all_item_data = json.load(f)
    
    item_objects = {}
    for item_id, item_data in all_item_data.items():
        item_data['item_id'] = item_id
        item_objects[item_id] = create_item_from_dict(item_data)
        
    return item_objects
