from core.board import Board, CellState, GameState
from core.rng import RNG

def test_board_initial_state():
    """
    Test board initialization.
    """
    rng = RNG(42)
    board = Board(9, 9, 10, rng)

    assert board.width == 9
    assert board.height == 9
    assert board.num_mines == 10
    assert board.game_state == GameState.PLAYING
    assert not board.first_click_done



def test_first_click_places_mines():
    """
    Test that mines are placed on first click.
    """
    rng = RNG(42)
    board = Board(9, 9, 10, rng)

    assert board.mines is None
    board.open(4, 4)

    assert board.mines is not None
    assert len(board.mines) == 10
    assert (4, 4) not in board.mines


def test_flood_fill():
    """
    Test flood fill on zero cells.
    """
    rng = RNG(100)
    board = Board(9, 9, 1, rng)

    success, revealed = board.open(0, 0)

    assert success
    assert len(revealed) > 1


def test_flag_toggle():
    """
    Test flag toggling.
    """
    rng = RNG(100)
    board = Board(9, 9, 10, rng)


    assert board.flag(3, 3)
    assert board.get_state(3, 3) == CellState.FLAGGED

    assert board.flag(3, 3)
    assert board.get_state(3, 3) == CellState.UNKNOWN


def test_chord():
    """
    Test chord mechanic.
    """
    rng = RNG(50)
    board = Board(9, 9, 5, rng)

    board.open(0, 0)

    from  core.generator import Generator
    for y in range(board.height):
        for x in range(board.width):
            if board.get_state(x, y) == CellState.REVEALED:
                count = board.get_count(x, y)
                if count is not None and count > 0:
                    neighbors = Generator.get_neighbors(x, y, board.width, board.height)
                    mines_nearby = [n for n in neighbors if board.is_mine(n[0], n[1])]

                    for mx, my in mines_nearby:
                        if board.get_state(mx, my) ==  CellState.UNKNOWN:
                            board.flag(mx, my)

                    success, revealed = board.chord(x, y)
                    if len(mines_nearby) == count:
                        assert success
                    
                    return

def test_win_condition():
    """
    Test win detection.
    """
    rng = RNG(1000)
    board = Board(3, 3, 1, rng)

    for y in range(3):
        for x in range(3):
            if board.get_state(x, y) == CellState.UNKNOWN and not board.is_mine(x, y):
                board.open(x, y)

    if board.revealed_count == 3 * 3 - 1:
        assert board.game_state == GameState.WON
    



    