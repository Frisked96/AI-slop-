import random
import numpy as np
import heapq
from ...world.tiles import FloorTile, NextMapTile, TrapTile, WallTile, GrassTile, MudTile, RockTile, RubbleTile, WaterTile
from . import Level

DEBUG_FORCE_X_TILE_NEAR_PLAYER = False

class DungeonLevel(Level):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.map_array = np.full((height, width), '#', dtype=str)
        self.room_coords = set()
        self.corridor_coords = set()

    def _is_valid(self, x, y):
        return 0 < x < self.width - 1 and 0 < y < self.height - 1

    def _distance(self, p1, p2):
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

    def _draw_corridor(self, start_point, end_point):
        path = self._a_star_path(start_point, end_point)
        if path:
            terrain_tile_chars = ['g', 'm', 'o', '%']
            for x, y in path:
                if self._is_valid(x, y):
                    self.map_array[y, x] = random.choice(terrain_tile_chars)
                    self.corridor_coords.add((x, y))

    def _a_star_path(self, start, end):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = { (x, y): float('inf') for x in range(self.width) for y in range(self.height) }
        g_score[start] = 0
        f_score = { (x, y): float('inf') for x in range(self.width) for y in range(self.height) }
        f_score[start] = self._distance(start, end)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if not self._is_valid(neighbor[0], neighbor[1]):
                    continue

                # Add a cost to avoid straight lines
                cost = 1 + random.uniform(0, 0.5)
                tentative_g_score = g_score[current] + cost

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self._distance(neighbor, end)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return None

    def _connect_rooms_mst(self, rooms):
        if not rooms: return
        room_centers = [((r[0][0] + r[1][0] // 2), (r[0][1] + r[1][1] // 2)) for r in rooms]
        edges = []
        for i in range(len(rooms)):
            for j in range(i + 1, len(rooms)):
                dist = self._distance(room_centers[i], room_centers[j])
                edges.append((dist, i, j))
        edges.sort()
        parent = list(range(len(rooms)))
        def find(i):
            if parent[i] == i: return i
            parent[i] = find(parent[i])
            return parent[i]
        def union(i, j):
            root_i, root_j = find(i), find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False
        for dist, i, j in edges:
            if union(i, j):
                self._draw_corridor(room_centers[i], room_centers[j])

    def _connect_rooms_k_nearest(self, rooms, k=3):
        if not rooms: return
        room_centers = [((r[0][0] + r[1][0] // 2), (r[0][1] + r[1][1] // 2)) for r in rooms]
        for i, center1 in enumerate(room_centers):
            distances = []
            for j, center2 in enumerate(room_centers):
                if i == j: continue
                distances.append((self._distance(center1, center2), j))
            distances.sort()
            for d, j in distances[:k]:
                self._draw_corridor(center1, room_centers[j])

    def _fill_room_area(self, x, y, room_width, room_height):
        terrain_tile_chars = ['g', 'm', 'o', '%']
        for ry in range(y, y + room_height):
            for rx in range(x, x + room_width):
                self.map_array[ry, rx] = random.choice(terrain_tile_chars)
                self.room_coords.add((rx, ry))

    def _add_internal_walls(self, x, y, room_width, room_height):
        if random.random() < 0.25:
            wall_length = random.choice([4, 5])
            if room_width > wall_length + 2 and room_height > wall_length + 2:
                start_rx = random.randint(x + 1, x + room_width - wall_length - 1)
                start_ry = random.randint(y + 1, y + room_height - wall_length - 1)
                if random.choice([True, False]):
                    for i in range(wall_length): self.map_array[start_ry, start_rx + i] = '#'
                else:
                    for i in range(wall_length): self.map_array[start_ry + i, start_rx] = '#'

    def _add_perimeter_irregularities(self, x, y, room_width, room_height):
        for rx in range(x + 1, x + room_width - 1):
            if random.random() < 0.1: self.map_array[y, rx] = '#'
            if random.random() < 0.1: self.map_array[y + room_height - 1, rx] = '#'
        for ry in range(y + 1, y + room_height - 1):
            if random.random() < 0.1: self.map_array[ry, x] = '#'
            if random.random() < 0.1: self.map_array[ry, x + room_width - 1] = '#'

    def add_room(self, x, y, room_width, room_height):
        if (x > 0 and y > 0 and x + room_width < self.width - 1 and y + room_height < self.height - 1):
            self._fill_room_area(x, y, room_width, room_height)
            self._add_internal_walls(x, y, room_width, room_height)
            self._add_perimeter_irregularities(x, y, room_width, room_height)
            return True
        return False

    def generate_rooms(self, num_rooms, min_size, max_size):
        rooms = []
        for _ in range(num_rooms):
            shape = random.choice(['rectangle', 'circle', 'ellipse', 'l_shape'])
            
            if shape == 'rectangle':
                room_width, room_height = random.randint(min_size, max_size), random.randint(min_size, max_size)
                x, y = random.randint(1, self.width - room_width - 1), random.randint(1, self.height - room_height - 1)
                if self.add_room(x, y, room_width, room_height):
                    rooms.append(((x, y), (room_width, room_height)))
            
            elif shape == 'circle':
                radius = random.randint(min_size // 2, max_size // 2)
                x, y = random.randint(1 + radius, self.width - radius - 1), random.randint(1 + radius, self.height - radius - 1)
                if self._add_circular_room(x, y, radius):
                    rooms.append(((x - radius, y - radius), (radius * 2, radius * 2)))

            elif shape == 'ellipse':
                rx, ry = random.randint(min_size // 2, max_size // 2), random.randint(min_size // 2, max_size // 2)
                x, y = random.randint(1 + rx, self.width - rx - 1), random.randint(1 + ry, self.height - ry - 1)
                if self._add_elliptical_room(x, y, rx, ry):
                    rooms.append(((x - rx, y - ry), (rx * 2, ry * 2)))

            elif shape == 'l_shape':
                w1, h1 = random.randint(min_size, max_size), random.randint(min_size, max_size)
                w2, h2 = random.randint(min_size, max_size), random.randint(min_size, max_size)
                x, y = random.randint(1, self.width - max(w1, w2) - 1), random.randint(1, self.height - h1 - h2 - 1)
                if self._add_l_shaped_room(x, y, w1, h1, w2, h2):
                    rooms.append(((x, y), (max(w1, w2), h1 + h2)))

        return rooms

    def _add_circular_room(self, cx, cy, radius):
        if not (self._is_valid(cx - radius, cy - radius) and self._is_valid(cx + radius, cy + radius)):
            return False
        
        terrain_tile_chars = ['g', 'm', 'o', '%']
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                if (x - cx)**2 + (y - cy)**2 <= radius**2:
                    if self._is_valid(x, y):
                        self.map_array[y, x] = random.choice(terrain_tile_chars)
                        self.room_coords.add((x, y))
        return True

    def _add_elliptical_room(self, cx, cy, rx, ry):
        if not (self._is_valid(cx - rx, cy - ry) and self._is_valid(cx + rx, cy + ry)):
            return False
            
        terrain_tile_chars = ['g', 'm', 'o', '%']
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                if ((x - cx) / rx)**2 + ((y - cy) / ry)**2 <= 1:
                    if self._is_valid(x, y):
                        self.map_array[y, x] = random.choice(terrain_tile_chars)
                        self.room_coords.add((x, y))
        return True

    def _add_l_shaped_room(self, x, y, w1, h1, w2, h2):
        if not (self._is_valid(x, y) and self._is_valid(x + max(w1, w2), y + h1 + h2)):
            return False

        terrain_tile_chars = ['g', 'm', 'o', '%']
        # Rectangle 1
        for ry in range(y, y + h1):
            for rx in range(x, x + w1):
                if self._is_valid(rx, ry):
                    self.map_array[ry, rx] = random.choice(terrain_tile_chars)
                    self.room_coords.add((rx, ry))
        
        # Rectangle 2
        for ry in range(y + h1, y + h1 + h2):
            for rx in range(x, x + w2):
                if self._is_valid(rx, ry):
                    self.map_array[ry, rx] = random.choice(terrain_tile_chars)
                    self.room_coords.add((rx, ry))
        return True

    def _apply_cellular_automata(self, iterations=6):
        terrain_chars = ['g', 'm', 'o', '%']
        for _ in range(iterations):
            new_map = np.copy(self.map_array)
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    if self.map_array[y, x] in terrain_chars:
                        neighbor_counts = {c: 0 for c in terrain_chars}
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                if dx == 0 and dy == 0: continue
                                if self.map_array[y + dy, x + dx] in terrain_chars:
                                    neighbor_counts[self.map_array[y + dy, x + dx]] += 1
                        most_common = max(neighbor_counts, key=neighbor_counts.get)
                        new_map[y, x] = most_common
            self.map_array = new_map

    def _generate_water(self, water_seed_prob=0.02, water_iterations=5):
        # Seed water
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.map_array[y, x] == '#' and random.random() < water_seed_prob:
                    self.map_array[y, x] = '~'

        # Grow water
        for _ in range(water_iterations):
            new_map = np.copy(self.map_array)
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    if self.map_array[y, x] == '#':
                        water_neighbors = 0
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                if self.map_array[y + dy, x + dx] == '~':
                                    water_neighbors += 1
                        if water_neighbors >= 5:
                            new_map[y, x] = '~'
            self.map_array = new_map

    def _generate_river(self, rooms):
        if len(rooms) < 2:
            return

        room_centers = [((r[0][0] + r[1][0] // 2), (r[0][1] + r[1][1] // 2)) for r in rooms]
        start_room_center, end_room_center = random.sample(room_centers, 2)

        path = self._a_star_path(start_room_center, end_room_center)
        if path:
            river_width = random.randint(3, 4)
            for x, y in path:
                for i in range(-river_width // 2, river_width // 2 + 1):
                    for j in range(-river_width // 2, river_width // 2 + 1):
                        if self._is_valid(x + i, y + j):
                            self.map_array[y + j, x + i] = '~'

    def generate_map(self, grid, room_centers, next_map_tile_pos, game_state=None):
        num_rooms, min_room_size, max_room_size = game_state.settings_manager.get_setting("num_rooms", 20), game_state.settings_manager.get_setting("min_room_size", 5), game_state.settings_manager.get_setting("max_room_size", 10)
        self.map_array = np.full((self.height, self.width), '#', dtype=str)
        rooms_data = self.generate_rooms(num_rooms, min_room_size, max_room_size)
        self._connect_rooms_mst(rooms_data)
        self._apply_cellular_automata(iterations=6)
        self._generate_water(water_seed_prob=0.02, water_iterations=5)
        self._generate_river(rooms_data)
        new_grid = [[self._char_to_tile(self.map_array[y, x]) for x in range(self.width)] for y in range(self.height)]
        grid[:] = new_grid
        room_centers[:] = [((r[0][0] + r[1][0] // 2), (r[0][1] + r[1][1] // 2)) for r in rooms_data]
        player_spawn_pos = random.choice(room_centers) if room_centers else None
        next_map_tile_pos = self._place_next_map_tile_furthest(new_grid, player_spawn_pos, room_centers)
        if game_state and game_state.dungeon_level >= 1:
            self._place_traps(new_grid, game_state, player_spawn_pos, next_map_tile_pos)
        if game_state and game_state.player and player_spawn_pos:
            game_state.player.x, game_state.player.y = player_spawn_pos
        return new_grid, room_centers, next_map_tile_pos, player_spawn_pos, self.room_coords, self.corridor_coords

    def _char_to_tile(self, char):
        from ...world.tiles import WaterTile
        return {'#': WallTile(), 'g': GrassTile(), 'm': MudTile(), 'o': RockTile(), '%': RubbleTile(), '~': WaterTile()}.get(char, WallTile())

    def _place_next_map_tile_furthest(self, grid, player_spawn_pos, room_centers):
        if not player_spawn_pos or not room_centers:
            return None

        # Find the room center furthest from the player's spawn point
        max_dist = -1
        furthest_room_center = None
        for center in room_centers:
            dist = self._distance(center, player_spawn_pos)
            if dist > max_dist:
                max_dist = dist
                furthest_room_center = center

        if furthest_room_center:
            x, y = furthest_room_center
            grid[y][x] = NextMapTile()
            return furthest_room_center
        return None

    def _place_traps(self, grid, game_state, player_spawn_pos, next_map_tile_pos):
        max_traps = 10
        possible_spawns = []
        for y in range(self.height):
            for x in range(self.width):
                if isinstance(grid[y][x], (GrassTile, MudTile, RockTile, RubbleTile)) and (x, y) != player_spawn_pos and (x, y) != next_map_tile_pos:
                    possible_spawns.append((x, y))
        random.shuffle(possible_spawns)
        for _ in range(min(max_traps, len(possible_spawns))):
            x, y = possible_spawns.pop()
            trap_char = '.'
