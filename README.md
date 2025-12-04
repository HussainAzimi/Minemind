# Individual Course Project.
## Overview

MineMind is a command-line Minesweeper game featuring an intelligent solver that uses logical reasoning and probabilistic analysis. Built entirely with Python 3.11+ standard library, it demonstrates advanced algorithms including Union-Find for component decomposition, constraint satisfaction with exact enumeration, and probability-based decision making. The game provides a complete REPL interface for playing, auto-solving, and analyzing Minesweeper boards with deterministic, reproducible gameplay through seeded random generation.

## Features

- **Classic Minesweeper gameplay** with first-click safety guarantee
- **Advanced solver** using deterministic rules and exact constraint enumeration
- **Probability analysis** for optimal guess selection
- **Component decomposition** using Union-Find for efficient solving
- **Save/load** game states to JSON
- **Deterministic** gameplay with optional seeding for reproducibility

## Installation

```bash
# Clone or download the repository
cd minemind

# No external dependencies required - uses Python 3.11+ stdlib only
```
## Quick Start

```bash
# Start a new game (beginner)
python -m minemind new --w 9 --h 9 --mines 10 --seed 42

# Start different difficulty levels
python -m minemind new --w 16 --h 16 --mines 40  # Intermediate
python -m minemind new --w 30 --h 16 --mines 99  # Expert
```

## Command Cheatsheet

### Game Commands
- `help` - Show all commands
- `new --w W --h H --mines M [--seed S]` - Start new game with custom dimensions
- `show [--reveal]` - Display current board state (--reveal shows all mines)
- `quit` or `exit` - Exit the program

### Playing Commands
- `open X Y` - Reveal cell at column X, row Y (zero-indexed)
- `flag X Y` - Toggle flag at position
- `chord X Y` - Auto-reveal neighbors if flags match number

### Solver Commands
- `hint` - Get one certain safe/mine move with explanation
- `step` - Apply one solver step automatically
- `auto [--guess] [--limit N]` - Auto-solve up to N steps (--guess enables guessing)
- `prob` - Show ASCII probability heatmap for unknown cells
- `frontier` - Display frontier component analysis

### Save/Load
- `save PATH` - Save current game to JSON file
- `load PATH` - Load game from JSON file

## Example Session

```
$ python -m minemind new --w 9 --h 9 --mines 10 --seed 42
New game: 9x9, 10 mines, seed=42
MineMind v1.0 - Type 'help' for commands

> show
    0 1 2 3 4 5 6 7 8
  0 . . . . . . . . .
  1 . . . . . . . . .
  2 . . . . . . . . .
  3 . . . . . . . . .
  4 . . . . . . . . .
  5 . . . . . . . . .
  6 . . . . . . . . .
  7 . . . . . . . . .
  8 . . . . . . . . .

> open 4 4
Revealed 46 cell
    0 1 2 3 4 5 6 7 8
  0 · · · · · · · · ·
  1 · · · · · · · · ·
  2 · · · 2 2 2 2 · ·
  3 · · · 1     1 · ·
  4 · · · 1     1 1 1
  5 · 1 1 1
  6 · 1
  7 · 1
  8 · 1

  > hint
MINE: (7, 3) - SINGLE at (6, 4): remaining=1 = |scope| -> all neighbors mines

> step
Applied SINGLE: Flagged (7, 3)
    0 1 2 3 4 5 6 7 8
  0 · · · · · · · · ·
  1 · · · · · · · · ·
  2 · · · 2 2 2 2 · ·
  3 · · · 1     1 F ·
  4 · · · 1     1 1 1
  5 · 1 1 1
  6 · 1
  7 · 1
  8 · 1
  
> auto --limit 100
Auto-solving (guess=False, limit=100)...
Auto-solving (guess=False, limit=100)...
 Step 14: Opened (8, 0) (SINGLE)
 Step 14: Opened (8, 0) (SINGLE)
 Step 15: Flagged (2, 0) (SINGLE)
 Step 15: Flagged (2, 0) (SINGLE)
 Step 15: Flagged (2, 1) (SINGLE)
 Step 16: Opened (1, 1) (SUBSET)
 Step 15: Flagged (2, 1) (SINGLE)
 Step 16: Opened (1, 1) (SUBSET)
 Step 17: Opened (0, 1) (SINGLE)
 Step 18: Flagged (1, 3) (SINGLE)
 Step 18: Flagged (1, 3) (SINGLE)
 Step 19: Opened (0, 3) (SINGLE)
 Step 20: Flagged (0, 7) (SINGLE)
 Step 19: Opened (0, 3) (SINGLE)
 Step 20: Flagged (0, 7) (SINGLE)
 Step 21: Opened (0, 8) (SINGLE)
 Step 20: Flagged (0, 7) (SINGLE)
 Step 21: Opened (0, 8) (SINGLE)
 WON in 21 steps!
 Step 21: Opened (0, 8) (SINGLE)
 WON in 21 steps!
 WON in 21 steps!
    0 1 2 3 4 5 6 7 8
    0 1 2 3 4 5 6 7 8
  0   2 F F 3 2 1 1 1
  1   2 F 4 F F 1 1 F
  2 1 2 2 2 2 2 2 2 2
  2 1 2 2 2 2 2 2 2 2
  3 1 F 2 1     1 F 1
  4 1 2 F 1     1 1 1
  5   1 1 1
  6 1 1
  7 F 1
  8 1 1

🎉 YOU WIN! 🎉
  
> save my_game.json
Saved to my_game.json

> quit
Goodbye!
```
## Board Symbols

- `·` (dot) - Unknown cell
- `F` - Flagged cell
- ` ` (space) - Revealed zero (no adjacent mines)
- `1-8` - Revealed number (adjacent mine count)
- `*` - Mine (shown on loss or with --reveal flag)

## Solver Strategy

The solver uses a multi-layered approach:

1. **Deterministic Rules**
   - **Singles Rule**: If remaining mines = 0, all unknown neighbors are safe; if remaining = scope size, all are mines
   - **Subset Rule**: For constraints A ⊆ B, deduce safe/mine cells from set differences

2. **Exact Enumeration** (for components with ≤20 unknowns)
   - Backtracking search with early pruning
   - Computes exact mine probabilities for each cell
   - Uses LRU cache for repeated constraint patterns

3. **Guess Selection** (when enabled with --guess)
   - Selects cell with lowest mine probability
   - Prefers central cells as tiebreaker

## Known Limitations

- Large components (>20 unknowns) use baseline probability estimates
- Chord requires exact flag count match (no safety checks)
- No undo functionality (use save/load for checkpointing)

```
core/
├── __init__.py
├── board.py         # Grid state, open/flag/chord
├── dsu.py           # Union-Find for components
├── frontier.py      # Constraint extraction
├── generator.py     # First-click-safe mine placement
├── lru.py           # LRU cache
├── priority_queue.py# Min-heap wrapper
├── rng.py           # Seeded random generator
├── rules.py         # Deterministic inference
├── signatures.py    # Component caching
├── snapshot.py      # Save/load JSON
└── solver.py        # Exact enumeration & auto-solve
minemind/
├── __init__.py
├── __main__.py      # Entry point
├── cli.py           # REPL and command handlers
├── render.py        # ASCII board rendering
tests/
├── test_board.py    # Test chord mechanic
├── test_dsu.py      # Tests for Union-Find (DSU) data structure
├── test_frontier.py # Tests for frontier extraction and components
├── test_generator.py# Tests for mine generators
├── test_lru.py      # Tests for LRU cache
├── test_rules.py    # Tests for deterministic solver rules
├── test_snapshot.py # Tests for save/load snapshots
├── test_solver_small.py# Tests for solver with exact enumeration

```

# Testing

```bash
# Run all tests
> python -m pytest tests/ -v 

# Run with coverage
> pytest tests/ --cov=minemind --cov-report=term-missing

29 comprehensive tests cover:
- Data structures (DSU, LRU cache)
- Mine generation and first-click safety
- Board mechanics (flood fill, chord, win detection)
- Frontier extraction and component decomposition
- Solver rules and exact enumeration
- Save/load round-trip fidelity

# License

Educational project - Fall 2025 data structures and algorithms final project.
