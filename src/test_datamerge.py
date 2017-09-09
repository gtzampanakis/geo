import unittest

import geomath as gm
import geotypes as gt
import datamerge as dm

class DataMergeTestCase(unittest.TestCase):
    
    def test_join_on_distance_threshold_1(self):
        a = [gt.Coords(0, 0)]
        b = [gt.Coords(0, 0)]
        self.assertEqual(
            list(dm.join_on_distance_threshold(
                lambda: a,
                lambda: b,
                1
            )),
            [(a[0], b[0])]
        )

    def test_join_on_distance_threshold_2(self):
        a = [gt.Coords(0, 0)]
        b = [gt.Coords(45, 0)]
        self.assertEqual(
            list(dm.join_on_distance_threshold(
                lambda: a,
                lambda: b,
                1
            )),
            []
        )

    def test_join_on_distance_threshold_3(self):
        a = [gt.Coords(0, 0), gt.Coords(0, 0)]
        b = [gt.Coords(45, 0)]
        self.assertEqual(
            list(dm.join_on_distance_threshold(
                lambda: a,
                lambda: b,
                1
            )),
            []
        )

    def test_join_on_distance_threshold_4(self):
        a = [gt.Coords(0, 0), gt.Coords(0, 0)]
        b = [gt.Coords(0, 0), gt.Coords(0, 0)]
        self.assertEqual(
            list(dm.join_on_distance_threshold(
                lambda: a,
                lambda: b,
                1
            )),
            [
                (a[0], b[0]),
                (a[0], b[1]),
                (a[1], b[0]),
                (a[1], b[1]),
            ]
        )

    def test_join_on_k_closest_1(self):
        a = [gt.Coords(0, 0)]
        b = [gt.Coords(0, 0), gt.Coords(45, 180)]
        self.assertEqual(
            list(dm.join_on_k_closest(
                lambda: a,
                lambda: b,
                1
            )),
            [
                (a[0], b[0]),
            ]
        )

    def test_join_on_k_closest_2(self):
        a = [gt.Coords(0, 0), gt.Coords(0, gm.deg_to_rad(44))]
        b = [
                gt.Coords(0, gm.deg_to_rad(70)),
                gt.Coords(0, gm.deg_to_rad(60)),
                gt.Coords(0, gm.deg_to_rad(50)),
                gt.Coords(0, gm.deg_to_rad(40)),
                gt.Coords(0, gm.deg_to_rad(30)),
                gt.Coords(0, gm.deg_to_rad(20)),
                gt.Coords(0, gm.deg_to_rad(10)),
        ]
        self.assertEqual(
            list(dm.join_on_k_closest(
                lambda: a,
                lambda: b,
                2
            )),
            [
                (a[0], b[5]),
                (a[0], b[6]),
                (a[1], b[2]),
                (a[1], b[3]),
            ]
        )
