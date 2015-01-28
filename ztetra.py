from zshape import ZShape
from listmath import coords, minus, dot
from math import sqrt, pi

class ZTetra(ZShape):
    def __init__(self, x, y, z, d, right=True):
        pts = coords([x, y, z], [
                [0,     sqrt(3) - (1.0/sqrt(3)),  0], 
                [-1,    -1.0 / sqrt(3),                0],
                [1,     -1.0 / sqrt(3),                0],
                [0,     0,              2.0 * sqrt(2/3.0)]
            ], d)
        e = .000001
        lines = []
        for a in pts:
            for b in pts:
                vector = minus(a, b)
                if d - e <= (dot(vector, vector) / (d * 4)) <= d + e:
                    lines.append((a, b))
        super(ZTetra, self).__init__(pts, lines)
        if right:
            self.rotate(-(2*pi)/4, "x")
