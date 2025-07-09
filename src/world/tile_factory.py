from .tiles import FloorTile, WallTile, NextMapTile, TrapTile, GrassTile, MudTile, RockTile, RubbleTile

def create_tile_from_dict(tile_data):
    tile_type_map = {
        "FloorTile": FloorTile,
        "WallTile": WallTile,
        "NextMapTile": NextMapTile,
        "TrapTile": TrapTile,
        "GrassTile": GrassTile,
        "MudTile": MudTile,
        "RockTile": RockTile,
        "RubbleTile": RubbleTile
    }
    tile_type_class = tile_type_map.get(tile_data["type"])
    if tile_type_class:
        if tile_data["type"] == "TrapTile":
            return tile_type_class.from_dict(tile_data)
        return tile_type_class()
    else:
        return FloorTile()
