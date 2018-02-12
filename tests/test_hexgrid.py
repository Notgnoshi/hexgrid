import unittest
from hexgrid import  Grid


class TestGrid(unittest.TestCase):
    def test_init(self):
        # Make sure we can construct all of the different options.
        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset')
        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset-odd-row')
        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset-even-row')
        g = Grid(hexagon_type='pointy-topped', coordinate_system='cube')
        g = Grid(hexagon_type='pointy-topped', coordinate_system='axial')
        g = Grid(hexagon_type='flat-topped', coordinate_system='offset')
        g = Grid(hexagon_type='flat-topped', coordinate_system='offset-odd-column')
        g = Grid(hexagon_type='flat-topped', coordinate_system='offset-even-column')
        g = Grid(hexagon_type='flat-topped', coordinate_system='cube')
        g = Grid(hexagon_type='flat-topped', coordinate_system='axial')

        # Make sure we can't do invalid things
        self.assertRaises(ValueError, Grid, 'invalid', 'offset')
        self.assertRaises(ValueError, Grid, 'flat-topped', 'invalid')

        # Make sure we can't do incompatible things.
        self.assertRaises(ValueError, Grid, 'pointy-topped', 'offset-odd-column')
        self.assertRaises(ValueError, Grid, 'pointy-topped', 'offset-even-column')
        self.assertRaises(ValueError, Grid, 'flat-topped', 'offset-odd-row')
        self.assertRaises(ValueError, Grid, 'flat-topped', 'offset-even-row')

        # Make sure using the 'offset' conveniency option gets handled right.
        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset')
        self.assertEqual(g.coordinate_system, 'offset-odd-row')
        g = Grid(hexagon_type='flat-topped', coordinate_system='offset')
        self.assertEqual(g.coordinate_system, 'offset-odd-column')

    def test_conversion_invertible(self):
        c = (2, -6, 4)
        out = Grid.convert(c, 'cube', 'axial')
        self.assertSequenceEqual(out, (2, 4))
        self.assertSequenceEqual(c, Grid.convert(out, 'axial', 'cube'))

        # Make sure conversions are invertible.
        coords = [(0, 0), (1, 1), (2, 3), (-2, 2), (2, 15), (20, 2), (2, -2), (-13.5, 2372.2)]
        for c in coords:
            for from_sys in Grid.COORDINATE_SYSTEM_OPTIONS[1:-1]:
                for to_sys in Grid.COORDINATE_SYSTEM_OPTIONS[1:-1]:
                    out = Grid.convert(c, from_sys, to_sys)
                    self.assertSequenceEqual(c, Grid.convert(out, to_sys, from_sys))

        # Recall that cubic coordinates must sum to 0...
        coords = [(0, 0, 0), (1, -2, 1), (1, 2, -3), (10.5, -10.5, 0)]
        for c in coords:
            for to_sys in Grid.COORDINATE_SYSTEM_OPTIONS[1:-1]:
                out = Grid.convert(c, 'cube', to_sys)
                self.assertSequenceEqual(c, Grid.convert(out, to_sys, 'cube'))

        # Make sure cubic coordinates pass through completely unchanged.
        for c in coords:
            out = Grid.convert(c, 'cube', 'cube')
            self.assertSequenceEqual(c, out)

    def test_offset_conversion(self):
        coords = [(0, 0), (0, 1), (0, 2), (-1, 2), (3, -4)]
        expected = [(0, 0), (1, 1), (0, 2), (-1, 2), (3, -4)]
        for c, e in zip(coords, expected):
            out = Grid.convert(c, 'offset-odd-row', 'offset-even-row')
            self.assertSequenceEqual(out, e)

        coords = [(0, 0), (0, 1), (0, 2), (-1, 2), (3, -4)]
        expected = [(0, 0), (0, 1), (-1, 1), (-2, 1), (5, -2)]
        for c, e in zip(coords, expected):
            out = Grid.convert(c, 'offset-odd-row', 'offset-odd-column')
            self.assertSequenceEqual(out, e)

        coords = [(0, 0), (0, 1), (0, 2), (-1, 2), (3, -4)]
        expected = [(0, 0), (0, 1), (-1, 2), (-2, 1), (5, -1)]
        for c, e in zip(coords, expected):
            out = Grid.convert(c, 'offset-odd-row', 'offset-even-column')
            self.assertSequenceEqual(out, e)
