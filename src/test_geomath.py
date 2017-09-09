from math import pi
import random
import unittest

import geomath as gm
import geotypes as gt

MODICUM = 1e-3

class MathTestCase(unittest.TestCase):

    def test_rad_to_deg(self):
        self.assertEqual(gm.rad_to_deg(0), 0)
        self.assertEqual(gm.rad_to_deg(pi), 180)
        self.assertEqual(gm.rad_to_deg(-pi), -180)
        self.assertEqual(gm.rad_to_deg(pi/2), 90)
        self.assertEqual(gm.rad_to_deg(-pi/2), -90)

    def test_deg_to_rad(self):
        self.assertEqual(gm.deg_to_rad(0), 0)
        self.assertEqual(gm.deg_to_rad(180), pi)
        self.assertEqual(gm.deg_to_rad(-180), -pi)
        self.assertEqual(gm.deg_to_rad(90), pi/2)
        self.assertEqual(gm.deg_to_rad(-90), -pi/2)

    def test_gc_dist_deg(self):
        for di in xrange(-360, 360, 5):
            self.assertLess(gm.gc_dist_deg(di, di, di, di), MODICUM)
            self.assertLess(
                abs(gm.gc_dist_deg(di, di, -di, di+180) - gm.MID_R*pi),
                MODICUM
            )
            self.assertLess(
                gm.gc_dist_deg(
                    360+di,
                    -360+di,
                    -360+di,
                    360+di
                ),
                MODICUM
            )
    
    def test_gc_dist_coords(self):
        random.seed('test_gc_dist_coords')
        for di in xrange(-360, 360, 1):
            c1 = gt.Coords(
                gm.deg_to_rad(di),
                gm.deg_to_rad(di) + random.random()*2*pi
            )
            c2 = gt.Coords(
                gm.deg_to_rad(di) + random.random()*2*pi,
                gm.deg_to_rad(di) + random.random()*2*pi
            )
            self.assertEqual(
                gm.gc_dist_coords(c1, c2),
                gm.gc_dist_rad(c1.p, c1.l, c2.p, c2.l)
            )
            self.assertLess(
                abs(gm.gc_dist_coords(c1, c2) - gm.gc_dist_coords(c2, c1)),
                MODICUM
            )

 
    def test_gc_dist_coords_incremental(self):
        cs = [
            gt.Coords(0, 0),
            gt.Coords(0, pi/10),
            gt.Coords(0, pi/9),
            gt.Coords(0, pi/8),
            gt.Coords(0, pi/7),
            gt.Coords(0, pi/6),
            gt.Coords(0, pi/5),
            gt.Coords(0, pi/4),
            gt.Coords(0, pi/3),
            gt.Coords(0, pi/2),
            gt.Coords(0, pi/1),
        ]
        c1 = cs[0]
        sor = sorted(cs, key = lambda c2: gm.gc_dist_coords(c1, c2))
        self.assertEqual(cs, sor)

