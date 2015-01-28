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
        super(ZOcta, self).__init__(pts, lines)
