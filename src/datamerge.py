import bisect
import collections
import heapq

import geotypes as gt
import fileio as fio
import geomath as gm

MID_R = 6371 * 1000.

def build_index(coords_list):
    x_index = []
    y_index = []
    z_index = []
    for c in coords_list:
        x,y,z = gm.coords_to_n_vector(c)
        x_index.append((x, c))
        y_index.append((y, c))
        z_index.append((z, c))
    x_index.sort()
    y_index.sort()
    z_index.sort()
    return x_index, y_index, z_index

def join_on_distance_threshold(
    coords_1_iterator,
    coords_2_iterator,
    threshold # in meters
):
    """
    Performs an 'INNER JOIN ON (DISTANCE(A,B) <= threshold)'
    """
    threshold /= MID_R # normalized
    coords_1_list = list(coords_1_iterator)
    coords_2_list = list(coords_2_iterator)
    coords_2_indexes = build_index(coords_2_list)
    for c1 in coords_1_list:
        for c2 in coords_2_list:
            if gm.gc_dist_coords(c1, c2) <= threshold:
                yield (c1, c2)

def join_on_k_closest(
    coords_1_iterator,
    coords_2_iterator,
    k
):
    """
    Performs an 'INNER JOIN ON (A IN {k closest points to B})'
    """
    assert k >= 1
    coords_1_list = list(coords_1_iterator)
    coords_2_list = list(coords_2_iterator)
    # heapq.pop() returns the smallest item so we use the opposite of the
    # distance function
    def dfn(c1_, c2_): return -gm.gc_dist_coords(c1_, c2_)
    for c1 in coords_1_list:
        items = []
        coords = []
        for c2 in coords_2_list:
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

def path_to_coords_iterator(path, result_queue=None):
    rowi = None
    for rowi, row in enumerate(fio.get_csv_reader(path), 1):
        coords = gt.Coords(
            float(row['Latitude']),
            float(row['Longitude']),
            data=row
        )
        yield coords
        if result_queue and rowi % 100 == 0:
            result_queue.put({'type': 'PROGRESS', 'payload': rowi})
    if result_queue and rowi is not None:
        result_queue.put({'type': 'PROGRESS', 'payload': rowi})

def join_files(path1, path2, threshold=None, k_closest=None, result_queue=None):
    assert threshold is None or k_closest is None
    assert threshold is not None or k_closest is not None

    args = [
        path_to_coords_iterator(path1, result_queue),
        path_to_coords_iterator(path2),
    ]

    if threshold is not None:
        fn = join_on_distance_threshold
        args.append(threshold)
    elif k_closest is not None:
        fn = join_on_k_closest
        args.append(k_closest)

    filter_names = ['__line_number', '__coords']
    for c_pair in fn(*args):
        out_row = collections.OrderedDict()

        for k,v in c_pair[0].data.iteritems():
            if k in filter_names:
                continue
            out_row['1_' + k] = v

        for k,v in c_pair[1].data.iteritems():
            if k in filter_names:
                continue
            out_row['2_' + k] = v

        yield out_row
