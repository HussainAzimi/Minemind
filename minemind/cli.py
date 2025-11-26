# REPL and command handlers
#--------------------------

import sys
# from typing import Optional
# from .core.rng import rng
# from core.board import Board, GameState
# from .core.solver import Solver
# from .core.snapshot import Snapshot
# from .render import Renderer

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

command_test = CommandHandlers()

command_test.run()