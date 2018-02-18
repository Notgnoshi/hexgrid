import unittest
from hexgrid import  Grid


class TestGrid(unittest.TestCase):
    def test_init(self):
        # Make sure we can construct all of the different options.
        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset')
        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset-odd-rows')
        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset-even-rows')
        g = Grid(hexagon_type='pointy-topped', coordinate_system='cube')
        g = Grid(hexagon_type='pointy-topped', coordinate_system='axial')
        g = Grid(hexagon_type='flat-topped', coordinate_system='offset')
        g = Grid(hexagon_type='flat-topped', coordinate_system='offset-odd-columns')
        g = Grid(hexagon_type='flat-topped', coordinate_system='offset-even-columns')
        g = Grid(hexagon_type='flat-topped', coordinate_system='cube')
        g = Grid(hexagon_type='flat-topped', coordinate_system='axial')

        # Make sure we can't do invalid things
        self.assertRaises(ValueError, Grid, 'invalid', 'offset')
        self.assertRaises(ValueError, Grid, 'flat-topped', 'invalid')

        # Make sure we can't do incompatible things.
        self.assertRaises(ValueError, Grid, 'pointy-topped', 'offset-odd-columns')
        self.assertRaises(ValueError, Grid, 'pointy-topped', 'offset-even-columns')
        self.assertRaises(ValueError, Grid, 'flat-topped', 'offset-odd-rows')
        self.assertRaises(ValueError, Grid, 'flat-topped', 'offset-even-rows')

        # Make sure using the 'offset' conveniency option gets handled right.
        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset')
        self.assertEqual(g.coordinate_system, 'offset-odd-rows')
        g = Grid(hexagon_type='flat-topped', coordinate_system='offset')
        self.assertEqual(g.coordinate_system, 'offset-odd-columns')

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
            out = Grid.convert(c, 'offset-odd-rows', 'offset-even-rows')
            self.assertSequenceEqual(out, e)

        coords = [(0, 0), (0, 1), (0, 2), (-1, 2), (3, -4)]
        expected = [(0, 0), (0, 1), (-1, 1), (-2, 1), (5, -2)]
        for c, e in zip(coords, expected):
            out = Grid.convert(c, 'offset-odd-rows', 'offset-odd-columns')
            self.assertSequenceEqual(out, e)

        coords = [(0, 0), (0, 1), (0, 2), (-1, 2), (3, -4)]
        expected = [(0, 0), (0, 1), (-1, 2), (-2, 1), (5, -1)]
        for c, e in zip(coords, expected):
            out = Grid.convert(c, 'offset-odd-rows', 'offset-even-columns')
            self.assertSequenceEqual(out, e)

    def test_valid_coordinates(self):
        g = Grid()
        self.assertRaises(NotImplementedError, g._assert_valid_coordinates, 1)
        self.assertRaises(NotImplementedError, g._assert_valid_coordinates, 0)
        self.assertRaises(ValueError, g._assert_valid_coordinates, None)
        self.assertRaises(NotImplementedError, g._assert_valid_coordinates, True)
        self.assertRaises(NotImplementedError, g._assert_valid_coordinates, False)
        self.assertRaises(ValueError, g._assert_valid_coordinates, (0,))
        g._assert_valid_coordinates((0, 0))
        self.assertRaises(ValueError, g._assert_valid_coordinates, (0, 0, 0))
        self.assertRaises(ValueError, g._assert_valid_coordinates, ('1', 'b'))
        self.assertRaises(ValueError, g._assert_valid_coordinates, ('a', 'b', 'c'))
        self.assertRaises(ValueError, g._assert_valid_coordinates, 'invalid')

        g = Grid(coordinate_system='cube')
        self.assertRaises(ValueError, g._assert_valid_coordinates, (0,))
        self.assertRaises(ValueError, g._assert_valid_coordinates, (0, 0))
        g._assert_valid_coordinates((0, 0, 0))
        self.assertRaises(ValueError, g._assert_valid_coordinates, ('1', 'b'))
        self.assertRaises(ValueError, g._assert_valid_coordinates, ('a', 'b', 'c'))

    def test_insert_remove(self):
        g = Grid()
        g[0, 0] = True
        g[1, 1] = False
        self.assertTrue((0, 0) in g)
        self.assertTrue((1, 1) in g)
        self.assertEqual(len(g), 2)
        self.assertEqual(g[0, 0], True)
        self.assertEqual(g[1, 1], False)
        del g[0, 0]
        self.assertFalse((0, 0) in g)
        self.assertEqual(len(g), 1)
        del g[1, 1]
        self.assertFalse((1, 1) in g)
        self.assertEqual(len(g), 0)

    def test_neighbor_coordinates(self):
        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset-odd-rows')
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 1), (2, 0), (1, 0), (0, 1), (1, 2), (2, 2)]
        self.assertSequenceEqual(n, expected)

        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset-even-rows')
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 1), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2)]
        self.assertSequenceEqual(n, expected)

        g = Grid(hexagon_type='flat-topped', coordinate_system='offset-odd-columns')
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 2), (2, 1), (1, 0), (0, 1), (0, 2), (1, 2)]
        self.assertSequenceEqual(n, expected)

        g = Grid(hexagon_type='flat-topped', coordinate_system='offset-even-columns')
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (1, 2)]
        self.assertSequenceEqual(n, expected)

        g = Grid(hexagon_type='pointy-topped', coordinate_system='axial')
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 1), (2, 0), (1, 0), (0, 1), (0, 2), (1, 2)]
        self.assertSequenceEqual(n, expected)

        # Flat topped vs pointy topped in axial coordinates just rotates the grid
        g = Grid(hexagon_type='flat-topped', coordinate_system='axial')
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 1), (2, 0), (1, 0), (0, 1), (0, 2), (1, 2)]
        self.assertSequenceEqual(n, expected)

        g = Grid(hexagon_type='pointy-topped', coordinate_system='cube')
        n = g.neighbor_coordinates((2, 0, -2), validate=False)
        expected = [(3, -1, -2), (3, 0, -3), (2, 1, -3), (1, 1, -2), (1, 0, -1), (2, -1, -1)]
        self.assertSequenceEqual(n, expected)

        # Flat topped vs pointy topped in cubic coordinates just rotates the grid
        g = Grid(hexagon_type='flat-topped', coordinate_system='cube')
        n = g.neighbor_coordinates((2, 0, -2), validate=False)
        expected = [(3, -1, -2), (3, 0, -3), (2, 1, -3), (1, 1, -2), (1, 0, -1), (2, -1, -1)]
        self.assertSequenceEqual(n, expected)

    def test_neighbors(self):
        g = Grid(hexagon_type='pointy-topped', coordinate_system='offset-odd-rows')
        g[1, 1] = 'center'
        g[1, 0] = 'adjacent 1'
        g[2, 0] = 'adjacent 2'
        g[3, 3] = 'not adjacent'

        n = g.neighbors((1, 1))
        self.assertSequenceEqual(n, ['adjacent 2', 'adjacent 1'])

        g = Grid(hexagon_type='pointy-topped', coordinate_system='cube')
        g[0, 0, 0] = 'center'
        g[1, 0, -1] = 'adjacent 1'
        g[-1, 0, 1] = 'adjacent 2'
        g[0, 2, -2] = 'not adjacent'
        n = g.neighbors((0, 0, 0))
        self.assertSequenceEqual(n, ['adjacent 1', 'adjacent 2'])

        g = Grid()
        g[0, 0] = 'center'
        self.assertEqual([], g.neighbors((0, 0)))

    def test_set_coordinate(self):
        g = Grid()
        g[0, 0] = None
        g.set_coordinate_system('cube')
        coord = tuple(g.keys())[0]
        self.assertSequenceEqual(coord, (0, 0, 0))
