import copy


class left_L:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = (width - 2, height - 2)
        self.space = [(0, 1), (0, 0), (1, 0), (2, 0)]
        self.next_rotate = {
            ((0, 1), (0, 0), (1, 0), (2, 0)): [(0, 0), (1, 0), (2, 0), (2, 1)],
            ((0, 0), (1, 0), (2, 0), (2, 1)): [(1, 0), (1, 1), (1, 2), (0, 2)],
            ((1, 0), (1, 1), (1, 2), (0, 2)): [(0, 0), (0, 1), (1, 1), (2, 1)],
            ((0, 0), (0, 1), (1, 1), (2, 1)): [(0, 1), (0, 0), (1, 0), (2, 0)],
        }

    def rotate(self):
        tmp = left_L(self.width, self.height)
        tmp.space = self.next_rotate[self.space]
        tmp.position = self.position
        return tmp

    def move_down(self):
        tmp = left_L(self.width, self.height)
        tmp.space = self.space
        tmp.position = (self.position[0] - 1, self.position[1])
        return tmp

    def get_locations(self):
        locs = []
        for diffs in self.space:
            locs.append((diffs[0] + self.position[0] + diffs[1] + self.position[1]))
        return locs


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for i in range(width)] for i in range(height)]
        self.piece = None

    def try_move(self, new_piece):
        curr_loc = new_piece.get_locations()
        for loc in curr_loc:
            if (
                loc[0] < 0
                or loc[0] >= len(self.grid)
                or loc[1] < 0
                or loc[1] >= len(self.grid[0])
                or self.grid[loc[0]][loc[1]] == 1
            ):
                return False
        return True

    def gravity(self):
        new_piece = self.piece.move_down()
        if self.try_move(new_piece):
            self.piece = new_piece
            return True
        else:
            curr_loc = self.piece.get_locations()
            for loc in curr_loc:
                self.grid[loc[0]][loc[1]] = 1
            return False

    def rotate(self):
        new_piece = self.piece.rotate()
        if self.try_move(new_piece):
            self.piece = new_piece
            return True
        else:
            return False
