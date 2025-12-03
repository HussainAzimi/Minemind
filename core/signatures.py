# canonical component signature

from typing import List, Tuple
from .frontier import Constraint

def compute_signature(constraints: List[Constraint]) -> Tuple:
    """
    Compute canonical signature for a component.
    Signature is a tuple of (sorted scope masks, corresponding remaining values).
    This allow caching of enumeration results for indentical constraint patterns.

    """

    pairs = [(c.scope_mask, c.remaining) for c in constraints]
    pairs.sort()
    
    masks = tuple(p[0] for p in pairs)
    remaining = tuple(p[1] for p in pairs)

    return (masks, remaining)