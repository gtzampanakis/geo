from math import *

# Using meters for all distances.

MID_R = 6371 * 1000.

FEET_PER_METER = 3.28084

def m_to_ft(m):
    return m * FEET_PER_METER

def ft_to_m(ft):
    return ft / FEET_PER_METER

def rad_to_deg(r):
    return 180. * r/pi

def deg_to_rad(d):
    return d/180. * pi

def gc_dist_rad(p1, l1, p2, l2, r=None):
    if r is None:
        r = MID_R
    dl = abs(l1 - l2)

    cosp1 = cos(p1)
    cosp2 = cos(p2)
    sindl = sin(dl)
    cosdl = cos(dl)
    sinp1 = sin(p1)
    sinp2 = sin(p2)

    nominator = (
          (cosp2 * sindl)**2
        + (cosp1 * sinp2 - sinp1 * cosp2 * cosdl)**2
    )
    denominator = sinp1 * sinp2 + cosp1 * cosp2 * cosdl
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
