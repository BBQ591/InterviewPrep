import random
import copy


class Match3:
    def __init__(self, colors: list[str], width: int, height: int):
        self.width = width
        self.height = height
        self.colors = colors
        self.grid = [[self.generate_el() for j in range(height)] for i in range(width)]
        self.score = 0

    def generate_el(self):
        return self.colors[random.randint(0, len(self.colors) - 1)]

    def switch_pos(self, grid, pos1, pos2):
        tmp_grid = copy.deepcopy(grid)
        x1, y1 = pos1
        x2, y2 = pos2
        tmp = tmp_grid[x1][y1]
        tmp_grid[x1][y1] = tmp_grid[x2][y2]
        tmp_grid[x2][y2] = tmp
        return tmp_grid

    def _check_move(self, grid) -> bool:
        for row in grid:
            count = 1
            grouped = []
            for i in range(1, len(row)):
                if row[i] == row[i - 1]:
                    count += 1
                else:
                    grouped.append(count)
                    count = 1

            grouped.append(count)
            for el in grouped:
                if el >= 3:
                    return True
        return False

    def transpose(self, arr):
        tmp_grid = [[0 for i in range(len(arr))] for j in range(len(arr[0]))]
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                tmp_grid[j][i] = arr[i][j]
        return tmp_grid

    def valid_move(self, tmp_grid) -> bool:
        if self._check_move(tmp_grid):
            return True
        transposed = self.transpose(tmp_grid)
        if self._check_move(transposed):
            return True

        return False

    def to_remove(self, grid):
        to_remove = set()
        for i, row in enumerate(grid):
            counter = 1
            zipped = []
            for j in range(1, len(row)):
                if row[j] == row[j - 1]:
                    counter += 1
                else:
                    zipped.append(counter)
                    counter = 1
            zipped.append(counter)
            new_row = []
            for j in range(len(zipped)):
                new_row.extend([zipped[j] for z in range(zipped[0])])

            for j in range(len(new_row)):
                if new_row[j] >= 3:
                    to_remove.add((i, j))
        return to_remove

    def revert_elements(self, sets):
        new_set = set()
        for el in sets:
            new_set.add((el[1], el[0]))
        return new_set

    def filter_fill_row(self, row, to_filter):
        new_row = []
        for i in range(len(row)):
            if i not in to_filter:
                new_row.append(row[i])
        to_add = len(row) - len(new_row)
        out_row = []
        for i in range(to_add):
            out_row.append(self.generate_el())
        out_row.extend(new_row)
        return out_row

    def filter_elements(self, grid, to_remove):
        transposed = self.transpose(grid)
        reverted_removes = self.revert_elements(to_remove)
        new_grid = []
        for i, row in enumerate(transposed):
            to_filter = [el[1] for el in reverted_removes if el[0] == i]
            new_row = self.filter_fill_row(row, to_filter)
            new_grid.append(new_row)
        final = self.transpose(new_grid)
        return final

    def get_col_remove(self, grid):
        transposed = self.transpose(grid)
        to_remove_col = self.to_remove(transposed)
        reverted_remove = self.revert_elements(to_remove_col)
        return reverted_remove

    def reduce_moves(self, tmp_grid):
        to_remove = self.to_remove(tmp_grid)
        to_remove_col = self.get_col_remove(tmp_grid)
        filtered_filled = self.filter_elements(tmp_grid, to_remove | to_remove_col)
        return filtered_filled

    def swap(self, pos1: tuple[int, int], pos2: tuple[int, int]):
        tmp_grid = copy.deepcopy(self.grid)
        tmp_grid = self.switch_pos(tmp_grid, pos1, pos2)
        while self.valid_move(tmp_grid):
            tmp_grid = self.reduce_moves(tmp_grid)
            self.grid = tmp_grid
