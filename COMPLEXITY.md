# MineMind COMPLEXITY.md

## Big‑O for Core Operations

### Board Actions
- **open(x, y):** O(1) normally; O(W×H) worst case (flood fill)  
- **flag(x, y):** O(1)  
- **chord(x, y):** O(W×H) worst case  

### Mine Setup
- **place_mines(first_x, first_y):** O(W×H)  
- **compute_counts(...):** O(W×H)  

### Frontier Extraction
- **_extract_frontier():** O(W×H)  
- **Space:** O(U + F)  

### Component Decomposition (DSU)
- **get_components():** O(F² × α(F))  
- **DSU find/union:** O(α(n)) amortized  

### Rule Passes
- **apply_singles(...):** O(F)  
- **apply_subset_rule(...):** O(F²)  
- **Total rules per pass:** O(F²)  

### Enumeration
- **_enumerate_component(...):** O(2^k × c × k) worst case  
  - k = unknowns in component  
  - c = constraints in component  
- **With pruning:** usually explores 1–10% of 2^k  
- **Space:** O(k) + recursion  

---

## Justification for `k_max = 20`

- **Exponential growth:**  
  - k=15 → 32K assignments  
  - k=20 → ~1M assignments (manageable)  
  - k=25 → ~33M assignments (too slow)  

- **Performance:**  
  - k ≤ 20 runs in ~10–100 ms  
  - k > 20 can take seconds → poor UX  

- **Practical observation:**  
  - Most components have k ≤ 15  
  - Rarely exceed k=20  
  - Larger components are usually unsolvable by logic alone  

- **Fallback strategy:**  
  - For k > 20, switch to probability‑based guesses  
  - Prevents exponential blowup  

---

## Quick Mental Model
- **Most operations:** linear in board size (O(W×H))  
- **Frontier logic:** cheap (O(F) to O(F²))  
- **Enumeration:** exponential, but capped at k ≤ 20  
- **Fallback:** guess when components are too big  
