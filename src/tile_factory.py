from .tiles import FloorTile, WallTile, NextMapTile, NorthExitTile, EastExitTile, SouthExitTile, WestExitTile, CityCenterEntranceTile, BlacksmithShopTile, DoorTile, TrapTile

def create_tile_from_dict(tile_data):
    tile_type_map = {
        "FloorTile": FloorTile,
        "WallTile": WallTile,
        "NextMapTile": NextMapTile,
        "NorthExitTile": NorthExitTile,
        "EastExitTile": EastExitTile,
        "SouthExitTile": SouthExitTile,
        "WestExitTile": WestExitTile,
        "CityCenterEntranceTile": CityCenterEntranceTile,
        "BlacksmithShopTile": BlacksmithShopTile,
        "DoorTile": DoorTile,
        "TrapTile": TrapTile  # Add TrapTile here
    }
    tile_type_class = tile_type_map.get(tile_data["type"])
    if tile_type_class:
        # For tiles that require specific arguments from tile_data beyond their type
        if tile_data["type"] == "BlacksmithShopTile":
            return tile_type_class(char=tile_data["character"])
        elif tile_data["type"] == "TrapTile":
            # TrapTile.from_dict will handle its specific attributes
            return tile_type_class.from_dict(tile_data)
        # For simple tiles that are just instantiated
        return tile_type_class()
    else:
        # Fallback for unknown tile types, or raise an error
        return FloorTile() # Default to floor
