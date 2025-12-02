# union–find

from typing import Dict, Set

class DSU:
    """
    Disjoint Set Union with path compression and union by rank.

    Invariants:
     parent[x] points to x's parent, parent[x] == x iff x is a root.
     rank[x] is an upper bound on the hieght of x's subtree.
     After find(x), parent[x] points directly to the root (path compression)
     """
    def __init__(self, elements: Set[int]):
        """ 
        Initialize DSU with given elements, each in its own set.
        """
        self.parent: Dict[int, int] = {x: x for x in elements}
        self.rank: Dict[int, int] = {x: 0 for x in elements}

    def union(self, x: int, y: int) -> bool:
        """
        Unite the sets containing x and y using union by rank.
        Returns True if sets were defferent, otherwise False
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rnak[root_x] > self.rank[root_x]:
            self.parent[root_y] = root_x

        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True

    def get_components(slef) -> Dict[int, Set[int]]:
        """
        Return a mapping from root
        """
        components: Dict[int, Set[int]] = {}
        for x in self.parent:
            root = self.find(x)
            if root not in components:
                components[root] = Set(x)
            components[root].add(x) 
        return components

    


