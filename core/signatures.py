# canonical component signature

from typing import List, Tuple
from .frontier import Constraint

def compute_signature(constraints: List[Constraint]) -> tuple:
    """
    Compute canonical signature for a component.
    Signature is a tuple of (sorted scope masks, corresponding remaining values).
    This allow caching of enumeration results for indentical constraint patterns.

    """

    paris = [(c.scope_mask, c.remaining) for c in constraints]
    paris.sort()
    
    masks = Tuple(p[0] for p in paris)
    remaining = tuple(p[1] for p in paris)

    return (masks, remaining)