# save/load JSON snapshot

import json
from typing import Any, Dict
from .board import Board, CellState, GameState
from .rng import RNG

class Snapshot:
    """
    Save and load game state to/from JSON file.
    """
    @staticmethod
    def save(board: Board, filepath: str) -> None:
        """
        Save board state to JSON file.
        """

        data = {
            "width": board.width,
            "height": board.height,
            "num_mines": board.num_mines,
            "seed": board.rng.seed,
            "first_click_done": board.first_click_done,
            "game_state": board.game_state,
            "revealed_count": board.revealed_count,
            "flag_count": board.flag_count,
            "state": [[board.state[y][x] for x in range(board.width)]
                         for y in range(board.height)],
            "mines": list(board.mines) if board.mines else None,
            "counts": {f"{x},{y}": count for (x, y), count in board.counts.items()}
                     if board.counts else None
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load(filepath: str) -> Board:
        """
        Load board state from JSON file.
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        rng = RNG(data["seed"])
        board = Board(data["width"], data["height"], data["num_mines"], rng)

        board.first_click_done = data["first_click_done"]
        board.game_state = data["game_state"]
        board.revealed_count = data["revealed_count"]
        board.flag_count = data["flag_count"]

        board.state = [[data["state"][y][x] for x in range(board.width)]
                        for y in range(board.height)] 
        
        if data["mines"] is not None:
            board.mines = set(tuple(m) for m in data["mines"])
        if data["counts"] is not None:
            board.counts = {}
            for key, count in data["counts"].items():
                x, y = map(int, key.split(','))
                board.counts[(x, y)] = count
        
        return board