# Test for deterministic solver rules.


from core.frontier import Constraint
from core.rules import Rules


def test_singles_all_safe():
    """
    Test singles rule for all safe.
    """
    def mask_to_cells(mask):
        cells = set()
        for i in range(8):
            if mask & (1 << i):
                cells.add((i, 0))

        return cells

    constraints = [Constraint((5, 5), 0b00001111, 0)]
    moves = Rules.apply_singles(constraints, mask_to_cells)

    assert len(moves) == 1
    assert not moves[0].is_mine
    assert len(moves[0].cells) == 4

def test_singles_all_mines():
    """
    Test singles rule for all mines.
    """
    def mask_to_cells(mask):
        cells = set()
        for i in range(8):
            if mask & (1 << i):
                cells.add((i, 0))

        return cells

    constraints = [Constraint((5, 5), 0b00000111, 3)]
    moves = Rules.apply_singles(constraints, mask_to_cells)

    assert len(moves) == 1
    assert moves[0].is_mine
    assert len(moves[0].cells) == 3

def test_subset_rule():
    """
    Test subset rule.
    """
    def mask_to_cells(mask):
        cells = set()
        for i in range(8):
            if mask & (1 << i):
                cells.add((i, 0))
        return cells

    constraints = [
        Constraint((5, 5), 0b00000011, 1),
        Constraint((6, 5), 0b00000111, 1)
    ]
    moves = Rules.apply_subset_rule(constraints, mask_to_cells)

    assert len(moves) >= 1

    for move in moves:
        if not move.is_mine:
            assert (2, 0) in move.cells

