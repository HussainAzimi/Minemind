# REPL and command handlers
#--------------------------

import sys
from typing import Optional
from core.rng import RNG
from core.board import Board, GameState
from core.solver import Solver
from core.snapshot import Snapshot
from  .render import Renderer

class CommandHandlers:
    """
    Handles user commands and game interaction.
    """
    def __init__(self):
        """
        initialize CLI with no active game.
        """
        self.board: Optional[Board] = None
        self.solver: Optional[solver]= None
        self.running = True

    def run(self, args=None):
        """
        Start REPL, optionally with initial new command.
        
        args: Parsed command-line arguments for initial setup.
        """
        if args and args.command == 'new':
            self._cmd_new(args.w, args.h, args.mines, args.seed)
        print("Welcome to MineMind game")
        print("\nMineMind v1.0 - type 'help' for commands")

        while self.running:
            try:
                line = input("> ").strip()
                if not line:
                    continue
                self._handle_command(line)
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                print(f"Error: {e}")

    def _handle_command(self, line: str):
        """
        Parse and execute command.
        """
        parts = line.split()
        cmd = parts[0].lower()

        if cmd in ['quit', 'exit']:
            self.running = False
            print("Goodbye!")
        
        elif cmd == 'help':
            self._cmd_help()
        
        elif cmd == 'show':
            self._cmd_show('--reveal' in parts)

        elif cmd == 'open':
            if len(parts) < 3:
                print("Usage: open X Y")
                return
            try:
                x, y = int(parts[1]), int(parts[2])
                self._cmd_open(x, y)
            except ValueError:
                print("Invalid Input")

        elif cmd == 'flag':
            if len(parts) < 3:
                print("Usage: flag X Y")
                return
            try:
                x, y = int(parts[1]), int(parts[2])
                self._cmd_flag(x, y)
            except ValueError:
                print("Invalid Input")

        elif cmd == 'chord':
            if len(parts) < 3:
                print("Usage: chord X Y")
                return
            try:
                x, y = int(parts[1]), int(parts[2])
                self._cmd_chord(x, y)
            except ValueError:
                print("Invalid Input")

        elif cmd == 'hint':
            self._cmd_hint()
        
        elif cmd == 'step':
            self._cmd_step()

        elif cmd == 'auto':
            allow_guess = '--guess' in parts
            limit = 1000
            for i, p in enumerate(parts):
                if p == '--limit' and i + 1 < len(parts):
                    try:
                        limit = int(parts[i + 1])
                    except ValueError:
                        pass
            self._cmd_auto(allow_guess, limit)
        
        elif cmd == 'prob':
            self._cmd_prob()

        elif cmd == 'frontier':
            self._cmd_frontier()

        elif cmd == 'save':
            if len(parts) < 2:
                print("Usage: save PATH")
                return
            self._cmd_save(parts[1])

        elif cmd == 'load':
            if len(parts) < 2:
                print("Usage load PATH")
                return
            self._cmd_load(parts[1])

        else:
            print(f"Unknown command: {cmd}. type 'help' for commands.")

    def _cmd_help(self):

        """
        Print help message.
        """
        print("""
Commands:
    help                                             - List commands
    new --w W --h H --mines M [--seed S]             - Start a new game
    show [--reveal]                                  - Print board; --reveal shows mines
    (debug/after loss)
    open X Y                                         - Reveal cell at (X,Y)
    flag X Y                                         - Toggle flag at (X, Y)
    chord X Y                                        - On a revealed number: if flags match,
    reveal remaining neighbors
    hint                                             - Print one certain safe/mine move with
    explanatio
    step                                             - Apply one deterministic solver step; or
    exact small-component ste
    auto [--guess] [--limit N]                       - Run solver up to N steps; --guess
    allows lowest-risk guesse
    prob                                             - Print coarse ASCII probability heatmap
    for unknown cell
    frontier                                         - Summary: #components, sizes, unknowns
    per componen
    save path.json                                   - Snapshot game state to JSON
    load path.json                                   - Restore snapshot from JSON 
    quit | exit                                      - Exit program
        
        """)
    def _parse_new(self, args):
        """
        Parse new command arguments.
        """
        width, height, mines, seed = 9, 9, 10, None
        i = 0
        while i < len(args):
            if args[i] == '--w' and i + 1 < len(args):
                width = int(args[i + 1])
                i += 2
            elif args[i] == '--h' and i + 1 < len(args):
                height = int(args[i + 1])
                i += 2
            elif args[i] == 'mines' and i + 1 < len(args):
                mines  = int(args[i + 1])
                i += 2
            elif args[i] == 'seed'  and i + 1 < len(args):
                seed = int(args[i + 1])
                i += 2
            else:
                i += 1
        self._cmd_new(width, height, mines, seed)
    
    def _cmd_new(self, width: int, height: int, mines: int, seed: Optional[int]):
        """
        Create new game
        """
        rng = RNG(seed)
        self.board = Board(width, height, mines, rng)
        self.solver = Solver(self.board)
        print(f"New game: {width}X{height}, {mines} mines" + 
        (f", seed={seed}" if seed is not None else ""))

    def _cmd_show(show, reveal: bool = False):
        """
        Display board
        """
        if not self.board:
            print("No active game, Enter 'new' to start.")
            return
        print(Renderer.render(self.board, reveal))
        
        elif self.board.game_state == GameState.WON:
            print("\n🎉 YOU WIN! 🎉")
        elif self.board.game_state == GameState.LOST:
            print("\n💥 GAME OVER 💥")

    def _cmd_open(self, x: int, y: int):
        """
        open cell
        """
        if not self.board:
            print("No active game.")
            return
        if self.board.game_state != GameState.PLYING:
            print("Game is over.")
            return
        
        success, revealed = self.board.open(x, y)
        print(f"Revealed {len(revealed)} cell")
        self._cmd_show()
    
    def _cmd_flag(self, x: int, y: int):
        """
        Toggle flag
        """
        if not self.board:
            print("No active game.")
            return
        if self.board.flag(x, y):
            print(f"Flag toggled at ({x}, {y})")
        else:
            print(f"Cannot flag ({x}, {y})")

    def _cmd_chord(self, x: int, y: int):
        """
        Chord at cell.
        """
        if not self.board:
            print("No active game.")
            return
        if self.board.game_state != GameState.PLYING:
            print("Game is over.")
            return
        success, revealed = self.board.chord(x, y)

        if revealed:
            print(f"Chorded, revealed {len(revealed)} cell")
            self._cmd_show
        else:
            print("Chord conditions not met or invalid cell")

    def _cmd_hint(self):
        """
        Get hint from solver.
        """
        if not self.board or not self.solver:
            print("No active game.")
            return

        move = self.solver.get_hint()
        if move:
            action = "MINE" if move.is_mine else "SAVE"
            cells_str = ", ".join(str(c) for c in sorted(move.cells))
            print(f"{action}: {cells_str} - {move.explanatio}")
        else:
            print("No certain moves found")

    def _cmd_step(self):
        """
        Apply one solver step.
        """
        if not self.board or not self.solver:
            print("No active game.")
            return

        result = self.solver.step()
        if result:
            move, cells = result
            action = "Flagged" if move.is_mine else "Opened"
            cells_str = ", ".join(str(c) for c in sorted(cells))
            print(f"Applied {move.rule}: {action} {cells_str}")

            for cell in cells:
                x, y = cell
                if move.is_mine:
                    self.board.flag(x, y)
                else:
                    self.board.open(x, y)
            self._cmd_show()
        else:
            print("No certain moves available.")

    def _cmd_auto(self, allow_guess: bool, limit: int):
        """
        Auto solve
        """
        if not self.board or not self.solve:
            print("No Active game.")
            return
            
        print(f"Auto-solving (guess={allow_guess}, limit={limit})...")
        step, log = self.solver.auto_solve(allow_guess, limit)

        for msg in log[-10:]:
            print(f" {msg}")
        
        self._cmd_show()

    def _cmd_prob(self):
        """
        Show probability heatmap.
        """
        if not self.board or not self.solver:
            print("No active game.")
            return

        probs = self.solver.compute_probabilities()
        print(Renderer.render_probabilites(self.board, probs))
        
    def _cmd_frontier(self):
        """
        Show frontier component summary.
        """
        if not self.board or not self.solver:
            print("No active game.")
            return

        from.core.frontier import Frontier
        frontier = Frontier(self.board)
        components = frontier.get_components()

        print(f"Frontier: {len(components)} components, {len(frontier.unknown)} unknown")
        print(f" Component {i + 1}: {len(constraints)} constraints, {len(unknown)} unknown")
    
    def _cmd_save(self, filepath: str):
        """
        Save game to file.
        """
        if not self.board:
            print("No Active game.")
            return
        Snapshot.save(self.board, filepath)
        print(f"Saved to {filepath}")

    def _cmd_load(self, filepath: str):
        """
        Load game from file.
        """
        try:
            self.board = Snapshot.load(filepath)
            self.solver = Solver(self.board)
            print(f"Loaded from {filepath}")
            self._cmd_show()
        except Exception as e:
            print(f"Failed to load: {e}")


def main():
    """
    Entry point for CLI.
    """
    import argparse

    parser = argparse.ArgumentParser(description="MineMind - CLI Minesweeper with Solver")
    parser.add_argument('command', nargs='?', default=None, help='Comamnd to execute')
    parser.add_argument('--w', type=int, default=9, help='Board width')
    parser.add_argument('--h', type=int, default=9, help='Board height')
    parser.add_argument('--mines', type=int, default=10, help='Number of mines')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')

    args = parser.parse_args()
    command_handler = CommandHandlers()
    command_handler.run(args)


if __name__ == '__main__':
    main()


