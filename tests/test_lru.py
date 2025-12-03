# Tests for LRU cache.

from core.lru import LRUCache

def test_lru_basic():
    """
    Test basic LRU cache operations.
    """
    cache = LRUCache(2)
    cache.put('a', 1)
    cache.put('b', 2)

    assert cache.get('a') == 1
    assert cache.get('b') == 2
    assert cache.get('c') is None

def test_lru_eviction():
    """
    Test LRU eviction.
    """
    cache = LRUCache(2)
    cache.put('a', 1)
    cache.put('b', 2)
    cache.put('c', 3)

    assert cache.get('a') is None
    assert cache.get('b') == 2
    assert cache.get('c') == 3

def test_lru_update():
    """
    Test updating existing key.
    """
    cache = LRUCache(2)
    cache.put('a', 1)
    cache.put('b', 2)
    cache.get('a')
    cache.put('c', 3)

    assert cache.get('a') == 1
    assert cache.get('b') is None

