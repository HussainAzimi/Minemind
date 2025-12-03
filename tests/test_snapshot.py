# Tests for save/load snapshots.

import os
import tempfile
from core.board import Board
from core.rng import RNG
from core.snapshot import Snapshot


def test_save_load_round_trip():
    """
    Test that save/load preserves state.
    """
    rng = RNG(42)
    board = Board(9, 9, 10, rng)

    board.open(4, 4)
    board.flag(1, 1)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        filepath = f.name

    try:
        Snapshot.save(board, filepath)
        loaded_board = Snapshot.load(filepath)

        assert loaded_board.width == board.width
        assert loaded_board.height == board.height
        assert loaded_board.num_mines == board.num_mines
        assert loaded_board.first_click_done == board.first_click_done
        assert loaded_board.revealed_count == board.revealed_count
        assert loaded_board.flag_count == board.flag_count
        
        for y in range(board.height):
            for x in range(board.width):
                assert loaded_board.get_state(x, y) == board.get_state(x, y)
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

def test_load_determinism():
    """
    Test that loaded games behave deterministically.
    """
    rng = RNG(999)
    board = Board(9, 9, 10, rng)

    board.open(4, 4)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        filepath = f.name

    try:
        Snapshot.save(board, filepath)

        loaded1 = Snapshot.load(filepath)
        loaded2 = Snapshot.load(filepath)

        assert loaded1.mines == loaded2.mines
    
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)



