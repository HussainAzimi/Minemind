# Test for frontier extraction and components.

from core.board import Board, CellState
from core.rng import RNG
from core.frontier import Frontier


def test_frontier_extraction():
    """
    Test frontier constraint extraction.
    """

    rng = RNG(42)
    board = Board(9, 9, 10, rng)
    board.open(4, 4)
    frontier = Frontier(board)

    assert len(frontier.unknown) > 0
    assert len(frontier.constraints) > 0

def test_frontier_components():
    """
    Test component decomposition.
    """
    rng = RNG(100)
    board = Board(9, 9, 10, rng)
    board.open(0, 0)
    board.open(8, 8)
    frontier = Frontier(board)
    components = frontier.get_components()

    assert len(components) >= 1

def test_bitmask_conversion():
    """
    Test bitmask to cells coversion.
    """
    rng = RNG(42)
    board = Board(5, 5, 3, rng)
    board.open(2, 2)
    frontier = Frontier(board)

    if frontier.constraints:
        mask = frontier.constraints[0].scope_mask
        cells = frontier.mask_to_cells(mask)

        reconstructed_mask = frontier.cells_to_mask(cells)
        assert mask == reconstructed_mask



    