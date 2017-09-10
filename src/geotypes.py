import collections

class Coords:
    def __init__(self, p, l, data=None):
        self.p = p
        self.l = l
        self.data = data

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Coords(p = %s, l = %s)' % (self.p, self.l)
