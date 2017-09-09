from math import *

MID_R = 6371 * 1000.

def rad_to_deg(r):
    return 180. * r/pi

def deg_to_rad(d):
    return d/180. * pi

def gc_dist_rad(p1, l1, p2, l2, r=None):
    if r is None:
        r = MID_R
    dp = abs(p1 - p2)
    dl = abs(l1 - l2)
    nominator = (
          (cos(p2) * sin(dl))**2
        + (cos(p1) * sin(p2) - sin(p1) * cos(p2) * cos(dl))**2
    )
    denominator = (
        sin(p1) * sin(p2) + cos(p1) * cos(p2) * cos(dl)
    )
    return r * atan2(nominator**.5, denominator)

def gc_dist_deg(p1, l1, p2, l2, r=None):
    return gc_dist_rad(
       deg_to_rad(p1),
       deg_to_rad(l1),
       deg_to_rad(p2),
       deg_to_rad(l2),
       r
    )

def gc_dist_coords(c1, c2, r=None):
    return gc_dist_rad(c1.p, c1.l, c2.p, c2.l)
