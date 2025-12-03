# Tests for Union-Find (DSU) data structure.

from core.dsu import DSU

def test_dsu_initial_state():
    """
    Test DSU initialization.
    """
    elements = {0, 1, 2, 3}
    dsu = DSU(elements)

    for x in elements:
        assert dsu.find(x) == x

def test_dsu_union():
    """
    Test union operation.
    """
    dsu = DSU({0, 1, 2, 3})

    assert dsu.union(0, 1) == True
    assert dsu.find(0) == dsu.find(1)

    assert dsu.union(0, 1) == False

def test_dsu_components():
    """
    Test component extraction.
    """
    dsu = DSU({0, 1, 2, 3, 4, 5})

    dsu.union(0, 1)
    dsu.union(1, 2)
    dsu.union(3, 4)

    components = dsu.get_components()
    assert len(components) == 3

    for comp in components.values():
        if 0 in comp:
            assert comp == {0, 1, 2}
        elif 3 in comp:
            assert comp == {3, 4}
        else:
            assert comp == {5}