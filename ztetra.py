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
        super(ZTetra, self).__init__(pts, [])
        if right:
            self.rotate(-(2*pi)/4, "x")
        pt_group = (
                (pts[0], pts[1], pts[2]),
                (pts[0], pts[2], pts[3]),
                (pts[0], pts[1], pts[3]),
                (pts[1], pts[2], pts[3])                
            )
        for group in pt_group:
            line_group = (
                    (group[0], group[1]),
                    (group[1], group[2]),
                    (group[0], group[2])
                )
            self.set_face(group, line_group)
