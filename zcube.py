from zshape import ZShape
from listmath import minus, dot, coords

class ZCube(ZShape):
    def __init__(self, x, y, z, d):
        pts = coords([x, y, z], [
                [-1,    -1,     -1],
                [-1,    1,      -1],
                [1,     -1,     -1],
                [1,     1,      -1],
                [-1,    -1,      1],
                [-1,    1,      1],
                [1,    -1,      1],
                [1,    1,      1],
        ], d / 2.0)
        newlines = []
        for a in pts:
            for b in pts:
                vector = minus(a, b)
                if dot(vector, vector) == d**2:
                    newlines.append((a, b))
        super(ZCube, self).__init__(pts, [])
        pt_groups = (
                (pts[0], pts[1], pts[2], pts[3]),
                (pts[4], pts[5], pts[6], pts[7]),
                (pts[0], pts[1], pts[4], pts[5]),
                (pts[2], pts[3], pts[6], pts[7]),
                (pts[0], pts[2], pts[4], pts[6]),
                (pts[1], pts[3], pts[5], pts[7])                
            )
        for group in pt_groups:
            lines = [(a, b) for a in group for b in group if 
                    (a, b) in newlines or (b, a) in newlines]
            self.set_face(group, lines)