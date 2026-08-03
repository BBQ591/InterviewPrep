from Solution import Match3
import copy

colors = ["b", "g", "r"]


def get_grid():
    return [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]]


def get_match():
    match_3 = Match3(colors, 5, 10)


def test_init():
    match_3 = Match3(
        colors,
        10,
        20,
    )
    for row in match_3.grid:
        for el in row:
            assert el in colors


def test_generate_el():
    match_3 = Match3(colors, 10, 20)
    assert match_3.generate_el() in colors


def test_switch_pos():
    grid1 = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]]
    match_3 = Match3(colors, 10, 20)
    expected = [[1, 2, 3, 4, 5], [13, 7, 8, 9, 10], [11, 12, 6, 14, 15]]
    assert match_3.switch_pos(grid1, (1, 0), (2, 2)) == expected


def test__check_move_true_row():
    match3_grid = [["r", "r", "r", "g", "g", "y"], ["g", "y", "b", "a", "a", "y"]]
    match3 = Match3(colors, 10, 20)
    assert match3._check_move(match3_grid)


def test__check_move_true_false():
    match3_grid = [
        ["r", "r", "a", "g", "g", "y"],
        ["r", "y", "b", "a", "a", "y"],
        ["r", "a", "c", "d", "e", "f"],
    ]
    match3 = Match3(colors, 10, 20)
    assert not match3._check_move(match3_grid)


def test_end_end():
    grid = [
        ["r", "r", "r", "r", "b", "g", "y"],
        ["b", "y", "r", "y", "b", "g", "y"],
        ["b", "y", "r", "y", "b", "a", "x"],
    ]
    tmp_grid = copy.deepcopy(grid)
    match_3 = Match3(colors, 3, 7)
    match_3.grid = grid
    assert match_3.reduce_moves(grid) != tmp_grid
    print(match_3.reduce_moves(grid))
