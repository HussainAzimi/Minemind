# Priority queue wrapper around heapq for clean min-heap operations.

import heapq
from typing import Any, List, Tuple, Optional

class PriorityQueue:
    """
    Min-heap priority queue.
    
    Elements are tuples (priority, item) where lower priority values come first.
    """
    def __init__(self):
        """
        Initialize empty priority queue.
        """
        self.heap: List[Tuple[Any, Any]] = []

    def push(self, priority: Any, item: Any) -> None:
        """
        Push item with given priority.
        """

        heapq.heappush(self.heap, (priority, item))

    def pop(self) -> Tuple[Any, Any]:
        """
        Pop and return (priority, item) with minimum priority.
        Raise IndexError if queue is empty.
        """
        return heapq.heappop(self.heap)

    def peek(self) -> Optional[Tuple[Any, Any]]:
        """
        Return (Priority, item) with minimum priority without removing it.
        Return None if queue is empty.
        """
        return self.heap[0] if self.heap else None

    def is_empty(self) -> bool:
        """
        Check if queue is empty
        """
        return len(self.heap) == 0

    def __len__(self) -> int:
        """
        Return number of items in queue.
        """
        return len(self.heap)

    def clear(self) -> None:
        """
        Remove all items from queue.
        """
        self.heap.clear()
