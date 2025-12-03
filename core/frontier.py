# build frontier, local indexing, component extraction

from typing import Set, Tuple, List, Dict
from dataclasses import dataclass
from .board import Board, CellState
from .generator import Generator
from .dsu import DSU

@dataclass
class Constraint:
    """
    A constraint from a revealed numbered cell.
    """
    cell: Tuple[int, int]
    scope_mask: int
    remaining: int


class Frontier:
    """
    Frontier of revealed cells adjacent to unknowns.
    """

    def __init__(self, board: Board):
        """
        Extract frontier form current board state.
        """
        self.board = board
        self.unknowns: List[Tuple[int, int]] = []
        self.unknown_to_idx: Dict[Tuple[int, int], int] = {}
        self.constraints: List[Constraint] = []

        self._extract_frontier()

    def _extract_frontier(self):
        """
        Build frontier constraints with local indexing.
        """
        unknowns_set = set()
        frontier_cells = []

        for y in range(self.board.height):
            for x in range(self.board.width):
                if self.board.get_state(x, y) == CellState.UNKNOWN:
                    unknowns_set.add((x, y))
                elif self.board.get_state(x, y) == CellState.REVEALED:
                    count = self.board.get_count(x, y)
                    
                    if count is not None and count > 0:
                        neighbors = Generator.get_neighbors(x, y, self.board.width, self.board.height)
                        has_unknown = any(self.board.get_state(nx, ny) == CellState.UNKNOWN 
                                        for nx, ny in neighbors) 
                        if has_unknown:
                            frontier_cells.append((x, y))
        
        self.unknowns = sorted(unknowns_set)
        self.unknown_to_idx = {cell: idx for idx, cell in enumerate(self.unknowns)}

        for fx, fy in frontier_cells:
            neighbors = Generator.get_neighbors(fx, fy, self.board.width, self.board.height)

            scope_mask = 0
            flagged_count = 0

            for nx, ny in neighbors:
                state = self.board.get_state(nx, ny)
                if state == CellState.UNKNOWN:
                    idx = self.unknown_to_idx[(nx, ny)]
                    scope_mask |= (1 << idx)
                elif state == CellState.FLAGGED:
                    flagged_count += 1
                
            if scope_mask > 0:
                count = self.board.get_count(fx, fy)
                if count is not None:
                    remaining = count - flagged_count
                    constraint = Constraint((fx, fy), scope_mask, remaining)
                    self.constraints.append(constraint)

    def get_components(self) -> List[Tuple[List[Constraint], Set[int]]]:
        """
        Decompose frontier into independent components using DSU

        Return: list of (constraints, unknown_indices) for each component
        """

        if not self.constraints:
            return []
        constraint_indices = set(range(len(self.constraints)))
        dsu = DSU(constraint_indices)

        for i in range(len(self.constraints)):
            for j in range(i + 1, len(self.constraints)):
                if self.constraints[i].scope_mask & self.constraints[j].scope_mask:
                    dsu.union(i, j)
        components_map = dsu.get_components()
        components = []

        for constraint_set in components_map.values():
            comp_constraints = [self.constraints[i] for i in sorted(constraint_set)]

            unknowns_mask = 0
            for c in comp_constraints:
                unknowns_mask |= c.scope_mask

            unknown_indices = set()
            for idx in range(len(self.unknowns)):
                if unknowns_mask & (1 << idx):
                    unknown_indices.add(idx)

            components.append((comp_constraints, unknown_indices))

        return components

    def mask_to_cells(self, mask: int) -> Set[Tuple[int, int]]:
        """
        Convert bitmask to set of cell coordinates.
        """
        cells = set()
        for idx in range(len(self.unknowns)):
            if mask & (1 << idx):
                cells.add(self.unknowns[idx])
        return cells

    def cells_to_mask(self, cells: Set[Tuple[int, int]]) -> int:
        """
        Convert set of cells to bitmask.
        """
        mask = 0
        for cell in cells:
            if cell in self.unknown_to_idx:
                idx = self.unknown_to_idx[cell]
                mask |= (1 << idx)
        return mask

                


