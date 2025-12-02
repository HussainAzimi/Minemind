# Tests for solver with exact enumeration.

from core.board import Board, GameState
from core.rng import RNG
from core.solver import Solver

def test_solver_hint():
    """
    Test sovler hint functionality.
    """
    rng = RNG(42)
    board = Board(9, 9, 10, rng)
    solver = Solver(board)

    board.open(4, 4)
    hint = solver.get_hint()

    if hint:
        assert hint.cells
        assert hint.rule in ['SINGLE', 'SUBSET', 'EXACT']


def test_solver_probabilities():
    """
    Test probability calculation.
    """
    rng = RNG(100)
    board = Board(9, 9, 10, rng)
    solver = Solver(board)

    board.open(0, 0)
    
    probs = solver.compute_probabilities()

    for cell, prob in probs.items():
        assert 0.0 <= prob <= 1.0

def test_solver_auto():
    """
    Test auto-solve without guessing.
    """
    rng = RNG(200)
    board = Board(5, 5, 3, rng)
    solver = Solver(board)

    board.open(2, 2)

    steps, log = solver.auto_solve(allow_guess=False, limit=50)

    assert steps >= 0

def test_enumeration_small_component():
    """
    Test exact enumeration on small component.
    """
    rng = RNG(123)
    board = Board(5, 5, 2, rng)
    solver = Solver(board, k_max=10)

    board.open(2, 2)

    probs = solver.compute_probabilities()

    for prob in probs.values():
        assert 0.0 <= prob <= 1.0

def test_guess_selection():
    """
    Test best guess selection.
    """
    rng = RNG(42)
    board = Board(9, 9, 10, rng)
    solver = Solver(board)

    board.open(4, 4)

    guess = solver._select_best_guess()
    
    if guess:
        x, y = guess
        assert 0 <= x < board.width
        assert 0 <= y < board.height
