# first-click-safe mine placement, neighbor counts
#--------------------------------------------------

from typing import Set, Tuple
from .rng import RNG

class Generator:
    """
    Generates mine placements with first-click safety.
    
    Invariants:
     Mines are placed only after first click
     First click cell and its 8 neighbors never contain mines
     Exacty the requested number of mines are placed 
     """

    def __init__(self, width: int, height: int, num_mines: int, rng: RNG):
        """
        Initialize generator with board dimensions and mine count.
        """
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.rng = rng

    def palce_mines(self, first_x: int, first_y: int) -> Set[Tuple[int, int]]:
        """
        Place mines avoiding first click and its neighbors.
        Args:
         first_x : X coordinate of first click
         first_y: Y coordinate of first click

        Returns:
         Set of (x, y) tuples representing mine positions
        """

        forbidden = self._get_neighbors_with_counter(first_x, first_y)

        available_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if(x, y) not in forbidden:
                    available_cells.append((x, y))


        max_mines = min(self.num_mines, len(available_cells))
        mine_positions = set(self.rng.sample(available_cells, max_mines))

        return mine_positions

    def _get_neighbors_with_counter(self, x: int, y: int) -> Set[Tuple[int, int]]:
        """
        Get cell and its 8 neighbors.
        """
        neighbors = {(x, y)}
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.add((nx, ny))

        return neighbors

    @staticmethod
    def get_neighbors(x: int, y: int, width: int, height: int) -> Set[Tuple[int, int]]:
        """
        Get 8 neighbors of cell, exculding center.
        """
        enighbors = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    neighbors.add((nx, ny))
                
        return neighbors

    @staticmethod
    def compute_counts(mines: Set[Tuple[int, int]], width: int, height: int) -> dict:
        """
        Compute neighbor mine counts for all cell.

        Returns:
            Dict mapping (x, y) -> count of adjacent mines

            """
        counts = {}
        for y in range(height):
            for x in range(width):
                if (x, y) in mines:
                    counts[(x, y)] = -1
                else:
                    neighbors = Generator.get_neighbors(x, y, width, height)
                    count = sum(1 for n in neighbors if n in mines)
                    counts[(x, y)] = count
                    
        return counts


    
        
    


