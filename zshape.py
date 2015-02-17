from math import hypot, atan2, cos, sin
from listmath import dot, sq_dist
from face import Face

class ZShape(object):
    """The base class for 3D objects."""
    def __init__(self, pts, lines):
        self.pts = pts
        self.lines = []
        self.faces = []
        self.color = [120, 120, 120]
        self.center = None
        self.direction = [0, 0, 0]
        self.zmove = 0
        #for pt in pts:
        #    self.pts.append(pt)
        #for line in lines:
        #    self.set_line(*line)
        self.set_center()
        self.set_sq_rad()
        
    @property
    def hitcube(self):
        """Returns a list that represents a cube surrounding the entire object.
        Values are [min_x, min_y, min_z, width, height, depth].
        """
        xyz = [min(pt[i] for pt in self.pts) for i in range(3)]
        # second list is width height depth
        return xyz + [max(pt[j] for pt in self.pts) - xyz[j] for j in range(3)]
        
    def set_sq_rad(self):
        """Set the squared radius as the double-dot product of the longest
        line from the center to the furthest of the object's points."""
        #def mag(a, b):
        #    ab = [b - a for a, b in zip(a, b)]
        #    return dot(ab, ab)
        
        rads = [sq_dist(self.center, x) for x in self.pts]
        self.sq_rad = max(rads)
        
    def set_face(self, pts, lines):
        self.faces.append(Face(pts, lines, self.center))
            
        
    def set_line(self, a, b):
        """Establishes which lines between points should be visible.
        Checks to ensure that the points are in obj.pts and neither
        the line or the inverse of the line are already in obj.lines.
        Does nothing if the above conditions are not satisfied.
        """
        if a in self.pts and b in self.pts:
            if (a, b) not in self.lines and (b, a) not in self.lines:
                self.lines.append((a, b))
    
    def set_center(self, new_center=None):
        """Finds the center by averaging the points in obj.pts.
        Can also be passed a center argument.
        """
        if new_center is not None:
            self.center = new_center
        else:
            self.center = [
                    sum([p[i] for p in self.pts])/float(len(self.pts)) 
                    for i in range(3)
                ]
    
    def move_to_center(self, new_center):
        """Moves the shape by setting a new center and then translating all points
        around the delta."""
        delta = [b - a if b is not None else 0 for a, b in zip(self.center, new_center)]
        for pt in self.pts + [self.center]:
            for i, x in enumerate(pt):
                pt[i] += delta[i]
    
    def move(self):
        """Movement based on the direction vector.
        Passes if obj.direction == [0, 0, 0]."""
        if not self.direction == [0, 0, 0]:
            for pt in self.pts + [self.center]:
                for i, x in enumerate(pt):
                    pt[i] += self.direction[i]
    
    def rotate(self, radians, axis):
        """Rotates the shape around the x, y, or z axis."""
        if axis == "x":
            i, j = 1, 2
        elif axis == "y":
            i, j = 2, 0
        elif axis == "z":
            i, j = 1, 0
        for pt in self.pts:
            v1, v2 = pt[i] - self.center[i], pt[j] - self.center[j]
            d = hypot(v1, v2)
            theta = atan2(v1, v2) + radians
            pt[j] = self.center[j] + d * cos(theta)
            pt[i] = self.center[i] + d * sin(theta)
        self.set_center()
    
    def update(self):
        """Oh, placeholder. :P"""
        pass
