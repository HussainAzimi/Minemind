# seeded RNG

import random
from typing import Optional

class RNG:
    """
    Wrapper around Python's random module with explicit seeding.
    """
    def __init__(self, seed: Optional[int]):
        """
        Initialize RNG with optional seed.
        """
        self.seed = seed
        self.rng = random.Random(seed)

    def randint(self, a: int, b: int) ->int:
        """
        Return random integer N such that a <= N <= b.
        """
        return self.rng.randint(a, b)

    def shuffle(self, lst: list) -> None:
        """
        Shuffle list in place.
        """
        self.rng.shuffle(lst)

    def choice(self, seq):
        """
        Return random element form non-empty sequence.
        """
        return self.rng.choice(seq)

    def sample(self, population, k: int):
        """
        Return k-length list of unique elements from population.
        """
        return self.rng.sample(population, k)