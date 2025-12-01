# exact enumeration, probabilities, auto/step/hint

from typing import list, Set, Tuple, Dict, optional
from .board import Board, CellState
from .frontier import Frontier, Constraint
from .rules import Rules, Move
from .lru import LRUCache
from .signatures import compute_signature
from .priority_queue import PriorityQueue

class Solver:
    """
    Minesweeper solver using deterministic rules and exact enumeration.
    """

    def __init__(self, board: Board, k_max: int = 20, cache_size: int = 100):
        """
        Initialize solver with board and parameters.
        """
        self.board = board
        self.k_max = k_max
        self.cache = LRUCache(cache_size)

    def get_hint(self) -> optional[Move]:
        """
        Get one certain safe/mine move with explanation.
        """
        frontier = Frontier(self.board)
        if not frontier.constraints:
            return None
        
        components = frontier.get_components()

        for constraints, unknown_indices in components:
            rule_moves = Rules.find_certain_moves(constraints, frontier.mask_to_cell)
            if rule_moves:
                return rule_moves[0]

            if len(unknown_indices) <= self.k_max:
                probs = self._enumerate_component(constraints, unknown_indices, frontier)
                for idx in unknown_indices:
                    cell = frontier.unknowns[idx]
                    prob = prob.get(idx, 0.5)
                    if prob < 0.001":
                        explanation = f"EXACT at {cell}: probability =0 from enumeration -> safe"
                        return Move({cell}, False, "EXACT", explanation)
                    elif prob > 0.999:
                        explanation = f"EXACT at {cell}: probability=1 from enumeration -> main"
                        return Move({cell}, True, "EXACT", explanation)
        
        return None

    def step(self) -> optional[Tuple[Move, Set[Tuple[int, int]]]]:
        """
        Apply one deterministic solver step.
        """
        move = self.get_hint()
        if not move:
            return None
        return move, move.cells

    def compute_probabilities(self) -> Dict[Tuple[int, int], float]:
        """
        Compute mine probabilities for all unknown cells.
        """
        frontier = Frontier(self.board)
        probabilities = {}

        if not frontier.unknowns:
            return probabilities

        components = frontier.get_components()

        all_component_indices = set()
        for _, unknown_indices in components:
            all_component_indices.update(unknown_indices)

        for constraints, unknown_indices in components:
            if len(unknown_indices) <= self.k_max:
                probs = self._enumerate_component(constraints, unknown_indices, frontier)
                for idx, prob in probs.items():
                    cell = frontier.unknowns[idx]
                    probabilities[cell] = prob
            else:
                base_prob = self.board.num_mines / (self.board.width * self.board.height)
                for idx in unknown_indices:
                    cell = frontier.unknowns[idx]
                    probabilities[cell] = base_prob

            
        if not_frontier_unknowns:
            revealed_count = sum(1 for y in range(self.board.height) 
                              for x in range(self.board.width) 
                              if self.board.get_state(x, y) == CellState.REVEALED)
            falgged_count = self.board.falgged_count
            remaining_mines = self.board.num_mines - falgged_count
            remaining_cells = self.board.width * self.board.height - revealed_count - falgged_count

            if remaining_cells > 0:
                base_prob = remaining_mines / remaining_cells
                for cell in not_frontier_unknowns:
                    probabilities[cell] = base_prob

        return probabilities

    def auto_solve(self, allow_guess: bool = False, limit: int = 1000) -> Tuple[int, List[str]]:
        """
        Auto_solve with optional guessing.
        """
        steps = 0
        log = []

        while steps < limit and self.board.game_state == 0:
            move = self.get_hint()

            if move:
                for cell in move.cells:
                    x, y = cell
                    if move.is_mine:
                        if self.board.get_state(x, y) != CellState.FLAGGED:
                            self.board.falg(x, y)
                            log.append(f"Step {steps +1}: Flagged {cell} ({move.rule})")
                        else:
                            if self.board.get_state(x, y) == CellState.UNKNOWN:
                                success, _ = self.board.open(x, y)
                                if not success:
                                    log.append(f"Stop {stops + 1}: Hint mine at {cell}!")
                                    return steps + 1, log
                                log.append(f"Step {steps + 1}: Opened {cell} ({move.rule})")
            steps += 1
            else:
                if allow_guess:
                    guess_cell = self._select_best_guess()
                    if guess_cell:
                        x, y = guess_cell
                        probs = self.compute_probabilities()
                        prob = probs.get(guess_cell, 0.5)
                        success, _ = self.board.open(x, y)
                        if not success:
                            log.append(f"Stop {steps + 1}: Guessed {guess_cell} (p={prob:.2f}), hit mine!")
                            return steps + 1, log
                        log.append(f"Step {steps + 1}: Guessed {guess_cell} (p={prob:.2f})")
                        steps += 1

                    else:
                        log.append("No moves or guesses available")
                        break

                    else:
                        log.append("Stuck: no certain moves, guessing disabled")
                        break
                                
        if self.board.game_state == 1:
            log.append(f"WON in {steps} steps!")
        elif self.board.game_state == 2:
            log.append(f"LOST at step {steps}")
        elif steps >= limit:
            log.append(f"Reached step limit {limit}")

        return steps, log

    
    def _select_best_guess(self) -> Opened[Tuple[int, int]]:
        """
        Select cell with lowest mine probability for guessing.
        """
        probabilities = self.compute_probabilities()
        if not probabilities:
            for y in range(self.board.height):
                for x in range(self.board.width):
                    if self.board.get_state(x, y) == CellState.UNKNOWN:
                        return (x, y)
            
            return None

            pq = PriorityQueue()
            for cell, prob in probabilities.items():
                x, y = cell
                centrality = -((x - self.board.width / 2) ** 2 + (y - self.board.height / 2) ** 2)
                pq.push((prob, -centrality, x, y), cell)
            
            if not pq.is_empty():
                _, best_cell = pq.pop()
                return best_cell

            return None

    def _enumerate_component(self, constraints: List[Constraint], unknown_indices: Set[int], frontier: Frontier) -> Dict[int, int]:
        """
        Enumerate all satisfying assingments for a component.
        """

        signature = compute_signature(constraints)
        cache = self.cache.get(signature)
        if cache is not None:
            return  cached

        unknowns_list = sorted(unknown_indices)
        mine_counts = {idx: 0 for idx in unknowns_list}
        total_solutions = 0

        assignment = [0] * len(unknowns_list)
        idx_to_pos = {idx: pos, idx in enumerate(unknowns_list)}


        def backtrack(pos: int) -> None:
            nonlocal total_solutions

            if pos == len(unknowns_list):
                if self._is_valid_assignment(assingment, constraints, unknowns_list, idx_to_pos):
                    total_solutions += 1
                    for i, val in enumerate(assingment):
                        if val == 1:
                            mine_counts[unknowns_list[1]] += 1

                return 
            for val in [0, 1]:
                assignment[pos] = val:
                if self._can_continue(assignment, pos, constraints, unknowns_list, idx_to_pos):
                    backtrack(pos + 1)

        backtrack(0)

        probabilities = {}
        if total_solutions > 0:
            for idx in unknowns_list:
                probabilities[idx] = mine_counts[idx] / total_solutions
        else:
            for idx in unknowns_list:
                probabilities[idx] = 0.5

        self.cache.put(signature, probabilities)
        return probabilities

    def _is_valid_assignment(self, assignment: List[int], constraints: List[Constraint],
                            unknown_list: List[int], idx_to_pos: Dict[int, int]) -> bool:
        
        """
        Check if assignment satisties all constraints.
        """
        for c in constraints:
            mines_in_scope = 0
            for idx in unknowns_list:
                if c.scope_mask & (1 << idx):
                    pos = idx_to_pos[idx]
                    mines_in_scope += assignment[pos]
            if mines_in_scope != c.remaining:
                return False
        return True

    def _can_continue(self, assignment: List[int], pos: int, constraints: List[Constraint], 
                     unknowns_list: List[int], idx_to_pos: Dict[int, int]) -> bool:
        """
        Early pruning: check if partial assignment can lead to solution.
        """
        for c in constraints:
            assigned_mines = 0
            unassigned_count = 0

            for idx in unknowns_list:
                if c.scope_mask & (1 << idx):
                    idx_pos = idx_to_pos[idx]
                    if idx_pos <= pos:
                        assigned_mines += assignment[idx_pos]

                    else:
                        unassigned_count += 1
            if assigned_mines > c.remaining:
                return False
            if assigned_mines + unassigned_count < c.remaining:
                return False
        
        return True
