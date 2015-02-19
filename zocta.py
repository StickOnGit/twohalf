from zshape import ZShape
from listmath import coords, minus, dot

class ZOcta(ZShape):
    def __init__(self, x, y, z, d):
        pts = coords([x, y, z], [
            [1,     0,      0],
            [0,     1,      0],
            [0,     0,      1],
            [-1,    0,      0],
            [0,     -1,     0],
            [0,     0,      -1]
        ], d)
        
        e = .000001
        lines = []
        for a in pts:
            for b in pts:
                vector = minus(a, b)
                if d - e <= (dot(vector, vector) / (d * 2)) <= d + e:
                    lines.append((a, b))
        super(ZOcta, self).__init__(pts)
        pt_groups = (
                (pts[0], pts[1], pts[2]),
                (pts[0], pts[1], pts[5]),
                (pts[3], pts[1], pts[2]),
                (pts[3], pts[1], pts[5]),
                (pts[0], pts[4], pts[2]),
                (pts[0], pts[4], pts[5]),
                (pts[3], pts[4], pts[2]),
                (pts[3], pts[4], pts[5])
            )
        
        for group in pt_groups:
            newlines = [(a, b) for a in group for b in group if
                        (a, b) in lines or (b, a) in lines]
            
            self.set_face(group, newlines)