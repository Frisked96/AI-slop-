import numpy as np
import random
import heapq
import os
import msvcrt # For Windows-specific non-blocking input
import time # For a small delay

class MapGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = np.full((height, width), '#', dtype=str)

    def add_room(self, x, y, room_width, room_height):
        if (x > 0 and y > 0 and
            x + room_width < self.width - 1 and
            y + room_height < self.height - 1):
            for ry in range(y, y + room_height):
                for rx in range(x, x + room_width):
                    self.map[ry, rx] = '.'
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

    def connect_rooms_mst(self, rooms):
        if not rooms: return

        # Create a graph where rooms are nodes and edges are distances between room centers
        edges = []
        for i in range(len(rooms)):
            for j in range(i + 1, len(rooms)):
                center1_x = rooms[i][0][0] + rooms[i][1][0] // 2
                center1_y = rooms[i][0][1] + rooms[i][1][1] // 2
                center2_x = rooms[j][0][0] + rooms[j][1][0] // 2
                center2_y = rooms[j][0][1] + rooms[j][1][1] // 2
                dist = self._distance((center1_x, center1_y), (center2_x, center2_y))
                edges.append((dist, i, j))

        # Sort edges by weight (distance)
        edges.sort()

        # Kruskal's algorithm for MST
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

        mst_edges = []
        for dist, i, j in edges:
            if union(i, j):
                mst_edges.append((rooms[i], rooms[j]))

        # Carve corridors along MST edges
        for room1, room2 in mst_edges:
            start_x = room1[0][0] + room1[1][0] // 2
            start_y = room1[0][1] + room1[1][1] // 2
            end_x = room2[0][0] + room2[1][0] // 2
            end_y = room2[0][1] + room2[1][1] // 2

            # Draw L-shaped corridor
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

    def print_map(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.map:
            print("".join(row))

    def generate_and_print(self):
        self.map = np.full((self.height, self.width), '#', dtype=str)
        rooms = self.generate_rooms(num_rooms=20, min_size=5, max_size=10)
        self.connect_rooms_mst(rooms)
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
        time.sleep(0.1)