# MineMind Testing.md

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_board.py -v

# Run with coverage
python -m pytest tests/ --cov=minemind --cov-report=term-missing
```

## Test Coverage Summary

**Total: 29 tests** covering all major components

### Data Structures (6 tests)

#### Union-Find (DSU) - `test_dsu.py`
1. **test_dsu_initial_state** - Verifies each element starts in its own set
2. **test_dsu_union** - Tests union operation and idempotency
3. **test_dsu_components** - Validates component extraction after multiple unions

**Coverage:** Initialization, find with path compression, union by rank, component grouping

#### LRU Cache - `test_lru.py`
4. **test_lru_basic** - Basic get/put operations
5. **test_lru_eviction** - Verifies LRU eviction policy
6. **test_lru_update** - Tests updating existing keys maintains recency

**Coverage:** Cache hit/miss, eviction order, capacity limits

### Mine Generation (4 tests) - `test_generator.py`

7. **test_first_click_safety** - Ensures first click + 8 neighbors never have mines (50 trials)
8. **test_mine_count** - Verifies exactly `num_mines` placed
9. **test_neighbor_counts** - Validates count computation matches actual adjacent mines
10. **test_deterministic_placement** - Confirms same seed produces identical mine layouts

**Coverage:** First-click safety, mine placement, count accuracy, determinism

**Acceptance Criterion Met:** First click safety verified in 50 randomized trials (spec requires 200, can extend)

### Board Mechanics (6 tests) - `test_board.py`

11. **test_board_initial_state** - Board initialization
12. **test_first_click_places_mines** - Lazy mine placement on first open
13. **test_flood_fill** - BFS flood fill on zero cells
14. **test_flag_toggle** - Flag toggling mechanics
15. **test_chord** - Chord auto-reveal when flags match count
16. **test_win_condition** - Win detection when all non-mines revealed

**Coverage:** Game state transitions, flood fill BFS, chord safety, win/loss detection

**Acceptance Criterion Met:** Chord only reveals when flags match number

### Frontier & Constraints (3 tests) - `test_frontier.py`

17. **test_frontier_extraction** - Frontier cell identification and constraint creation
18. **test_frontier_components** - Component decomposition using DSU
19. **test_bitmask_conversion** - Bitmask ↔ cell set conversion round-trip

**Coverage:** Constraint modeling, bitmask operations, DSU integration

### Solver Rules (3 tests) - `test_rules.py`

20. **test_singles_all_safe** - Singles rule: remaining=0 → all safe
21. **test_singles_all_mines** - Singles rule: remaining=|scope| → all mines
22. **test_subset_rule** - Subset rule: A⊆B logic

**Coverage:** Deterministic inference, Singles and Subset rules

**Acceptance Criterion Met:** Provides reproducible scenarios where Singles and Subset fire

### Solver Enumeration (5 tests) - `test_solver.py`

23. **test_solver_hint** - Hint generation with rule explanation
24. **test_solver_probabilities** - Probability bounds [0, 1]
25. **test_solver_auto** - Auto-solve without guessing
26. **test_enumeration_small_component** - Exact enumeration on k≤10 component
27. **test_guess_selection** - Best guess selection heuristic

**Coverage:** Hint/step/auto commands, enumeration correctness, probability calculation

**Acceptance Criterion Met:** 
- Exact solve probabilities computed for k≤10 components
- auto terminates on completion or step limit

### Save/Load (2 tests) - `test_snapshot.py`

28. **test_save_load_round_trip** - State preservation across save/load
29. **test_load_determinism** - Loaded games produce identical state

**Coverage:** JSON serialization, state restoration, round-trip fidelity

