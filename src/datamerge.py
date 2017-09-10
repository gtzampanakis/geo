import heapq

import geotypes as gt
import fileio as fio
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

def path_to_coords_iterator(path):
    for row in fio.get_csv_reader(path):
        coords = row['__coords']
        coords.data = row
        yield coords

def join_files(path1, path2, threshold=None, k_closest=None):
    assert threshold is None or k_closest is None
    assert threshold is not None or k_closest is not None

    args = [
        lambda: path_to_coords_iterator(path1),
        lambda: path_to_coords_iterator(path2),
    ]

    if threshold is not None:
        fn = join_on_distance_threshold
        args.append(threshold)
    elif k_closest is not None:
        fn = join_on_k_closest
        args.append(k_closest)

    filter_names = ['__line_number', '__coords']
    for c_pair in fn(*args):
        out_row = {}

        for k,v in c_pair[0].data.iteritems():
            if k in filter_names:
                continue
            out_row[k] = v

        for k,v in c_pair[1].data.iteritems():
            if k in filter_names:
                continue
            if k in out_row:
                out_row['1_' + k] = out_row[k]
                del out_row[k]
                out_row['2_' + k] = v

        yield out_row
