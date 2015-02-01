from listmath import dot, sq_dist, minus, plus, cross, pt_cross

class HitDetector(object):
    def __init__(self):
        self.search = []
        self.simplex = []
        self.hit = False
    
    def hitcube_collide(self, shape1, shape2):
        #cube1 = shape1.hitcube
        #cube2 = shape2.hitcube
        #left, top, front = [a - b - c for a, b, c in zip(cube1, cube2, cube2[3:])]
        #width, height, depth = [p + q for p, q in zip(cube1[3:], cube2[3:])]
        #return (left < 0 < (left + width) and 
        #        top < 0 < (top + height) and
        #        front < 0 < (front + depth))
        return shape1.sq_rad + shape2.sq_rad > sq_dist(shape1.center, shape2.center)
        #rad_1 = max(shape1.pts, key=lambda p: self.sq_dist(shape1.center, p))
        #rad_2 = max(shape2.pts, key=lambda q: self.sq_dist(shape2.center, q))
        #return rad_1 + rad_2 > total_dist

    def get_support(self, shape1, shape2):
        """Gets a support point based on two points in
        the shapes that may be colliding.
        """
        opposite = [-x for x in self.search]
                    
        a = max(shape1.pts, key=lambda p: dot(minus(p, shape1.center), self.search))
        b = max(shape2.pts, key=lambda p: dot(minus(p, shape2.center), opposite))
                    
        return minus(a, b)
    
    @property    
    def ao(self):
        """This object constantly checks to ensure that things
        have a positive dot product with the line from simplex[-1] to
        the origin (0, 0, 0) so this keeps it consistent."""
        return [-x for x in self.simplex[-1]]
                    
    def same_direction(self, vector):
        """Checks to see if the dot product of the passed vector and
        the vector from simplex[-1] to the origin is positive."""
        return dot(vector, self.ao) > 0
        
    def same_side(self, a, b, c, d, pt):
        """Checks to see that a point is on the same side of a triangle
        as point d.
        Triangle is a, b, c (the first three arguments)
        d is the next-to-last argument and the test point is the 
        final argument.
        """
        norm = cross([a, b], [a, c])
        dot_of_d = dot(norm, d)
        dot_of_pt = dot(norm, pt)
        
        return self.get_sign(dot_of_d) == self.get_sign(dot_of_pt)
        
    def get_sign(self, value):
        """Get the sign of a value. Returns -1, 0, or 1."""
        return (x > 0) - (x < 0)
        
    def wrap_get(self, seq, i):
        """Gets the index of a list, but lets the value "wrap-around"
        the list without causing an IndexError. 
                    
        Returns list[index % len(list)].
        """
        return seq[i % len(seq)]
                   
    def check_line(self):
        """Determines which part of a 2-simplex is closest
        to the origin. Sets search direction in accordance.
        
        May reduce the simplex to a single point if self.simplex[-1]
        is the closest aspect.
        """
        ab = minus(self.simplex[0], self.simplex[1])
        if self.same_direction(ab):
            # set next search vector
            self.search = pt_cross(pt_cross(ab, self.ao), ab)
        else:
            # the closest aspect
            # is the last point in the simplex.
            # so the simplex is pt A
            # and the search direction is AO
            self.simplex.pop(0)
            self.search = self.ao
                
    def check_triangle(self):
        """Determines which part of a 3-simplex is closest
        to the origin. Sets search direction in accordance.

        May reduce the simplex to either a 2-simplex or a
        single point, depending on the results.
        """
        # note that at this point,
        # self.simplex is triangle
        # CBA, not ABC! we want to keep looking
        # towards line AO (simplex[-1] to origin)
        # so unroll the list accordingly
        c, b, a = self.simplex
                
        # these come up a lot here
        ab_vec = minus(b, a)
        ac_vec = minus(c, a)
        # get triangle normal
        abc_norm = pt_cross(ab_vec, ac_vec)
        # then get normal from the normal! this should
        # always point outward (away from triangle center)
        abc_x_ac = pt_cross(abc_norm, ac_vec)
        
        fall_thru = False        
        # if a line orthogonal from the triangle
        # AND line AC is the same as AO...
        if self.same_direction(abc_x_ac):
            # ...do another test because origin could
            # still be outside the triangle
            if self.same_direction(ac_vec):
                # simplex becomes line AC
                # search is the normal from AC x AO x AC
                self.simplex = [c, a]
                self.search = pt_cross(pt_cross(ac_vec, self.ao), ac_vec)
            else:
                fall_thru = True
        else:
            # otherwise check the other normal from the other side
            ab_x_abc = pt_cross(ab_vec, abc_norm)
            if not self.same_direction(ab_x_abc):
                # it's a NOT check because if ab_x_abc
                # dots positively to self.ao, it 
                # means that line AB is the closest, so
                # that becomes the new simplex.
                # otherwise, the triangle is the closest aspect
                # now we just need to find the right normal from
                # the triangle to search in
                if self.same_direction(abc_norm):
                    # just change the search, triangle is fine
                    self.search = abc_norm
                else:
                    # otherwise, flip the normal and the
                    # b & c points in the triangle!
                    self.simplex = [b, c, a]
                    self.search = [-x for x in abc_norm]
            else:
                fall_thru = True
        # if we're here it means that AB was closest
        # and so we pop simplex[0]
        if fall_thru:
            if self.same_direction(ab_vec):
                self.simplex = [b, a]
                self.search = pt_cross(pt_cross(ab_vec, self.ao), ab_vec)
            else:
                # must be that the triangle itself was pointed at the origin
                # and point A was closest, so pop again and set search to self.ao
                self.simplex = [a]
                self.search = self.ao
                
    def check_tetrahedron(self):
        """Determines whether the origin is enclosed within
        a 4-simplex.
        
        Changes self.hit to True if there's a hit.
        Otherwise, drops a point from the simplex and
        sets the search to its normal vector.
        """
        # we know triangle DCB is aligned correctly;
        # we need to check the other 3 normals for same_direction
        
        d, c, b, a = self.simplex
        triangles = [
            [c, b, a],
            [d, b, a],
            [d, c, a]
        ]
        
        # saving the order of points in the triangles so
        # we know which cross product order creates an
        # inward-facing normal when rolled out in reverse
        # order (c, b, a = triangle, not a, b, c = triangle)
        
        good_tris = []
        for tri in triangles:
            cc, bb, aa = tri
            ab_vec = minus(bb, aa)
            ac_vec = minus(cc, aa)
            
            # get the point to test the direction of the norm
            dd = [pt for pt in self.simplex if pt not in tri][0]
            norm = pt_cross(ab_vec, ac_vec)
            if dot(dd, norm) > 0:
                if self.same_direction(norm):
                    good_tris.append(tri)
            else:
                new_norm = [-x for x in norm]
                if self.same_direction(new_norm):
                    good_tris.append([bb, cc, aa])
        self.hit = len(good_tris) == 3
        if not self.hit:
            # i can admit, this is really just sort of flailing.
            # but it isn't entirely stupid; i'm just throwing out the oldest point
            # and starting over with a triangle and a new search direction.
            self.simplex.pop(0)
            c, b, a = self.simplex
            ab = minus(b, a)
            ac = minus(c, a)
            ab_x = pt_cross(ab, ac)
            if self.same_direction(ab_x):
                self.simplex = [c, b, a]
                self.search = ab_x
            else:
                self.simplex = [b, c, a]
                self.search = [-x for x in ab_x]
            
              
    def get_simplex(self):
        """Gets the length of the simplex array,
        sees which part is closest to origin [0, 0, 0].
        if origin is inside a tetrahedron, hit. return True.
        
        Otherwise, use the closest part and make that
        the new simplex, set search in that direction (
                new_piece --> origin
        )
        """
        new_len = len(self.simplex)
        if new_len == 2:
            self.check_line()        
        elif new_len == 3:
            self.check_triangle()
        elif new_len == 4:
            self.check_tetrahedron()

    def find_collision(self, shape1, shape2):
        self.hit = False
        self.search = minus(shape1.center, shape2.center)
        self.simplex = [self.get_support(shape1, shape2)]
        self.search = [-x for x in self.search]
        # keeps it from working on the same
        # two shapes ad infinitum 
        for _ in xrange(len(shape1.pts) * len(shape2.pts)):
            next_pt = self.get_support(shape1, shape2)
            # if the dot product of line ON (origin -> next_pt) 
            # and line OS (origin -> search) is positive, 
            # then we evolve the simplex and continue.
            #
            # if not, we cannot have a hit - return False. Loop over!
            if dot(next_pt, self.search) > 0:
                self.simplex.append(next_pt)
                # if the origin is enclosed
                # by the tetrahedron, self.hit flips to True
                self.get_simplex()
            else:
                return False
            if self.hit:
                return True


