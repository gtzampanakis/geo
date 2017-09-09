import heapq

import geomath as gm

def join_on_distance_threshold(
    coords_1_iterator_factory,
    coords_2_iterator_factory,
    threshold
):
    """
    Performs an 'INNER JOIN ON (DISTANCE(A,B) <= threshold)'
    """
    assert threshold >= 0
    for c1 in coords_1_iterator_factory():
        c2_iterator = coords_2_iterator_factory()
        for c2 in c2_iterator:
            if gm.gc_dist_coords(c1, c2) <= threshold:
                yield (c1, c2)

def join_on_k_closest(
    coords_1_iterator_factory,
    coords_2_iterator_factory,
    k
):
    """
    Performs an 'INNER JOIN ON (A IN {k closest points to B})'
    """
    assert k >= 1
    # heapq.pop() returns the smallest item so we use the opposite of the
    # distance function
    def dfn(c1_, c2_): return -gm.gc_dist_coords(c1_, c2_)
    for c1 in coords_1_iterator_factory():
        c2_iterator = coords_2_iterator_factory()
        items = []
        coords = []
        for c2 in c2_iterator:
            d = dfn(c1, c2)
            # Sorting by this item effectively means sorting by the first element
            # and as a bonus we keep a reference to the coords to which "d"
            # applies.
            item = (d, c2) 
            if len(items) < k:
                heapq.heappush(items, item)
            elif len(items) == k:
                if item > items[0]:
                    heapq.heapreplace(items, item)
            assert len(items) <= k
        for item in items:
            yield (c1, item[1])

