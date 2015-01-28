"""Little library for throwing Python lists around as if
they were 3D points.

Note that this library doesn't necessarily borrow against itself;
if an operation would use plus(point_a, point_b) it will instead
use Python's bare list comprehension - 

    [p + q for p, q in zip(point_a, point_b)] 
    
- wherever it makes sense.
"""

def plus(x, y):
    """Adds the contents of two lists."""
    return [(a + b) for a, b in zip(x, y)]
    
def minus(x, y):
    """Subtracts the contents of two lists."""
    return [(a - b) for a, b in zip(x, y)]
    
def times(x, y):
    """Multiplies the contents of two lists."""
    return [(a * b) for a, b in zip(x, y)]
    
def dot(x, y):
    """Returns the dot product of two lists."""
    return sum([a * b for a, b in zip(x, y)])
    
def sq_dist(a, b):
    """Returns the squared distance between two points.
    Uses the dot product of the vector and itself."""
    ab = [b - a for a, b in zip(a, b)]
    return sum(abs(c * c) for c in ab)
    
def coords(xyz, matrix, d):
    """Matrix-math-but-not. 
    
    Used primarily to get a set of points when creating a new shape.
    
    First multiplies the values in matrix by d, then adds those values
    to the passed point. Returns the new set of points.
    """
    # so the 'long form' of this would be more or less as follows:
    #   d_list = [d, d, d]
    #   real_matrix = [
    #       times(abc, d_list) for abc in matrix
    #   ]
    #   return [
    #       plus(xyz, j) for j in real_matrix
    #   ]
    # 
    # however, the nested list comprehension above avoids all those
    # assignments, which appears to be better for performance.
    return [
            [a + b for a, b in zip(xyz, j)] for j in 
            [[d * n for n in abc] for abc in matrix]
        ]
        
def old_coords(xyz, matrix, d):
    """This only exists for test purposes."""
    d_list = [d, d, d]
    real_matrix = [[d * n for n in abc] for abc in matrix]
    return [[a + b for a, b in zip(xyz, j)] for j in real_matrix]
    #
    #return new_set
     
    
def cross(line1, line2):
    """Gets the cross product of two lists of lists.
    This is ideal when it's simpler to pass two lines
    instead of two vectors/points.
    """
    u = [b - a for a, b in zip(*line1)]
    v = [b - a for a, b in zip(*line2)]
    
    return [
        (u[1] * v[2]) - (u[2] * v[1]),
        (u[2] * v[0]) - (u[0] * v[2]),
        (u[0] * v[1]) - (u[1] * v[0]),
    ]
    
def pt_cross(u, v):
    """Returns the cross product of two lists.
    Use this when you would cross two vectors that
    have already been calculated.
    """
    
    return [
        (u[1] * v[2]) - (u[2] * v[1]),
        (u[2] * v[0]) - (u[0] * v[2]),
        (u[0] * v[1]) - (u[1] * v[0]),
    ]
    
