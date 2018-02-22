import unittest
from hexgrid import Grid, CoordinateSystem, HexagonType
from hexgrid import FLAT, POINTY
from hexgrid import OFFSET, CUBIC, AXIAL
from hexgrid import OFFSET_EVEN_COLUMNS, OFFSET_ODD_COLUMNS, OFFSET_EVEN_ROWS, OFFSET_ODD_ROWS


class TestGrid(unittest.TestCase):
    def test_init(self):
        # Make sure we can construct all of the different options.
        g = Grid(hexagon_type=POINTY, coordinate_system=OFFSET)
        g = Grid(hexagon_type=POINTY, coordinate_system=OFFSET_ODD_ROWS)
        g = Grid(hexagon_type=POINTY, coordinate_system=OFFSET_EVEN_ROWS)
        g = Grid(hexagon_type=POINTY, coordinate_system=CUBIC)
        g = Grid(hexagon_type=POINTY, coordinate_system=AXIAL)
        g = Grid(hexagon_type=FLAT, coordinate_system=OFFSET)
        g = Grid(hexagon_type=FLAT, coordinate_system=OFFSET_ODD_COLUMNS)
        g = Grid(hexagon_type=FLAT, coordinate_system=OFFSET_EVEN_COLUMNS)
        g = Grid(hexagon_type=FLAT, coordinate_system=CUBIC)
        g = Grid(hexagon_type=FLAT, coordinate_system=AXIAL)

        # Make sure we can't do invalid things
        self.assertRaises(ValueError, Grid, 'invalid', OFFSET)
        self.assertRaises(ValueError, Grid, FLAT, 'invalid')

        # Make sure we can't do incompatible things.
        self.assertRaises(ValueError, Grid, POINTY, OFFSET_ODD_COLUMNS)
        self.assertRaises(ValueError, Grid, POINTY, OFFSET_EVEN_COLUMNS)
        self.assertRaises(ValueError, Grid, FLAT, OFFSET_ODD_ROWS)
        self.assertRaises(ValueError, Grid, FLAT, OFFSET_EVEN_ROWS)

        # Make sure using the 'offset' conveniency option gets handled right.
        g = Grid(hexagon_type=POINTY, coordinate_system=OFFSET)
        self.assertEqual(g.coordinate_system, OFFSET_ODD_ROWS)
        g = Grid(hexagon_type=FLAT, coordinate_system=OFFSET)
        self.assertEqual(g.coordinate_system, OFFSET_ODD_COLUMNS)

    def test_conversion_invertible(self):
        c = (2, -6, 4)
        out = Grid.convert(c, CUBIC, AXIAL)
        self.assertSequenceEqual(out, (2, 4))
        self.assertSequenceEqual(c, Grid.convert(out, AXIAL, CUBIC))

        # Make sure conversions are invertible.
        coords = [(0, 0), (1, 1), (2, 3), (-2, 2), (2, 15), (20, 2), (2, -2), (-13.5, 2372.2)]
        for c in coords:
            for from_sys in [AXIAL, OFFSET_EVEN_COLUMNS, OFFSET_ODD_COLUMNS, OFFSET_EVEN_ROWS, OFFSET_ODD_ROWS]:
                for to_sys in [AXIAL, OFFSET_EVEN_COLUMNS, OFFSET_ODD_COLUMNS, OFFSET_EVEN_ROWS, OFFSET_ODD_ROWS]:
                    out = Grid.convert(c, from_sys, to_sys)
                    self.assertSequenceEqual(c, Grid.convert(out, to_sys, from_sys))

        # Recall that cubic coordinates must sum to 0...
        coords = [(0, 0, 0), (1, -2, 1), (1, 2, -3), (10.5, -10.5, 0)]
        for c in coords:
            for to_sys in [CUBIC, AXIAL, OFFSET_EVEN_COLUMNS, OFFSET_ODD_COLUMNS, OFFSET_EVEN_ROWS, OFFSET_ODD_ROWS]:
                out = Grid.convert(c, CUBIC, to_sys)
                self.assertSequenceEqual(c, Grid.convert(out, to_sys, CUBIC))

        # Make sure cubic coordinates pass through completely unchanged.
        for c in coords:
            out = Grid.convert(c, CUBIC, CUBIC)
            self.assertSequenceEqual(c, out)

    def test_offset_conversion(self):
        coords = [(0, 0), (0, 1), (0, 2), (-1, 2), (3, -4)]
        expected = [(0, 0), (1, 1), (0, 2), (-1, 2), (3, -4)]
        for c, e in zip(coords, expected):
            out = Grid.convert(c, OFFSET_ODD_ROWS, OFFSET_EVEN_ROWS)
            self.assertSequenceEqual(out, e)

        coords = [(0, 0), (0, 1), (0, 2), (-1, 2), (3, -4)]
        expected = [(0, 0), (0, 1), (-1, 1), (-2, 1), (5, -2)]
        for c, e in zip(coords, expected):
            out = Grid.convert(c, OFFSET_ODD_ROWS, OFFSET_ODD_COLUMNS)
            self.assertSequenceEqual(out, e)

        coords = [(0, 0), (0, 1), (0, 2), (-1, 2), (3, -4)]
        expected = [(0, 0), (0, 1), (-1, 2), (-2, 1), (5, -1)]
        for c, e in zip(coords, expected):
            out = Grid.convert(c, OFFSET_ODD_ROWS, OFFSET_EVEN_COLUMNS)
            self.assertSequenceEqual(out, e)

    def test_valid_coordinates(self):
        g = Grid()
        self.assertRaises(ValueError, g._assert_valid_coordinates, 1)
        self.assertRaises(ValueError, g._assert_valid_coordinates, 0)
        self.assertRaises(ValueError, g._assert_valid_coordinates, None)
        self.assertRaises(ValueError, g._assert_valid_coordinates, True)
        self.assertRaises(ValueError, g._assert_valid_coordinates, False)
        self.assertRaises(ValueError, g._assert_valid_coordinates, (0,))
        g._assert_valid_coordinates((0, 0))
        self.assertRaises(ValueError, g._assert_valid_coordinates, (0, 0, 0))
        self.assertRaises(ValueError, g._assert_valid_coordinates, ('1', 'b'))
        self.assertRaises(ValueError, g._assert_valid_coordinates, ('a', 'b', 'c'))
        self.assertRaises(ValueError, g._assert_valid_coordinates, 'invalid')

        g = Grid(coordinate_system=CUBIC)
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
        g = Grid(hexagon_type=POINTY, coordinate_system=OFFSET_ODD_ROWS)
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 1), (2, 0), (1, 0), (0, 1), (1, 2), (2, 2)]
        self.assertSequenceEqual(n, expected)

        g = Grid(hexagon_type=POINTY, coordinate_system=OFFSET_EVEN_ROWS)
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 1), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2)]
        self.assertSequenceEqual(n, expected)

        g = Grid(hexagon_type=FLAT, coordinate_system=OFFSET_ODD_COLUMNS)
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 2), (2, 1), (1, 0), (0, 1), (0, 2), (1, 2)]
        self.assertSequenceEqual(n, expected)

        g = Grid(hexagon_type=FLAT, coordinate_system=OFFSET_EVEN_COLUMNS)
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (1, 2)]
        self.assertSequenceEqual(n, expected)

        g = Grid(hexagon_type=POINTY, coordinate_system=AXIAL)
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 1), (2, 0), (1, 0), (0, 1), (0, 2), (1, 2)]
        self.assertSequenceEqual(n, expected)

        # Flat topped vs pointy topped in axial coordinates just rotates the grid
        g = Grid(hexagon_type=FLAT, coordinate_system=AXIAL)
        n = g.neighbor_coordinates((1, 1), validate=False)
        expected = [(2, 1), (2, 0), (1, 0), (0, 1), (0, 2), (1, 2)]
        self.assertSequenceEqual(n, expected)

        g = Grid(hexagon_type=POINTY, coordinate_system=CUBIC)
        n = g.neighbor_coordinates((2, 0, -2), validate=False)
        expected = [(3, -1, -2), (3, 0, -3), (2, 1, -3), (1, 1, -2), (1, 0, -1), (2, -1, -1)]
        self.assertSequenceEqual(n, expected)

        # Flat topped vs pointy topped in cubic coordinates just rotates the grid
        g = Grid(hexagon_type=FLAT, coordinate_system=CUBIC)
        n = g.neighbor_coordinates((2, 0, -2), validate=False)
        expected = [(3, -1, -2), (3, 0, -3), (2, 1, -3), (1, 1, -2), (1, 0, -1), (2, -1, -1)]
        self.assertSequenceEqual(n, expected)

    def test_neighbors(self):
        g = Grid(hexagon_type=POINTY, coordinate_system=OFFSET_ODD_ROWS)
        g[1, 1] = 'center'
        g[1, 0] = 'adjacent 1'
        g[2, 0] = 'adjacent 2'
        g[3, 3] = 'not adjacent'

        n = g.neighbors((1, 1))
        self.assertSequenceEqual(n, ['adjacent 2', 'adjacent 1'])

        g = Grid(hexagon_type=POINTY, coordinate_system=CUBIC)
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
        g.set_coordinate_system(CUBIC)
        coord = tuple(g.keys())[0]
        self.assertSequenceEqual(coord, (0, 0, 0))

    def test_distance(self):
        g = Grid()

        self.assertEqual(g.distance((0, 0), (1, 0)), 1)
        self.assertEqual(g.distance((0, 0), (0, -2)), 2)
        g = Grid(coordinate_system=CUBIC)
        self.assertEqual(g.distance((0, 0, 0), (1, 0, -1)), 1)
        self.assertEqual(g.distance((0, 0, 0), (0, -2, 2)), 2)

        g = Grid(coordinate_system=AXIAL)
        self.assertEqual(g.distance((0, 0), (1, 0)), 1)
        self.assertEqual(g.distance((0, 0), (0, -2)), 2)

    def test_within_coordinates(self):
        g = Grid(hexagon_type=HexagonType.FLAT, coordinate_system=CoordinateSystem.OFFSET)
        for i in range(-3, 4):
            for j in range(-3, 4):
                g[i, j] = None

        expected = [(0, 0), (0, -1), (0, 1), (1, -1), (1, 0), (-1, -1), (-1, 0)]
        self.assertCountEqual(g.within_coordinates((0, 0), 1, validate=True), expected)

        expected = [(0, 0), (0, -1), (0, 1), (1, -1), (1, 0), (-1, -1), (-1, 0),
                    (0, -2), (1, -2), (2, -1), (2, 0), (2, 1), (1, 1), (0, 2),
                    (-1, 1), (-2, 1), (-2, 0), (-2, -1), (-1, -2)]
        self.assertCountEqual(g.within_coordinates((0, 0), 2, validate=True), expected)

        g = Grid(hexagon_type=HexagonType.FLAT, coordinate_system=CoordinateSystem.CUBIC)
        for i in range(-3, 4):
            for j in range(-3, 4):
                c = Grid.convert((i, j), CoordinateSystem.AXIAL, CoordinateSystem.CUBIC)
                g[c] = None

        expected = [(2, 0, -2), (2, 1, -3), (3, 0, -3), (3, -1, -2), (2, -1, -1),
                    (1, 0, -1), (1, 1, -2)]
        self.assertCountEqual(g.within_coordinates((2, 0, -2), 1, validate=True), expected)

        expected = [(2, 0, -2), (2, 1, -3), (3, 0, -3), (3, -1, -2), (2, -1, -1),
                    (1, 0, -1), (1, 1, -2), (3, -2, -1), (2, -2, 0), (1, -1, 0),
                    (0, 0, 0), (0, 1, -1), (0, 2, -2), (1, 2, -3)]
        self.assertCountEqual(g.within_coordinates((2, 0, -2), 2, validate=True), expected)

    def test_within(self):
        g = Grid(hexagon_type=HexagonType.FLAT, coordinate_system=CoordinateSystem.OFFSET)
        for i in range(-3, 4):
            for j in range(-3, 4):
                g[i, j] = None

        expected = [None] * 7
        self.assertCountEqual(g.within((0, 0), 1), expected)

        g = Grid(hexagon_type=HexagonType.FLAT, coordinate_system=CoordinateSystem.CUBIC)
        for i in range(-3, 4):
            for j in range(-3, 4):
                c = Grid.convert((i, j), CoordinateSystem.AXIAL, CoordinateSystem.CUBIC)
                g[c] = None

        expected = [None] * 7
        self.assertCountEqual(g.within((2, 0, -2), 1), expected)

    def test_ring_coordinates(self):
        g = Grid(HexagonType.FLAT, CoordinateSystem.AXIAL)
        for i in range(5):
            for j in range(5):
                g[i, j] = None

        expected = [(0, 2), (1, 1), (2, 0)]
        self.assertCountEqual(g.ring_coordinates((0, 0), 2, validate=True), expected)

        expected = g.neighbor_coordinates((1, 2), validate=True)
        self.assertCountEqual(g.ring_coordinates((1, 2), 1, validate=True), expected)

        g = Grid(hexagon_type=HexagonType.FLAT, coordinate_system=CoordinateSystem.CUBIC)
        for i in range(-3, 4):
            for j in range(-3, 4):
                c = Grid.convert((i, j), CoordinateSystem.AXIAL, CoordinateSystem.CUBIC)
                g[c] = None

        expected = [(0, -3, 3), (1, -3, 2), (2, -3, 1), (3, -3, 0)]
        self.assertCountEqual(g.ring_coordinates((3, -6, 3), 3), expected)

    def test_ring(self):
        g = Grid(HexagonType.FLAT, CoordinateSystem.AXIAL)
        for i in range(5):
            for j in range(5):
                g[i, j] = None

        expected = [None] * 3
        self.assertCountEqual(g.ring((0, 0), 2), expected)

        expected = g.neighbors((1, 2))
        self.assertCountEqual(g.ring((1, 2), 1), expected)

        g = Grid(hexagon_type=HexagonType.FLAT, coordinate_system=CoordinateSystem.CUBIC)
        for i in range(-3, 4):
            for j in range(-3, 4):
                c = Grid.convert((i, j), CoordinateSystem.AXIAL, CoordinateSystem.CUBIC)
                g[c] = None

        expected = [None] * 4
        self.assertCountEqual(g.ring((3, -6, 3), 3), expected)
