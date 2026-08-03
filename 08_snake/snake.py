import random
from enum import Enum


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class Snake:
    def __init__(self, height, width):
        self.direction = Direction.EAST
        self.cells = [(0, 0)]
        self.height = height
        self.width = width

    def get_cells(self):
        return self.cells

    def move(self, prev_eaten: bool) -> bool:
        delta = {
            Direction.EAST: (0, 1),
            Direction.WEST: (0, -1),
            Direction.SOUTH: (1, 0),
            Direction.NORTH: (-1, 0),
        }
        curr_delta = delta[self.direction]
        curr_head = self.head()
        next_head = (curr_head[0] + curr_delta[0], curr_head[1] + curr_delta[1])
        if (
            next_head in self.cells
            or next_head[0] < 0
            or next_head[1] < 0
            or next_head[0] >= self.height
            or next_head[1] >= self.width
        ):
            raise NotImplementedError("Game Ended")

        self.cells.append(next_head)
        if not prev_eaten:
            self.cells = self.cells[1:]

    def head(self):
        return self.cells[-1]

    def change_direction(self, direction):
        opposite = {
            Direction.SOUTH: Direction.NORTH,
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        if self.direction == direction or opposite[self.direction] == direction:
            return
        self.direction = direction


class Food:
    def __init__(self):
        self.row = None
        self.col = None


class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
        self.snake = Snake(height, width)
        self.food = Food()
        self.prev_eaten = False

    def place_food(self):
        snake_position = self.snake.get_cells()
        random_row = random.randint(0, self.height - 1)
        random_col = random.randint(0, self.width - 1)
        while (random_row, random_col) in snake_position:
            random_row = random.randint(0, self.height - 1)
            random_col = random.randint(0, self.width - 1)

        self.food = Food()
        self.food.row = random_row
        self.food.col = random_col
        return self.food

    def move_snake(self):
        self.snake.move(self.prev_eaten)
        if new_snake.head() == (self.food.row, self.food.col):
            self.place_food()
            self.prev_eaten = True
        else:
            self.prev_eaten = False

    def change_direction(self, direction: Direction):
        self.snake.change_direction(direction)
