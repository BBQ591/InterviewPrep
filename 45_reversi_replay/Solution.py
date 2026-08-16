from enum import Enum


class Player(Enum):
    ONE = 1
    TWO = 2


class Othello:
    def __init__(self):
        self.grid = {}
        for i in range(8):
            self.grid[i] = [None for i in range(8)]

        self.grid[3][3] = Player.TWO
        self.grid[3][4] = Player.ONE
        self.grid[4][3] = Player.ONE
        self.grid[4][4] = Player.TWO
        self.player_one = 2
        self.player_two = 2

    def valid(self, point):
        return point[0] in self.grid and point[1] >= 0 and point[1] < 8

    def get_opposite(self, player):
        return Player.TWO if player == Player.ONE else Player.ONE

    def go_direction(self, direction, position, player, change_board) -> int:
        point = (position[0] + direction[0], position[1] + direction[1])
        opposite = self.get_opposite(player)
        changed = 0
        while self.valid(point) and self.grid[point[0]][point[1]] == opposite:
            if change_board:
                self.grid[point[0]][point[1]] = player
            changed += 1
            point = (point[0] + direction[0], point[1] + direction[1])
        return changed

    def flip(self, player, position):
        directions = [
            [-1, -1],
            [1, 1],
            [-1, 1],
            [1, -1],
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
        ]
        self.grid[position[0]][position[1]] = player
        for direction in directions:
            converted = self.go_direction(direction, position, player, True)
            if player == Player.ONE:
                self.player_one += converted
                self.player_two -= converted
            else:
                self.player_two += converted
                self.player_one -= converted
        if player == player.ONE:
            self.player_one += 1
        else:
            self.player_two += 1

    def legal_moves(self, player) -> bool:
        directions = [
            [-1, -1],
            [1, 1],
            [-1, 1],
            [1, -1],
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
        ]
        for row in range(8):
            for col in range(8):
                for direction in directions:
                    if self.go_direction(direction, (row, col), player, False) > 0:
                        return True
        return False

    def replay(self, moves):
        curr_player = Player.ONE
        for move in moves:
            curr_valid = self.legal_moves(curr_player)
            curr_next_valid = self.legal_moves(self.get_opposite(curr_player))
            if not curr_valid and not curr_next_valid:
                break
            if not curr_valid:
                curr_player = self.get_opposite(curr_player)
            self.flip(curr_player, move)
            curr_player = self.get_opposite(curr_player)
        return (self.player_one, self.player_two)

    def bot(self, player):
        directions = [
            [-1, -1],
            [1, 1],
            [-1, 1],
            [1, -1],
            [0, 1],
            [0, -1],
            [1, 0],
            [-1, 0],
        ]
        best_position = None
        best_amount = 0
        for row in range(8):
            for col in range(8):
                if self.grid[row][col] is not None:
                    continue
                for direction in directions:
                    amount = self.go_direction(direction, (row, col), player, False)
                    if amount > best_amount:
                        best_position = (row, col)
                        best_amount = amount
        return best_position
