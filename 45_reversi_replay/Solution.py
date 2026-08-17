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

    def go_direction(self, direction, position, player):
        point = (position[0] + direction[0], position[1] + direction[1])
        opposite = self.get_opposite(player)
        changed = set()
        while self.valid(point) and self.grid[point[0]][point[1]] == opposite:
            changed.add(point)
            point = (point[0] + direction[0], point[1] + direction[1])
        if self.valid(point) and self.grid[point[0]][point[1]] == player:
            return len(changed), changed
        return 0, set()

    def valid_move(self, player, position):
        if self.grid[position[0]][position[1]] is not None:
            return False
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
        for direction in directions:
            amount, _ = self.go_direction(direction, position, player)
            if amount > 0:
                return True

        return False

    def flip(self, player, position):
        if not self.valid_move(player, position):
            raise NotImplementedError("not implemented. not a valid move")
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
            converted, to_change = self.go_direction(direction, position, player)
            for change in to_change:
                self.grid[change[0]][change[1]] = player
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

    def has_move(self, player):
        for i in range(8):
            for j in range(8):
                if self.valid_move(player, (i, j)):
                    return True
        return False

    def replay(self, moves, starting_player):
        curr_player = starting_player
        for move in moves:
            if not self.has_move(curr_player):
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
                if not self.valid_move(player, (row, col)):
                    continue
                total_amount = 0
                for direction in directions:
                    amount, _ = self.go_direction(direction, (row, col), player)
                    total_amount += amount
                if total_amount > best_amount:
                    best_position = (row, col)
                    best_amount = total_amount
        return best_position
