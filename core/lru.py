# LRU cache

from collections import OrderedDict
from typing import Any, Optional

class LRUCache:
    """
    LRU cache with fixed capacity.

    """

    def __init__(self, capacity: int):
        """
        Initialize LRU cache with given capacity.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive.")
        self.capacity = capacity
        self.cache: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        """
        Get value for key, marking it as recently used.
        Return None if key not found.
        """

        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> None:
        """
        Put key value pair, marking as recently used
        """

        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(slef.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate(self, key: Any) -> None:
        """
        Remove key from cache if present.
        """
        self.cache.pop(key, None)

    def clear(self) -> None:
        """
        Clear all entries form cache.
        """
        self.cache.clear()

    def _len__(self) -> int:
        """
        Return current cache size.
        """
        return len(self.cache)
