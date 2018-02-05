import math


class Cell(object):
    """
        Implements a flat-topped hexagonal cell.
    """
    def __init__(self, x=0, y=0, radius=1):
        self.x = x
        self.y = y
        self.radius = radius

    def corners(self):
        """
            Returns an iterable of the corner vertices of the hexagonal cell.
        """
        for i in range(6):
            theta = i * math.pi / 3
            yield (self.x + self.radius * math.cos(theta),
                   self.y + self.radius * math.sin(theta))

    def __repr__(self):
        return f'<Cell {self.x}, {self.y}>'

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.__dict__ == other.__dict__
        return False
