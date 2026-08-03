from typing import List
import random


class Minesweeper:
    def __init__(self, width, height, mines: int):
        self.width = width
        self.height = height
        self.mines = self.generate_mines(mines)
        self.flags = set()
        self.grid = [[-1 for i in range(width)] for j in range(height)]
        self.revealed = set()

    def generate_mines(self, num_mines) -> set[tuple[int, int]]:
        mines = set()
        while num_mines > 0:
            pos = (
                random.randint(0, self.height - 1),
                random.randint(0, self.width - 1),
            )
            if pos in mines:
                continue
            num_mines -= 1
            mines.add(pos)
        return mines

    def click_flag(self, position: tuple[int, int]):
        if position in self.flags:
            self.flags.remove(position)
        else:
            self.flags.add(position)

    def check_position(self, row, col) -> bool:
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return False
        return True

    def get_neighbors(self, position):
        deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        out = []
        for delta in deltas:
            del_row, del_col = delta
            if self.check_position(del_row + position[0], del_col + position[1]):
                out.append((del_row + position[0], del_col + position[1]))

        return out

    def click_position(self, position: tuple[int, int]):
        if position in self.flags:
            return
        if position in self.mines:
            raise NotImplementedError("Game Over")
        row, col = position
        if self.grid[row][col] != -1:
            return
        self.revealed.add(position)
        if len(self.revealed) >= self.width * self.height - len(self.mines):
            raise NotImplementedError("Game Won!")
        neighbors = self.get_neighbors(position)
        count = 0
        for neighbor in neighbors:
            if neighbor in self.mines:
                count += 1

        self.grid[row][col] = count
        if count == 0:
            for neighbor in neighbors:
                self.click_position(neighbor)
