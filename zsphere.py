from zshape import ZShape
from listmath import coords, plus, minus, dot, normalize_vector
from math import sqrt, pi
from random import randint

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
        
        #for group in pt_groups:
        #    lines = [(0, 1), (0, 2), (1, 2)]
        #    f_pts = [pts[x] for x in group]
        #    # f_pts = group
        #    f_lines = [(pts[a], pts[b]) for a, b in lines]
        #    self.set_face(f_pts, f_lines)
        refined_group = []
        for abc in pt_groups:
            tiny_group = []
            a, b, c = [self.pts[i] for i in abc]
            # radius = minus(a, self.center)
            aa = [x / 2 for x in plus(a, b)]
            bb = [y / 2 for y in plus(b, c)]
            cc = [z / 2 for z in plus(c, a)]
            # these points will be too close; need to
            # push them out to lie on the sphere
            
            for pt in (aa, bb, cc):
                vec = normalize_vector(minus(pt, self.center))
                new_pt = coords(self.center, [vec], d)[0]
                if new_pt not in self.pts:
                    self.pts.append(new_pt)
                else:
                    new_pt = self.pts[self.pts.index(new_pt)]
                tiny_group.append(new_pt)
            
            refined_group.append(tiny_group)
                    # pt_cache.append(pt)
        
                    
        # print len(self.pts)
        for group in refined_group:
            lines = [(0, 1), (0, 2), (1, 2)]
            f_pts = group
            f_lines = [(pts[a], pts[b]) for a, b in lines]
            self.set_face(f_pts, f_lines)
        """
        #pts = []
        #for i in xrange(48):
        #    vec = [randint(-10, 10) for j in range(3)]
        #    n_vec = normalize_vector(vec)
        #    pts.append(coords([x, y, z], [n_vec], d)[0])
        #super(ZSphere, self).__init__(pts)
        #for pt in pts:
        #    others = [p for p in pts if p is not pt]
        #    closest = sorted(others, key=lambda x: dot(pt, x))[:3]
        #    lines = [(closest[a], closest[b]) for a, b in ((0, 1), (0, 2), (1, 2))]
        #    #print closest
        #    #print lines
        #    self.set_face(closest, lines)
        """