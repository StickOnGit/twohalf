from listmath import cross, dot, minus

class Face(object):
    def __init__(self, pts, lines, wrong_way):
        self.pts = []
        self.lines = []
        self.color = [120, 120, 120]
        self.center = None
        #self.direction = [0, 0, 0]
        #self.zmove = 0
        for pt in pts:
            self.pts.append(pt)
        self.order = self.pts[:3]
        for line in lines:
            self.set_line(*line)
        self.set_center()
        self.set_norm(wrong_way)
        
    def set_line(self, a, b):
        """Establishes which lines between points should be visible.
        Checks to ensure that the points are in obj.pts and neither
        the line or the inverse of the line are already in obj.lines.
        Does nothing if the above conditions are not satisfied.
        """
        if a in self.pts and b in self.pts:
            if (a, b) not in self.lines and (b, a) not in self.lines:
                self.lines.append((a, b))
    
    def set_center(self):
        """Finds the center by averaging the points in obj.pts."""
        self.center = [
                sum([p[i] for p in self.pts])/float(len(self.pts)) 
                for i in range(3)
            ]
            
    def get_norm(self):
        return cross(self.order[:2], self.order[1:])
            
    def set_norm(self, wrong_way):
        """Determines the correct order for calculating the surface
        normal. Ideally all points in this surface are coplanar so
        just three points are enough. The 'wrong way' point is needed
        to set the direction (line self.center -> wrong_way) 
        we do NOT want the normal to point.
        """
        wrong_vector = minus(wrong_way, self.center)
        if not dot(wrong_vector, self.get_norm()) < 0:
            self.order.append(self.order.pop(1))