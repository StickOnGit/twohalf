from zshape import ZShape
from grange import grange
from math import sqrt

class ZLine(ZShape):
    """It's a line!
    
    It's cool because it generates a series of line segments
    between the pts you specify, so it will gradually fade away as
    it reaches towards the horizon.
    """
    def __init__(self, pts):
        allpts = list(self.set_initial_pts(*pts))
        lines = []
        for i in range(len(allpts) - 1):
            lines.append((allpts[i], allpts[i+1]))
        super(ZLine, self).__init__(allpts, lines)
    
    def set_initial_pts(self, pt1, pt2):
        steps = int(sqrt(sum(abs(b-a)**2 for a, b in zip(pt1, pt2))) / 20)
        xs, ys, zs = [grange(pt1[j], pt2[j], steps) for j in range(3)]
        for i in xrange(steps):
            yield map(next, (xs, ys, zs))
