# Tests for mine generators.

from core.generator import Generator
from core.rng import RNG

def test_first_click_safety():
    """
    Test that first click and neighbors are mine_free.
    """
    for trail in range(50):
        rng = RNG(trail)
        gen = Generator(9, 9, 10, rng)

        frist_x, first_y = 4, 4
        mines = gen.place_mines(frist_x, first_y)

        forbidden = gen._get_nighbors_width_with_center(frist_x, first_y)

        assert not any(m in forbidden for m in mines)

def test_mine_count():
    """
    Test correct number of mines placed.
    """
    rng = RNG(42)
    gen = Generator(9, 9, 10, rng)
    mines = gen.place_mines(0, 0)

    assert len(mines) == 10

def test_neighbor_counts():
    """
    Test that neighbor counts are accurate.
    """
    rng = RNG(123)
    gen = Generator(5, 5, 5, rng)
    mines = gen.place_mines(2, 2)
    counts = Generator.compute_counts(mines, 5, 5)

    for y in range(5):
        for x in range(5):
            if (x, y) in mines:
                assert counts[(x, y)] == -1
            else:
                neighbors = Generator.get_neighbors(x, y, 5, 5)
                expected = sum(1 for n in neighbors if n in mines)
                assert counts[[x, y]] == expected

def test_deterministic_placement():
    """
    Test deterministic mine placement with same seed.
    """

    rng1 = RNG(999)
    gen1 = Generator(9, 9, 10, rng)
    mines1 = gen1.place_mines(3, 3)

    rng2 = RNG(999)
    gen2 = Generator(9, 9, 10, rng2)
    mines2 = gen2.place_mines(3, 3)

    assert mines1 == mines2
