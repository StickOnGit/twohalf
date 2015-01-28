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
        super(ZCube, self).__init__(pts, newlines)
