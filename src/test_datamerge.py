import glob
import os
import unittest

import geomath as gm
import geotypes as gt
import datamerge as dm

BASE_DIR = os.path.dirname(__name__)
TEST_DATA_DIR = os.path.join(BASE_DIR, 'test_data')

class DataMergeTestCase(unittest.TestCase):
    
    def test_join_on_distance_threshold_1(self):
        a = [gt.Coords(0, 0)]
        b = [gt.Coords(0, 0)]
        self.assertEqual(
            list(dm.join_on_distance_threshold(
                a,
                b,
                1
            )),
            [(a[0], b[0])]
        )

    def test_join_on_distance_threshold_2(self):
        a = [gt.Coords(0, 0)]
        b = [gt.Coords(45, 0)]
        self.assertEqual(
            list(dm.join_on_distance_threshold(
                a,
                b,
                1
            )),
            []
        )

    def test_join_on_distance_threshold_3(self):
        a = [gt.Coords(0, 0), gt.Coords(0, 0)]
        b = [gt.Coords(45, 0)]
        self.assertEqual(
            list(dm.join_on_distance_threshold(
                a,
                b,
                1
            )),
            []
        )

    def test_join_on_distance_threshold_4(self):
        a = [gt.Coords(0, 0), gt.Coords(0, 0)]
        b = [gt.Coords(0, 0), gt.Coords(0, 0)]
        self.assertEqual(
            list(dm.join_on_distance_threshold(
                a,
                b,
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
                a,
                b,
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
                a,
                b,
                2
            )),
            [
                (a[0], b[5]),
                (a[0], b[6]),
                (a[1], b[2]),
                (a[1], b[3]),
            ]
        )

    def test_path_to_coords_iterator(self):
        paths = glob.glob(os.path.join(TEST_DATA_DIR, 'success*.csv'))
        for path in paths:
            for c in dm.path_to_coords_iterator(path):
                pass

    def test_join_files_by_threshold(self):
        rows = list(
            dm.join_files(
                os.path.join(TEST_DATA_DIR, 'success1.csv'),
                os.path.join(TEST_DATA_DIR, 'success1.csv'),
                threshold = 0
            )
        )
        for row in rows:
            self.assertEqual(row['1_Latitude'], row['2_Latitude'])
            self.assertEqual(row['1_Longitude'], row['2_Longitude'])

    def test_join_files_by_k_closest(self):
        path = os.path.join(TEST_DATA_DIR, 'success1.csv')
        rows = list(dm.path_to_coords_iterator(path))
        for k_closest in xrange(1, len(rows) + 1):
            joint_rows = list(dm.join_files(path, path, k_closest = k_closest))
            if k_closest == 1:
                for rowi, row in enumerate(joint_rows, 1):
                    self.assertEqual(row['1_Latitude'], row['2_Latitude'])
                    self.assertEqual(row['1_Longitude'], row['2_Longitude'])
            self.assertEqual(len(joint_rows), len(rows) * k_closest)
