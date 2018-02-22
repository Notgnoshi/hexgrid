def tuple_add(t1, t2):
    """
        Adds two tuples componentwise

        Example
        >>> t1 = (1, 2, 3)
        >>> t2 = (4, 5, 6)
        >>> tuple_add(t1, t2)
        (5, 7, 9)
    """
    return tuple(r + s for r, s in zip(t1, t2))

def tuple_multiply(t, k):
    """
        Multiplies the tuple `t` by the scalar `k`

        Example
        >>> t = (1, 2, 3)
        >>> tuple_multiply(t, -1)
        (-1, -2, -3)
    """
    return tuple(k * t_i for t_i in t)
