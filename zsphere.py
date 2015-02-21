from zshape import ZShape
from listmath import coords, minus, dot
from math import sqrt, pi

class ZSphere(ZShape):
    def __init__(self, x, y, z, d):
        t = (1 + sqrt(5)) / 2.0
        pts = coords([x, y, z], [
            (-1, t, 0),
            (1, t, 0),
            (-1, -t, 0),
            (1, -t, 0),
            (0, -1, t),
            (0, 1, t),
            (0, -1, -t),
            (0, 1, -t),
            (t, 0, -1),
            (t, 0, 1),
            (-t, 0, -1),
            (-t, 0, 1)
        ], d)
        super(ZSphere, self).__init__(pts)
        pt_groups = [
                (0, 11, 5),
                (0, 5, 1),
                (0, 1, 7),
                (0, 7, 10),
                (0, 10, 11),
                (1, 5, 9),
                (5, 11, 4),
                (11, 10, 2),
                (10, 7, 6),
                (7, 1, 8),
                (3, 9, 4),
                (3, 4, 2),
                (3, 2, 6),
                (3, 6, 8),
                (3, 8, 9),
                (4, 9, 5),
                (2, 4, 11),
                (6, 2, 10),
                (8, 6, 7),
                (9, 8, 1)
            ]
        for group in pt_groups:
            lines = [(0, 1), (0, 2), (1, 2)]
            f_pts = [pts[x] for x in group]
            f_lines = [(pts[a], pts[b]) for a, b in lines]
            self.set_face(f_pts, f_lines)