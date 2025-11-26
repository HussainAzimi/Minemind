# first-click-safe mine placement, neighbor counts
#--------------------------------------------------
import random
from typing import List, Tuple

class Generator:
    def __init__(self, width: int, height: int, mines: int, seed: int | None = None):
        self.width = width
        self.height = height
        self.mines = mines
        self.seed = seed
        self.rng = random.Random(seed)


    def _neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Return valid neighbor coordinates arround (x, y)
        """
        coords = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    coords.append((nx, ny))
        return coords
    

    def palce_mines(self, first_click: Tuple[int, int]) -> List[List[int]]:

        fx, fy = first_click

        forbidden = {(fx, fy)} | set(self._neighbors(fx, fy))

        all_cells = [(x, y) for x in range(self.width) for y in range(self.height)
                     if (x, y) not in forbidden]

        mine_cells = set(self.rng.sample(all_cells, self.mines))

        grid = [[0 for _ in range(self.height)] for _ in range(self.width)]
        for (x, y) in mine_cells:
            grid[x][y] = -1

        for x in range(self.width):
            for y in range(self.height):
                if grid[x][y] == -1:
                    continue
                count = sum(1 for (nx, ny) in self._neighbors(x, y)
                             if grid[x][y] == -1)
                grid[x][y] = count

        return grid
        

gen = Generator(width=9, height=9, mines=10, seed=42)
grid = gen.palce_mines((3, 3))
for y in range(gen.height):
    row = []
    for x in range(gen.width):
        val = grid[x][y]
        row.append("*" if val == -1 else str(val))
    print(" ".join(row)) Washington University in St. Louis
WashU.edu