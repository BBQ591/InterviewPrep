from enum import Enum
from typing import List


class Player(Enum):
    UNKNOWN = 0
    ONE = 1
    TWO = 2


class ConnectFour:
    def __init__(self, w, h, k):
        self.width = w
        self.height = h
        # self.grid = [[Piece.UNKNOWN for i in range(w)] for j in range(h)]
        self.player = Player.ONE
        self.k = k
        self.prev_move = None
        self.player_one_pieces = set()
        self.player_two_pieces = set()

    def drop(self, col: int) -> int:
        row = 0
        while (row, col) in self.player_one_pieces or (
            row,
            col,
        ) in self.player_two_pieces:
            row += 1
        if self.player == Player.ONE:
            self.player_one_pieces.add((row, col))
            self.player = Player.TWO
        else:
            self.player_two_pieces.add((row, col))
            self.player = Player.ONE
        self.prev_move = (row, col)
        return row

    #        column = [
    #            self.grid[i][col]
    #            for i in range(len(self.grid[0]))
    #            if self.grid[i][col] != Piece.UNKNOWN
    #        ]
    #        row = len(column)
    #        if self.player == Player.ONE:
    #            self.grid[row][col] = Piece.ONE
    #            self.player = Player.TWO
    #        if self.player == Player.TWO:
    #            self.grid[row][col] = Piece.TWO
    #            self.player = Player.ONE
    #
    #        self.prev_move = (row, col)
    #        return row

    def get_element(self, row, col):
        if (row, col) in self.player_one_pieces:
            return Player.ONE
        if (row, col) in self.player_two_pieces:
            return Player.TWO
        return Player.UNKNOWN

    #        if row < 0 or col < 0 or row >= len(self.grid) or col >= len(self.grid[0]):
    #            return None
    #        return self.grid[row][col]

    def check_elements(self, row, col, diffs):
        common = None
        for i in range(len(diffs)):
            new_row = row + diffs[i][0]
            new_col = col + diffs[i][1]
            piece = self.get_element(new_row, new_col)
            if common is None:
                common = self.get_element(new_row, new_col)
            if common != piece:
                return None
        if common == Player.ONE:
            return Player.ONE
        return Player.TWO

    def check_row(self, row, col) -> Player | None:
        diffs = [(i, 0) for i in range(self.k + 1)]
        for new_row in range(row - self.k, row + 1):
            check1 = self.check_elements(new_row, col, diffs)
            if check1 is not None:
                return check1
        return None

    def check_col(self, row, col) -> Player | None:
        diffs = [(0, i) for i in range(self.k + 1)]
        for new_col in range(col - self.k, col):
            check1 = self.check_elements(row, new_col, diffs)
            if check1 is not None:
                return check1
        return None

    def check_diag(self, row, col) -> Player | None:
        # this should be expand from this center point
        diffs = [(i, i) for i in range(self.k + 1)]
        diffs2 = [(-i, i) for i in range(self.k + 1)]
        for diff in range(-self.k, 1):
            new_row_1 = row - diff
            new_col_1 = col - diff
            new_row_2 = row + diff
            check1 = self.check_elements(new_row_1, new_col_1, diffs)
            if check1 is not None:
                return check1
            check2 = self.check_elements(new_row_2, new_col_1, diffs2)
            if check2 is not None:
                return check2
        return None

    def winner(self) -> Player | None:
        if self.prev_move is None:
            return None
        return self._winner(self.prev_move[0], self.prev_move[1])

    def _winner(self, row, col) -> Player | None:
        # what we could do for O(k) instead is count both directions and see how many there are and then add them together, and if they add together to be more than k, then someone has won

        row_winner = self.check_row(row, col)
        col_winner = self.check_col(row, col)
        diag_winner = self.check_diag(row, col)
        if row_winner:
            return row_winner
        if col_winner:
            return col_winner
        if diag_winner:
            return diag_winner
        return None

    def change_player(self, points_to_change, set_to_change):
        new_points = set()
        for point in points_to_change:
            set_to_change.remove(point)
            new_points.add((point[0] + 1, point[1]))
        for point in new_points:
            set_to_change.add(point)

    def get_moves_col(self, col, set_to_inspect):
        out = set()
        for point in set_to_inspect:
            if point[1] == col:
                out.add(point)
        return out

    def check_winners(self, move):
        all_moves = self.get_moves_col(
            move, self.player_one_pieces
        ) + self.get_moves_col(move, self.player_two_pieces)
        all_winners = set()
        for point in all_moves:
            tmp_winner = self._winner(point[0], point[1])
            if tmp_winner is not None:
                all_winners.add(tmp_winner)
        return all_winners

    def play(self, moves: List[int]):
        winners = set()
        first_winner = -1
        for i, move in enumerate(moves):
            moves_player_one = self.get_moves_col(move, self.player_one_pieces)
            self.change_player(moves_player_one, self.player_one_pieces)
            moves_player_two = self.get_moves_col(move, self.player_two_pieces)
            self.change_player(moves_player_two, self.player_two_pieces)
            winners_tmp = self.check_winners(move)
            if first_winner == -1 and len(winners_tmp) > 0:
                first_winner = i
            winners |= winners_tmp
            if i % 2 == 0:
                self.player_one_pieces.add((0, move))
            else:
                self.player_two_pieces.add((0, move))
        return first_winner, winners
