# grid state, open/flag/chord, flood fill

from typing import Set, Tuple, Optional
from collections import deque
from .generator import Generator
from .rng import RNG


class CellState:
    """
    Cell visibility states.
    """
    UNKNOWN = 0
    REVEALED = 1
    FLAGGED = 2

class GameState:
    """
    Game outcome states.
    """
    PLAYING = 0
    WON = 1
    LOST = 2

class Board:
    """
    Minesweeper board with game mechanics.

    Invariants:
     Cells are either UNKNOWN, REVEALED, or FLAGGED
     Revealed cells cannot to flagged
     Mines placed after first open, avoiding first click + neighbors
     Counts accurately reflect adjacent mines
    """

    def __init__(self, width: int, height: int, num_mines: int, rng: RNG):
        """
        Initialize board with dimensions and mine count.
        """
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.rng = rng

        self.state = [[CellState.UNKNOWN for _ in range(width)] for _ in range(height)]
        self.mines: Optional[Set[Tuple[int, int]]] = None   
        self.counts: Optional[dict] = None

        self.first_click_done = False
        self.game_state = GameState.PLAYING
        self.revealed_count = 0
        self.flag_count = 0

    def open(self, x: int, y: int) -> Tuple[bool, Set[Tuple[int, int]]]:
        """ 
        Open cell at (x, y).

        Returns:
         (success, revealed_cells) where success is False if mine hit, and
         revealed_cells is set of newly revealed positions
        """
        if not self._in_bounds(x, y):
            return False, set()

        if self.state[y][x] != CellState.UNKNOWN:
            return True, set()
        
        if not self.first_click_done:
            self._place_mines(x, y)
            self.first_click_done = True

        if self.mines is not None and (x, y) in self.mines:
            self.state[y][x] = CellState.REVEALED
            self.game_state = GameState.LOST
            return False, {(x, y)}

        revealed = self._flood_fill(x, y)
        self.revealed_count += len(revealed)

        if self.revealed_count == self.width * self.height - self.num_mines:
            self.game_state = GameState.WON

        return True, revealed

    def flag(self, x: int, y: int) -> bool:
        """
        Toggle flag at (x, y)
        True if flag state changed, False otherwise
        """
        if not self._in_bounds(x, y):
            return False
        if self.state[y][x] == CellState.REVEALED:
            return False

        if self.state[y][x] == CellState.UNKNOWN:
            self.state[y][x] = CellState.FLAGGED
            self.flag_count += 1
            return True
        
        elif self.state[y][x] == CellState.FLAGGED:
            self.state[y][x] = CellState.UNKNOWN
            self.flag_count -= 1
            return True
        
        return False

    def chord(self, x: int, y: int) -> Tuple[bool, Set[Tuple[int, int]]]:
        """
        Chord at (x, y): if revealed number and flags match count, then
        reveal all unflagged neighbors.

        Returns:
         (success, revealed_cells) where success is False if mine hit
        """

        if not self._in_bounds(x, y):
            return True, set()
        
        if self.state[y][x] != CellState.REVEALED:
            return True, set()
        if self.counts is None or self.counts[(x, y)] == 0:
            return True, set()

        neighbors = Generator.get_neighbors(x, y, self.width, self.height)
        flagged = sum(1 for nx, ny in neighbors if self.state[ny][nx] == CellState.FLAGGED)

        if self.counts is None or flagged != self.counts[(x, y)]:
            return True, set()

        all_revealed = set()
        for nx, ny in neighbors:
            if self.state[ny][nx] == CellState.UNKNOWN:
                success, revealed = self.open(nx, ny)
                all_revealed.update(revealed)
                if not success:
                    return False, all_revealed

        return True, all_revealed
    
    def _place_mines(self, first_x: int, first_y: int):
        """
        Place mines avoiding first click and neighbors.
        """
        generator = Generator(self.width, self.height, self.num_mines, self.rng)
        self.mines = generator.place_mines(first_x, first_y)
        self.counts = Generator.compute_counts(self.mines, self.width, self.height)

    def _flood_fill(self, x: int, y: int) -> Set[Tuple[int, int]]:
        """
        Flood fill from (x, y) revealing zeros and their perimeter.
        Uses BFS
        Return: set of revealed cell positions
        """

        revealed  = set()
        queue = deque([(x, y)])
        visited = {(x, y)}

        while queue:
            cx, cy = queue.popleft()
            self.state[cy][cx] = CellState.REVEALED
            revealed.add((cx, cy))

            if self.counts is not None and self.counts[(cx, cy)] == 0:
                neighbors = Generator.get_neighbors(cx, cy, self.width, self.height)
                for nx, ny in neighbors:
                    if (nx, ny) not in visited and self.state[ny][nx] == CellState.UNKNOWN:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

        return revealed

    def _in_bounds(self, x: int, y: int) -> bool:
        """
        Check if coordinates are within board bounds.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_state(self, x: int, y: int) -> int:
        """
        Get cell state (UNKNOWN, REVEALED, FLAGGED).
        """
        if not self._in_bounds(x, y):
            return CellState.UNKNOWN
        return self.state[y][x]

    def get_count(self, x: int, y: int) -> Optional[int]:
        """
        Get mine count for cell (None if mines not placed yet).
        """
        if self.counts is None:
            return None
        return self.counts.get((x, y))

    def is_mine(self, x: int, y: int) -> bool:
        """
        Check if cell is mine.
        """
        if self.mines is None:
            return False
        return (x, y) in self.mines

         




