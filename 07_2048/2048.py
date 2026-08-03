from enum import Enum
import copy


class directions(Enum):
    RIGHT = "right"
    LEFT = "left"
    DOWN = "down"
    UP = "up"


class game_2048:
    def __init__(self):
        self.grid = [[0 for i in range(4)] for j in range(4)]

    def reverse_grid(self, new_grid):
        pass

    def reverse_columns(self, new_grid):
        pass

    def operate_row(self, row):
        non_zero_row = []
        for i in range(len(row)):
            if row[i] != 0:
                non_zero_row.append(row[i])

        out_row = []
        index = 0
        while index + 1 < len(non_zero_row):
            if non_zero_row[index] == non_zero_row[index + 1]:
                out_row.append(non_zero_row[index] * 2)
                index += 2
            else:
                out_row.append(non_zero_row[index])
                index += 1
        if index < len(non_zero_row):
            out_row.append(non_zero_row[index])
        for i in range(len(row) - len(out_row)):
            out_row.append(0)
        return out_row

    def operate_col(self, grid, col):
        out_col = []
        for i in range(len(grid)):
            out_col.append(grid[i][col])

        return out_col

    def apply_left(self, new_grid):
        out_grid = []
        for row in new_grid:
            pass

    def apply_up(self, new_grid):
        out_grid = [[0 for j in range(len(new_grid[0]))] for i in range(new_grid)]
        for col in range(len(new_grid[0])):
            curr_col = self.operate_col(new_grid, col)
            out_col = self.operate_row(curr_col)
            for i in range(len(new_grid)):
                out_grid[i][col] = out_col[i]

        return out_grid

    def move(self, direction):
        if direction == directions.RIGHT:
            new_grid = self.reverse_grid(self.grid)
            next_grid = self.apply_left(new_grid)
            final_grid = self.reverse_grid(next_grid)
        if direction == directions.DOWN:
            new_grid = self.reverse_columns(self.grid)
            next_grid = self.apply_up(new_grid)
            final_grid = self.reverse_columns(next_grid)
        if direction == directions.LEFT:
            final_grid = self.apply_left(self.grid)
        if direction == directions.UP:
            final_grid = self.apply_up(self.grid)
