from math import *

# Using meters for all distances.

FEET_PER_METER = 3.28084

def m_to_ft(m):
    return m * FEET_PER_METER

def ft_to_m(ft):
    return ft / FEET_PER_METER

def rad_to_deg(r):
    return 180. * r/pi

def deg_to_rad(d):
    return d/180. * pi

def gc_dist_rad(
    p1, l1, p2, l2,
    sinp1 = None,
    cosp1 = None,
    sinp2 = None,
    cosp2 = None,
    sindl = None,
    cosdl = None,
):
    dl = abs(l1 - l2)

    if cosp1 is None: cosp1 = cos(p1)
    if cosp2 is None: cosp2 = cos(p2)
    if sindl is None: sindl = sin(dl)
    if cosdl is None: cosdl = cos(dl)
    if sinp1 is None: sinp1 = sin(p1)
    if sinp2 is None: sinp2 = sin(p2)

    nominator = (
          (cosp2 * sindl)**2
        + (cosp1 * sinp2 - sinp1 * cosp2 * cosdl)**2
    )
    denominator = sinp1 * sinp2 + cosp1 * cosp2 * cosdl
    return atan2(nominator**.5, denominator)

def gc_dist_deg(p1, l1, p2, l2):
    return gc_dist_rad(
       deg_to_rad(p1),
       deg_to_rad(l1),
       deg_to_rad(p2),
       deg_to_rad(l2)
    )

def gc_dist_coords_rad(c1, c2):
    return gc_dist_rad(c1.p, c1.l, c2.p, c2.l)

def gc_dist_coords_deg(c1, c2):
    return gc_dist_deg(c1.p, c1.l, c2.p, c2.l)
