from math import pi, sin, cos
import unittest
from hexgrid import Cell, Grid


class TestCell(unittest.TestCase):
    def test_corners(self):
        for x, y, r in [(0, 0, 0), (0, 0, 1), (1, 1, 3), (-1, 1, 2), (0.5, 0.333, 35)]:
            c = Cell(x=x, y=y, radius=r)
            corners = tuple(c.corners())
            angles = (0, pi/3, 2*pi/3, pi, 4*pi/3, 5*pi/3)
            points = tuple((x + r * cos(t), y + r * sin(t)) for t in angles)
            self.assertSequenceEqual(corners, points)

    def test_equals(self):
        g1 = Cell(2, 1, 4)
        g2 = Cell(2, 1, 4)
        self.assertEqual(g1, g2)

        g3 = Cell(2, 1.5, 4)
        self.assertNotEqual(g1, g3)

class TestGrid(unittest.TestCase):
    def test_adjacent_coords(self):
        # Note that the returned coordinates from adjacent_coordinates are in (col, row) order
        g = Grid(2, 2)
        # coord adjacent to (0, 0)
        adj = [(1, 0), (0, 1)]
        self.assertSequenceEqual(adj, g.adjacent_coordinates(0, 0))

        # Coords adjacent to (1, 0)
        adj = [(0, 0), (0, 1), (1, 1)]
        self.assertSequenceEqual(adj, g.adjacent_coordinates(1, 0))

        # A 1x1 grid has no adjacent coordinates at (0, 0)
        g = Grid(1, 1)
        self.assertSequenceEqual([], g.adjacent_coordinates(0, 0))

        g = Grid(3, 3)
        # In counter clockwise order, starting at the lower right.
        adj = [(2, 2), (2, 1), (1, 0), (0, 1), (0, 2), (1, 2)]
        self.assertSequenceEqual(adj, g.adjacent_coordinates(1, 1))

    def test_adjacent_cells(self):
        g = Grid(3, 3)
        adj = [Cell(2, 2), Cell(2, 1), Cell(1, 0), Cell(0, 1), Cell(0, 2), Cell(1, 2)]
        cells = g.adjacent_cells(1, 1)
        self.assertSequenceEqual(adj, cells)

    def test_draw(self):
        g = Grid(1, 1)
        self.assertRaises(NotImplementedError, g.draw)
