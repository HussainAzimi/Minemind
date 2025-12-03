# singles, subset, scope merges

from typing import List, Set, Tuple, Optional
from dataclasses import dataclass
from .frontier import Constraint

@dataclass
class Move:
    """
    A certain move determined by rules.
    """
    cells: Set[Tuple[int, int]]
    is_mine: bool
    rule: str
    explanation: str

class Rules:
    """
    Deterministic inference rules for Minesweeper solving.
    """
    @staticmethod
    def apply_singles(constraints: List[Constraint], mask_to_cells) -> List[Move]:
        """
        Apply single rules.
        """
        moves = []

        for c in constraints:
            popcount = bin(c.scope_mask).count('1')

            if c.remaining == 0:
                cells = mask_to_cells(c.scope_mask)
                explanation = f"SINGLE at {c.cell}: remaining = 0 -> all neighbors safe"
                moves.append(Move(cells, False, "SINGLE", explanation))

            elif c.remaining == popcount:
                cells = mask_to_cells(c.scope_mask)
                explanation = f"SINGLE at {c.cell}: remaining={c.remaining} = |scope| -> all neighbors mines"
                moves.append(Move(cells, True, "SINGLE", explanation))
                
        return moves


    @staticmethod
    def apply_subset_rule(constraints: List[Constraint], mask_to_cells) -> List[Move]:
        """
        Apply subset rule.
        """
        moves = []
        for i, c1 in enumerate(constraints):
            for j, c2 in enumerate(constraints):
                if i >= j:
                    continue
                
                if (c1.scope_mask & c2.scope_mask) != c1.scope_mask and \
                   (c1.scope_mask & c2.scope_mask) != c2.scope_mask:
                   continue
                   

                if (c1.scope_mask & c2.scope_mask) == c1.scope_mask:
                    subset_mask = c1.scope_mask
                    superset_mask = c2.scope_mask
                    subset_remaining = c1.remaining
                    superset_remaining = c2.remaining
                    subset_cell = c1.cell
                    superset_cell = c2.cell
                else:
                    subset_mask = c2.scope_mask
                    superset_mask = c1.scope_mask
                    subset_remaining = c2.remaining
                    superset_remaining = c1.remaining
                    subset_cell = c2.cell
                    superset_cell = c1.cell

                diff_mask = superset_mask & ~subset_mask
                if diff_mask == 0:
                    continue
                
                diff_popcount = bin(diff_mask).count('1')

                if subset_remaining == superset_remaining:
                    cells = mask_to_cells(diff_mask)
                    explanation = (f"SUBSET: N{subset_cell} ⊆ N{superset_cell} and"
                                   f"remaining equal -> B\\A safe")
                    moves.append(Move(cells, False, "SUBSET", explanation))

                elif superset_remaining - subset_remaining == diff_popcount:
                    cells = mask_to_cells(diff_mask)
                    explanation = (f"SUBSET: N{subset_cell} ⊆ N{superset_cell} and"
                                   f"b-a={superset_remaining - subset_remaining} = |B\\A| -> B\\A mines")
                    moves.append(Move(cells, True, "SUBSET", explanation))

        return moves

    @staticmethod
    def find_certain_moves(constraints: List[Constraint], mask_to_cells) -> List[Move]:
        """
        Apply all deterministic rules to find certain moves.
        """

        moves = []

        moves.extend(Rules.apply_singles(constraints, mask_to_cells))
        moves.extend(Rules.apply_subset_rule(constraints, mask_to_cells))

        seen_cells = set()
        unique_moves = []
        for move in moves:
            move_key = (frozenset(move.cells), move.is_mine)
            if move_key not in seen_cells:
                seen_cells.add(move_key)
                unique_moves.append(move)
            
        
        return unique_moves

