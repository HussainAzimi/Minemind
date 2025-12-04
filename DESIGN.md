# MineMind DESIGN.md

## Architecture Overview

MineMind follows a modular architecture separating game mechanics, solver logic, and presentation:


![Architecture overview](/Architecture%20_overview.png)

## Core Components

### 1. Board State (`board.py`)
**Invariants:**
- Cells are in one of three states: UNKNOWN, REVEALED, FLAGGED
- Revealed cells cannot be flagged
- Mines are placed lazily on first `open()` call
- First click and its 8 neighbors are always mine-free
- Counts accurately reflect adjacent mines: `count[x,y] = |{mines in neighbors(x,y)}|`

**State Transitions:**
```
UNKNOWN ──flag()──> FLAGGED
   │                   │
   └───────┬───────────┘
           │
       open() (if not mine)
           │
           ▼
       REVEALED
```

**Flood Fill Algorithm:**
When opening a zero-count cell, perform BFS:
1. Start from clicked cell
2. Reveal current cell
3. If count == 0, add all unknown neighbors to queue
4. Repeat until queue empty

### 2. Mine Generation (`generator.py`)

**First-Click Safety:**
```
Forbidden zone = {first_click} ∪ neighbors(first_click)
Available cells = all_cells \ forbidden_zone
Mines = random_sample(available_cells, num_mines)
```

**Invariants:**
- Exactly `num_mines` mines placed (or fewer if board too small)
- Deterministic with same seed
- Counts computed after placement: `count[x,y] = Σ_{n ∈ neighbors(x,y)} is_mine(n)`

### 3. Frontier Extraction (`frontier.py`)

**Frontier Definition:**
A cell `v` is in the frontier iff:
- `state[v] = REVEALED`
- `count[v] > 0`
- `∃ neighbor n : state[n] = UNKNOWN`

**Constraint Modeling:**
For each frontier cell `v` with label `L` and unknown neighbors `N(v)`:
```
Constraint: Σ_{u ∈ N(v)} x_u = L - |{flagged neighbors}|
where x_u ∈ {0, 1} (1 = mine)
```

**Bitmask Encoding:**
- Unknown cells mapped to local indices: `0, 1, 2, ..., k-1`
- Scope represented as integer bitmask: `scope_mask = Σ 2^i for i in scope`
- Enables fast set operations: `A ∩ B = a & b`, `A ∪ B = a | b`, `A \ B = a & ~b`

**Example:**
```
Frontier cell at (5, 5) with label 2
Unknown neighbors: (4,4), (5,4), (6,4)  → indices 0, 1, 2
scope_mask = 0b00000111 (bits 0, 1, 2 set)
remaining = 2 - 0 = 2 (no flags)
```


### 4. Component Decomposition (`dsu.py`)

**Intersection Graph:**
Build graph where:
- Nodes = constraints
- Edge (c1, c2) exists iff `scope[c1] ∩ scope[c2] ≠ ∅`

**DSU Algorithm:**
```python
dsu = DSU(constraint_indices)
for i, j in pairs(constraints):
    if constraints[i].scope_mask & constraints[j].scope_mask != 0:
        dsu.union(i, j)
```

**Invariants:**
- Each component is independent (no shared unknowns between components)
- Components can be solved in parallel
- DSU maintains: `parent[x] = root` after `find(x)` (path compression)

**Component Structure:**
```
Component = {
    constraints: [(scope_mask, remaining), ...],
    unknowns: {indices of unknown cells}
}
```

## Solver Architecture

### Data Flow: hint/step/auto

```
Board State
    │
    ▼
Extract Frontier
    │
    ▼
Build Constraints (bitmasks)
    │
    ▼
Decompose into Components (DSU)
    │
    ├──> For each component:
    │    ├──> Apply deterministic rules
    │    │    (Singles, Subset)
    │    │         │
    │    │         ▼
    │    │    Found certain move? ──Yes──> Return
    │    │         │
    │    │        No
    │    │         │
    │    └──> If k ≤ k_max:
    │         Exact enumeration
    │              │
    │              ▼
    │         Compute probabilities
    │              │
    │              ▼
    │         p=0 or p=1? ──Yes──> Return
    │
    └──> No certain moves found
         │
         ▼
    (Optional) Select best guess
    (lowest probability)
```

### 5. Deterministic Rules (`rules.py`)

**Singles Rule:**
```
If remaining == 0:
    → All cells in scope are SAFE
If remaining == |scope|:
    → All cells in scope are MINES
```

**Subset Rule:**
Given constraints `(A, a)` and `(B, b)` where `A ⊆ B`:
```
If a == b:
    → B \ A are SAFE (same mines, different scope)
If b - a == |B \ A|:
    → B \ A are MINES (difference exactly fills gap)
```

**Example:**
```
C1: cells {0, 1, 2}, remaining = 2
C2: cells {0, 1}, remaining = 2
→ Subset: {0, 1} ⊆ {0, 1, 2}
→ Since a == b: cell 2 is SAFE
```

### 6. Exact Enumeration (`solver.py`)

**Backtracking Search:**
```python
def enumerate(assignment, pos):
    if pos == k:  # All assigned
        if valid(assignment):
            count_solution()
        return
    
    for value in [0, 1]:  # Try mine/safe
        assignment[pos] = value
        if can_continue(assignment, pos):  # Early pruning
            enumerate(assignment, pos + 1)
```

**Early Pruning:**
For each constraint `c`:
```
assigned_mines = count(assignment[i] for i in c.scope if i ≤ pos)
unassigned = count(i for i in c.scope if i > pos)

Prune if:
  - assigned_mines > c.remaining (too many mines)
  - assigned_mines + unassigned < c.remaining (not enough slots)
```

**Probability Calculation:**
```
For each cell i:
    p_mine[i] = (# solutions with assignment[i]=1) / (total solutions)
```

**Caching:**
- Key = `(sorted(scope_masks), sorted(remaining_values))`
- Cache hit → reuse probabilities (component structure identical)
- Invalidate on any board change affecting component

### 7. LRU Cache (`lru.py`)

**Implementation:**
Uses `collections.OrderedDict`:
- `get(key)`: move to end (most recent)
- `put(key, val)`: insert at end, evict first if at capacity

**Invariants:**
- Size never exceeds capacity
- Most recently used items at end
- Least recently used at beginning

## Complexity Analysis

See `COMPLEXITY.md` for detailed time/space complexity of all operations.

## Testing Strategy

See `TESTING.md` for comprehensive test coverage documentation.
