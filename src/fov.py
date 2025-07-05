
def compute_fov(game_map, player_x, player_y, radius):
    """
    Computes the Field of View for a given map, player position, and radius.
    Uses a basic raycasting algorithm.
    """
    visible_tiles = set()
    visible_tiles.add((player_x, player_y))

    for x in range(player_x - radius, player_x + radius + 1):
        for y in range(player_y - radius, player_y + radius + 1):
            if (x - player_x)**2 + (y - player_y)**2 <= radius**2:
                if _is_in_line_of_sight(game_map, player_x, player_y, x, y):
                    visible_tiles.add((x, y))
    return visible_tiles

def _is_in_line_of_sight(game_map, start_x, start_y, end_x, end_y):
    """
    Checks if there is an unobstructed line of sight between two points.
    Uses Bresenham's Line Algorithm.
    """
    x1, y1 = start_x, start_y
    x2, y2 = end_x, end_y
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        if x1 == x2 and y1 == y2:
            return True

        # Check if the current tile blocks sight, but don't block the start or end tiles themselves
        if (x1 != start_x or y1 != start_y) and (x1 != end_x or y1 != end_y):
            if 0 <= x1 < game_map.width and 0 <= y1 < game_map.height:
                if not game_map.grid[y1][x1].is_transparent:
                    return False

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
