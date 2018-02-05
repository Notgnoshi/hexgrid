from .cell import Cell
class Grid(object):
    """
        Implements a Grid of flat-topped hexagonal Cells, using
        the so-called "odd-q" vertical layout discussed at
        https://www.redblobgames.com/grids/hexagons/
    """
    def __init__(self, height, width):
        """
            Constructs a height-by-width grid of hexagonal tiles, indexed by the "odd-q" method.
        """
        self.height = height
        self.width = width
        self.cells = list()
        for i in range(height):
            row = list()
            for j in range(width):
                # Use x for the column, and y for the row.
                row.append(Cell(x=j, y=i))
            self.cells.append(row)

    def __repr__(self):
        return f'<Grid {self.height}, {self.width}'

    def _coords_valid(self, col, row):
        """
            Indicates whether the given coordinates are valid.

            Example:
            >>> g = Grid(2, 2)
            >>> g._coords_valid(0, 1)
            True
            >>> g._coords_valid(2, 0)
            False
        """
        if row < 0 or col < 0:
            return False
        elif row > (self.height - 1) or col > (self.width - 1):
            return False
        return True

    def adjacent_coordinates(self, col, row):
        """
            Returns a list of valid adjacent coordinates to the
            provided cell coordinates in (col, row) order.
        """
        # Directions of adjacent coordinates. Specific to the "odd-q" grid representation
        oddq_directions = [
            # Even column directions (col, row)
            [(1, 0), (1, -1), (0, -1),
             (-1, -1), (-1, 0), (0, 1)],
            # Odd column directions (col, row)
            [(1, 1), (1, 0), (0, -1),
             (-1, 0), (-1, 1), (0, 1)]
        ]
        adjacents = []
        for dc, dr in oddq_directions[col % 2]:
            adj_c = col + dc
            adj_r = row + dr
            if self._coords_valid(adj_c, adj_r):
                adjacents.append((adj_c, adj_r))
        return adjacents

    def adjacent_cells(self, col, row):
        """
            Returns a list of the adjacent cells.
        """
        return [self.cells[r][c] for c, r in self.adjacent_coordinates(col, row)]

    def draw(self):
        raise NotImplementedError('Drawing not yet implemented.')
