"""A generator for neat things."""

def grange(start, end, steps):
    """Returns a generator which starts at one value, ends at the end value,
    only the third argument is 'number of steps' instead of 'step-by value'.
    Example:
    >>> this = grange(1, 10, 4)
    >>> that = list(this)
    >>> print that      # will print [1, 4.0, 7.0, 10]
    >>> len(that)       # len is 4; the steps argument was 4
    
    This does return the end value as the final step; while the in-betweens
    are subject to rounding errors in the event that it does not yield integers, 
    both the start and end values are yielded as precisely what was passed when
    calling the function.
    """
    inc = (end - start) / float(steps - 1)
    for i in xrange(steps - 1):
        yield start
        start += inc
    yield end
