from Solution import Othello, Player


def print_grid(grid):
    for row in grid:
        print(grid[row])


def test_flip():
    print("starting")
    othello = Othello()
    new_move = othello.bot(Player.ONE)
    assert new_move is not None
    new = othello.replay([new_move])
    curr_player = Player.TWO
    count = 0
    while count < 2:
        print(new)
        print_grid(othello.grid)
        new_move = othello.bot(curr_player)
        if new_move is None:
            count += 1
            continue
        count = 0
        new = othello.replay([new_move])
        curr_player = othello.get_opposite(curr_player)
    print_grid(othello.grid)

    print("ending")
