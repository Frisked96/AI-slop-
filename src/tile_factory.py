from .tiles import FloorTile, WallTile, NextMapTile, NorthExitTile, EastExitTile, SouthExitTile, WestExitTile, CityCenterEntranceTile, BlacksmithShopTile, DoorTile

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
        "DoorTile": DoorTile
    }
    tile_type = tile_type_map.get(tile_data["type"])
    if tile_type:
        if tile_data["type"] == "BlacksmithShopTile":
            return tile_type(char=tile_data["character"])
        return tile_type()
    else:
        # Fallback for unknown tile types, or raise an error
        return FloorTile() # Default to floor
