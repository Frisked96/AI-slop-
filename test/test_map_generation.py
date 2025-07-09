import numpy as np
import random
import msvcrt # For Windows-specific non-blocking input
import time # For a small delay
import os # For clearing the console
import heapq # For MST algorithm

class MapGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = np.full((height, width), '#', dtype=str) # Initialize with walls

    def create_border(self):
        # Border is already created by initializing with walls
        pass

    def add_room(self, x, y, room_width, room_height):
        # Ensure room is within bounds and not overlapping with border
        if (x > 0 and y > 0 and
            x + room_width < self.width - 1 and
            y + room_height < self.height - 1):
            # Fill the room with floor tiles
            for ry in range(y, y + room_height):
                for rx in range(x, x + room_width):
                    self.map[ry, rx] = '.'

            # Add internal walls with a 25% chance
            if random.random() < 0.25:
                wall_length = random.choice([4, 5])
                # Ensure wall can fit within the room with some padding
                if room_width > wall_length + 2 and room_height > wall_length + 2:
                    # Randomly choose starting point within the room (excluding perimeter)
                    start_rx = random.randint(x + 1, x + room_width - wall_length - 1)
                    start_ry = random.randint(y + 1, y + room_height - wall_length - 1)

                    # Randomly choose orientation (horizontal or vertical)
                    if random.choice([True, False]): # Horizontal wall
                        for i in range(wall_length):
                            self.map[start_ry, start_rx + i] = '#'
                    else: # Vertical wall
                        for i in range(wall_length):
                            self.map[start_ry + i, start_rx] = '#'

            # Introduce some irregularity to the edges
            # Iterate over the perimeter and randomly change some back to walls
            # Top and bottom edges (excluding corners)
            for rx in range(x + 1, x + room_width - 1):
                if random.random() < 0.1: # 10% chance to make it a wall
                    self.map[y, rx] = '#'
                if random.random() < 0.1:
                    self.map[y + room_height - 1, rx] = '#'
            # Left and right edges (excluding corners)
            for ry in range(y + 1, y + room_height - 1):
                if random.random() < 0.1:
                    self.map[ry, x] = '#'
                if random.random() < 0.1:
                    self.map[ry, x + room_width - 1] = '#'
            return True
        return False

    def generate_rooms(self, num_rooms, min_size, max_size):
        rooms = []
        for _ in range(num_rooms):
            room_width = random.randint(min_size, max_size)
            room_height = random.randint(min_size, max_size)
            x = random.randint(1, self.width - room_width - 1)
            y = random.randint(1, self.height - room_height - 1)
            if self.add_room(x, y, room_width, room_height):
                rooms.append(((x, y), (room_width, room_height)))
        return rooms

    def _is_valid(self, x, y):
        return 0 < x < self.width - 1 and 0 < y < self.height - 1

    def _distance(self, p1, p2):
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

    def _draw_corridor(self, start_point, end_point):
        start_x, start_y = start_point
        end_x, end_y = end_point

        if random.choice([True, False]):
            for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                if self._is_valid(x, start_y):
                    self.map[start_y, x] = '.'
            for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                if self._is_valid(end_x, y):
                    self.map[y, end_x] = '.'
        else:
            for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                if self._is_valid(start_x, y):
                    self.map[y, start_x] = '.'
            for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                if self._is_valid(x, end_y):
                    self.map[end_y, x] = '.'

    def _connect_rooms_mst(self, rooms):
        if not rooms: return

        room_centers = []
        for r in rooms:
            room_centers.append((r[0][0] + r[1][0] // 2, r[0][1] + r[1][1] // 2))

        edges = []
        for i in range(len(rooms)):
            for j in range(i + 1, len(rooms)):
                dist = self._distance(room_centers[i], room_centers[j])
                edges.append((dist, i, j))

        edges.sort()

        parent = list(range(len(rooms)))
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False

        for dist, i, j in edges:
            if union(i, j):
                self._draw_corridor(room_centers[i], room_centers[j])

    def _connect_rooms_k_nearest(self, rooms, k=3):
        if not rooms: return

        room_centers = []
        for r in rooms:
            room_centers.append((r[0][0] + r[1][0] // 2, r[0][1] + r[1][1] // 2))

        for i, center1 in enumerate(room_centers):
            distances = []
            for j, center2 in enumerate(room_centers):
                if i == j: continue
                distances.append((self._distance(center1, center2), j))
            
            distances.sort()
            
            for d, j in distances[:k]:
                self._draw_corridor(center1, room_centers[j])

    def print_map(self):
        os.system('cls' if os.name == 'nt' else 'clear') # Clear console
        for row in self.map:
            print("".join(row))

    def generate_and_print(self):
        self.map = np.full((self.height, self.width), '#', dtype=str) # Reset map
        self.create_border()
        rooms = self.generate_rooms(num_rooms=20, min_size=5, max_size=10)
        self._connect_rooms_mst(rooms) # Ensure all rooms are connected
        self._connect_rooms_k_nearest(rooms) # Add additional connections
        self.print_map()

if __name__ == "__main__":
    generator = MapGenerator(width=100, height=30)
    
    print("Press 'w' to generate a new map, 'q' to quit.")
    generator.generate_and_print()

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key == 'w':
                print("\nGenerating new map...")
                generator.generate_and_print()
            elif key == 'q':
                print("Exiting.")
                break
        time.sleep(0.1) # Small delay to prevent busy-waiting