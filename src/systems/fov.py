def compute_fov(game_map, player_x, player_y, radius, last_direction='s'):
    visible_tiles = set()
    visible_tiles.add((player_x, player_y))

    if last_direction in ['w', 's']:  # Vertical movement (circular FOV, appears as a tall ellipse)
        x_radius = radius
        y_radius = radius
    else:  # Horizontal movement (elliptical FOV, appears as a wide ellipse)
        # Account for character aspect ratio (approx. 1:2 width:height)
        x_radius = int(radius * 2)  # Make it wider
        y_radius = int(radius * 0.75) # Make it shorter to compensate

    for x in range(player_x - x_radius, player_x + x_radius + 1):
        for y in range(player_y - y_radius, player_y + y_radius + 1):
            # Use ellipse equation for all cases.
            if x_radius > 0 and y_radius > 0:
                if ((x - player_x) / x_radius)**2 + ((y - player_y) / y_radius)**2 <= 1:
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
