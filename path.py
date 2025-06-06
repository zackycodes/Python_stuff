import tkinter as tk
import random
import numpy as np
import heapq

# Constants
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE
SNAKE_SPEED = 200  # ms between moves

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Pathfinding Maze")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.start = (0, 0)
        self.food = (GRID_SIZE - 1, GRID_SIZE - 1)
        self.snake = [self.start]
        self.path = []
        self.snake_trail = [self.start]

        self.generate_maze() # gen maze
        self.draw_maze() # draw it
        #self.find_path() # find path
        self.find_path_recursive_wrapper()
        self.move_snake() # move

        self.root.after(SNAKE_SPEED, self.move_snake)  # schedule

    def generate_maze(self):
        while True:
            # maze gen
            self.grid = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[0.7, 0.3])
            self.grid[0, 0] = 0  # start
            self.grid[GRID_SIZE - 1, GRID_SIZE - 1] = 0  # food

            if self.is_solvable():
                break

    def is_solvable(self):
        # check if there is a path from start to food
        open_list = [self.start]
        visited = set()
        while open_list:
            current = open_list.pop(0)
            if current == self.food:
                return True
            for next in self.neighbors(current):
                if next not in visited:
                    visited.add(next)
                    open_list.append(next)
        return False

    def draw_maze(self):
        self.canvas.delete("all")
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                color = "black" if self.grid[y, x] == 1 else "white"
                self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                             (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                             fill=color, outline="gray")
        start_x, start_y = self.start
        food_x, food_y = self.food
        self.canvas.create_rectangle(start_x * CELL_SIZE, start_y * CELL_SIZE,
                                     (start_x + 1) * CELL_SIZE, (start_y + 1) * CELL_SIZE,
                                     fill="green", outline="gray")
        self.canvas.create_rectangle(food_x * CELL_SIZE, food_y * CELL_SIZE,
                                     (food_x + 1) * CELL_SIZE, (food_y + 1) * CELL_SIZE,
                                     fill="red", outline="gray")

    def find_path(self):
        open_list = []
        heapq.heappush(open_list, (0, self.start))
        came_from = {}
        cost_so_far = {self.start: 0}
        came_from[self.start] = None

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == self.food:
                self.reconstruct_path(came_from)
                return

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, self.food)
                    heapq.heappush(open_list, (priority, next))
                    came_from[next] = current

    def find_path_recursive(self, pathyet,  level):
        print(f"\rDepth: {level}", end="")
        neighbors = [n for n in self.neighbors(pathyet[-1]) if (not n in pathyet) and self.grid[n[0]][n[1]] == 0]
        neighbors.sort(key=lambda move: self.heuristic(move, self.food))
        if pathyet[-1] == self.food:
            return level, [pathyet[-1]]
        if len(neighbors) == 0:
            return 0, None
        for i, n in enumerate(neighbors):
            val, move = self.find_path_recursive(pathyet + [n], level + 1)
            if 0 < val and move is not None:
                return val, [n] + move
        return 0, None

    def find_path_recursive_wrapper(self):
        self.pathstack = []
        self.path = self.find_path_recursive([self.start], 1)[1]
        print()
        print(self.path)
    def reconstruct_path(self, came_from):
        self.path = []
        current = self.food
        while current != self.start:
            self.path.append(current)
            current = came_from[current]
        self.path.reverse()

    def move_snake(self):
        if not self.path:
            return

        next_pos = self.path.pop(0)
        
        self.snake.append(next_pos)
        self.snake_trail.append(next_pos)
        
        # limit trail
        if len(self.snake_trail) > len(self.snake):
            self.snake_trail.pop(0)

        self.draw_maze()
        self.draw_snake()
        self.root.after(SNAKE_SPEED, self.move_snake)  # Schedule the next move

    def draw_snake(self):
        # draw the snake's trail
        for segment in self.snake_trail:
            y, x = segment
            self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                         (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                         fill="blue", outline="gray")

    def neighbors(self, pos):
        y, x = pos
        results = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and self.grid[ny, nx] == 0:
                results.append((ny, nx))
        return results

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
    input('------x End Program Here x-------')
