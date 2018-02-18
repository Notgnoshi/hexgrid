from .enums import CoordinateSystem, HexagonType
from .enums import FLAT, POINTY
from .enums import OFFSET, CUBIC, AXIAL
from .enums import OFFSET_EVEN_COLUMNS, OFFSET_ODD_COLUMNS, OFFSET_EVEN_ROWS, OFFSET_ODD_ROWS


class Grid(dict):
    """
        Implements a configurable hexagonal Grid.
    """

    def __init__(self, hexagon_type=POINTY, coordinate_system=OFFSET):
        """
            Constructs an empty Grid with a given coordinate system and hexagon type. Choices for
            the hexagon type are:

                * POINTY                    (default)
                * FLAT

            Coordinate system choices are one of the following:

                * OFFSET or OFFSET_ODD_ROWS (default if hexagon_type is POINTY)
                * OFFSET_ODD_COLUMNS        (default if hexagon_type is FLAT)
                * OFFSET_EVEN_ROWS
                * OFFSET_EVEN_COLUMNS
                * CUBIC
                * AXIAL

            All of the coordinate systems use ordered pairs to index Cells except the 'cube'
            coordinate system, which uses ordered (x, y, z) triples.

            Examples:

            >>> Grid()
            <Grid POINTY, OFFSET_ODD_ROWS>
            >>> Grid(hexagon_type=FLAT)
            <Grid FLAT, OFFSET_ODD_COLUMNS>
            >>> Grid(coordinate_system=AXIAL)
            <Grid POINTY, AXIAL>
        """
        # Check the hexagon_type and coordinate_system for option errors.
        if hexagon_type not in HexagonType:
            raise ValueError(f'invalid hexagon type {hexagon_type}')
        if coordinate_system not in CoordinateSystem:
            raise ValueError(f'invalid coordinate system {coordinate_system}')

        # Handle the conveniency 'offset' option for coordinate_system
        if coordinate_system is OFFSET and hexagon_type is POINTY:
            coordinate_system = OFFSET_ODD_ROWS
        elif coordinate_system is OFFSET and hexagon_type is FLAT:
            coordinate_system = OFFSET_ODD_COLUMNS

        # Make sure types are compatable.
        if hexagon_type is FLAT and 'ROWS' in coordinate_system.name:
            raise ValueError('Cannot offset by row when using flat-topped hexagons')
        if hexagon_type is POINTY and 'COLUMNS' in coordinate_system.name:
            raise ValueError('Cannot offset by column when using pointy-topped hexagons')

        self.hexagon_type = hexagon_type
        self.coordinate_system = coordinate_system
        super().__init__()

    def __repr__(self):
        """
            The official string representation of a Grid. Displays the hexagon type and the
            coordinate system used.

            Examples:

            >>> Grid()
            <Grid POINTY, OFFSET_ODD_ROWS>
        """
        return f'<Grid {self.hexagon_type.name}, {self.coordinate_system.name}>'

    def _assert_valid_coordinates(self, coordinates):
        """
            Check coordinates for validity, raising a ValueError if they are invalid.
        """
        if isinstance(coordinates, int):
            raise NotImplementedError('integer indexing not supported')
        elif isinstance(coordinates, tuple):
            if self.coordinate_system is CUBIC and len(coordinates) != 3:
                raise ValueError('key must be a 3-tuple')
            elif self.coordinate_system is not CUBIC and len(coordinates) != 2:
                raise ValueError('key must be a 2-tuple')
            if not all(isinstance(x, int) for x in coordinates):
                raise ValueError('key must be a tuple of integers')
        else:
            raise ValueError(f'key must of type tuple, not {type(coordinates)}')

    def __getitem__(self, coordinates):
        """
            Returns the cell at the given coordinates if it exists.
        """
        self._assert_valid_coordinates(coordinates)
        if coordinates not in self:
            raise KeyError(f'No item found at {coordinates}')
        return super().__getitem__(coordinates)

    def __setitem__(self, coordinates, cell):
        """
            Set the cell at the given coordinates to the given cell.
        """
        self._assert_valid_coordinates(coordinates)
        # Tuples are immutable and therefore hashable.
        # Use super()'s __setitem__ so we don't infinitely recurse on self.__setitem__
        super().__setitem__(coordinates, cell)

    def __delitem__(self, coordinates):
        """
            Delete the cell at the given coordinates if it exists.
        """
        self._assert_valid_coordinates(coordinates)
        if coordinates not in self:
            raise KeyError(f'No item found at {coordinates}')

        super().__delitem__(coordinates)

    def neighbor_coordinates(self, coordinates, validate=True):
        """
            Returns neighboring cell coordinates to some given coordinates. Does not include the
            given coordinates.
        """

        # TODO: move to a utils module?
        def __add_coordinates(t1, t2):
            """Add two tuples componentwise"""
            return tuple(c1 + c2 for c1, c2 in zip(t1, t2))

        coordinates = self.convert(coordinates, self.coordinate_system, CUBIC)
        cube_directions = [
            (+1, -1, 0), (+1, 0, -1), (0, +1, -1),
            (-1, +1, 0), (-1, 0, +1), (0, -1, +1)
        ]

        adj = [__add_coordinates(d, coordinates) for d in cube_directions]
        adj = [self.convert(c, CUBIC, self.coordinate_system) for c in adj]
        if validate:
            return [neighbor for neighbor in adj if neighbor in self]
        return adj

    def neighbors(self, coordinates):
        """
            Returns the items in the neighboring cells of some given coordinate. Does not include
            the item at the given coordinates.
        """
        return [self[key] for key in self.neighbor_coordinates(coordinates)]

    def distance(self, coord1, coord2):
        """
            Returns the distance between two given cell coordinates.
        """
        ax, ay, az = self.convert(coord1, self.coordinate_system, CUBIC)
        bx, by, bz = self.convert(coord2, self.coordinate_system, CUBIC)
        return max(abs(ax - bx), abs(ay - by), abs(az - bz))

    def line_coordinates(self, coord1, coord2, validate=True):
        """
            Returns a list of coordinates defining a line between the two given coordinates.
        """
        def __lerp(a, b, t):
            """Runs linear interpolation between two numbers a and b"""
            return a + (b - a) * t

        def __cube_lerp(a, b, t):
            """Runs linear interpolation between two cubic points"""
            ax, ay, az = a
            bx, by, bz = b
            return __lerp(ax, bx, t), __lerp(ay, by, t), __lerp(az, bz, t)

        def __cube_round(coord):
            """Rounds the floating x, y, z cubic coordinates back into integers."""
            x, y, z = coord
            rx, ry, rz = round(x), round(y), round(z)
            dx, dy, dz = abs(rx - x), abs(ry - y), abs(rz - z)
            if dx > dy and dx > dz:
                rx = -ry - rz
            elif dy > dz:
                ry = -rx - rz
            else:
                rz = -rx - ry

            return int(rx), int(ry), int(rz)

        N = self.distance(coord1, coord2)
        # Convert coordinate system after computing distance so distance knows what system to use
        coord1 = self.convert(coord1, self.coordinate_system, CUBIC)
        coord2 = self.convert(coord2, self.coordinate_system, CUBIC)

        cells = [__cube_round(__cube_lerp(coord1, coord2, i / N)) for i in range(N + 1)]
        cells = [self.convert(c, CUBIC, self.coordinate_system) for c in cells]

        if validate:
            return [c for c in cells if c in self]
        return cells

    def lines(self, coord1, coord2):
        """
            Returns all cells on a line between the two given coordinates.
        """
        return [self[key] for key in self.line_coordinates(coord1, coord2)]

    def within(self, cell, radius):
        """
            Returns all cells within `distance` of the given cell.
        """
        raise NotImplementedError

    def ring(self, cell, radius):
        """
            Returns all cells `radius` away of the given cell.
        """
        raise NotImplementedError

    def spiral(self, cell, radius):
        """
            Returns an ordered list of cells spiralling away from the given
            cell with a given radius.
        """
        raise NotImplementedError

    def shortest_path(self, coordinate1, coordinate2):
        """
            Returns an ordered list of cells between two given coordinates representing the
            shortest path between those coordinates. Returns an empty list if no such path exists.
        """
        raise NotImplementedError

    @classmethod
    def convert(cls, coordinates, from_sys, to_sys):
        """
            Converts coordinates of one type to coordinates of another type. Note that 'cube'
            coordinates must sum to 0.

            Example
            >>> Grid.convert((0, 0), AXIAL, CUBIC)
            (0, 0, 0)
        """
        if from_sys is OFFSET or to_sys is OFFSET:
            raise ValueError('OFFSET not detailed enough. Offset by row or column explicitly.')
        if from_sys not in CoordinateSystem:
            raise ValueError(f'invalid coordinate system {from_sys}')
        if to_sys not in CoordinateSystem:
            raise ValueError(f'invalid coordinate system {to_sys}')

        if from_sys == to_sys:
            return coordinates

        def __identity(coord):
            """The identity coordinate conversion"""
            return coord

        def __axial_to_cube(coord):
            """Converts 'axial' coordinates to 'cube' coordinates"""
            q, r = coord
            x = q
            z = r
            y = -x-z
            return x, y, z

        def __odd_row_to_cube(coord):
            """Converts 'offset-odd-rows' coordinates to 'cube' coordinates"""
            col, row = coord
            # In Python (unlike C++) % implements `modulo` and not `remainder`,
            # and thus works correctly with negative numbers.
            parity = row % 2
            x = col - (row - parity) // 2
            z = row
            y = -x-z
            return x, y, z

        def __even_row_to_cube(coord):
            """Converts 'offset-even-rows' coordinates to 'cube' coordinates"""
            col, row = coord
            parity = row % 2
            x = col - (row + parity) // 2
            z = row
            y = -x-z
            return x, y, z

        def __odd_column_to_cube(coord):
            """Converts 'offset-odd-columns' coordinates to 'cube' coordinates"""
            col, row = coord
            parity = col % 2
            x = col
            z = row - (col - parity) // 2
            y = -x-z
            return x, y, z

        def __even_column_to_cube(coord):
            """Converts 'offset-even-columns' coordinates to 'cube' coordinates"""
            col, row = coord
            parity = col % 2
            x = col
            z = row - (col + parity) // 2
            y = -x-z
            return x, y, z

        def __cube_to_axial(coord):
            """Converts 'cube' coordinates to 'axial' coordinates"""
            x, _, z = coord
            q = x
            r = z
            return q, r

        def __cube_to_odd_row(coord):
            """Converts 'cube' coordinates to 'offset-odd-rows' coordinates"""
            x, _, z = coord
            parity = z % 2
            col = x + (z - parity) // 2
            row = z
            return col, row

        def __cube_to_even_row(coord):
            """Converts 'cube' coordinates to 'offset-even-rows' coordinates"""
            x, _, z = coord
            parity = z % 2
            col = x + (z + parity) // 2
            row = z
            return col, row

        def __cube_to_odd_column(coord):
            """Converts 'cube' coordinates to 'offset-odd-columns' coordinates"""
            x, _, z = coord
            parity = x % 2
            col = x
            row = z + (x - parity) // 2
            return col, row

        def __cube_to_even_column(coord):
            """Converts 'cube' coordinates to 'offset-even-columns' coordinates"""
            x, _, z = coord
            parity = x % 2
            col = x
            row = z + (x + parity) // 2
            return col, row

        to_cube = {
            AXIAL: __axial_to_cube,
            OFFSET_ODD_ROWS: __odd_row_to_cube,
            OFFSET_ODD_COLUMNS: __odd_column_to_cube,
            OFFSET_EVEN_ROWS: __even_row_to_cube,
            OFFSET_EVEN_COLUMNS: __even_column_to_cube,
            CUBIC: __identity,
        }

        from_cube = {
            AXIAL: __cube_to_axial,
            OFFSET_ODD_ROWS: __cube_to_odd_row,
            OFFSET_ODD_COLUMNS: __cube_to_odd_column,
            OFFSET_EVEN_ROWS: __cube_to_even_row,
            OFFSET_EVEN_COLUMNS: __cube_to_even_column,
            CUBIC: __identity,
        }

        partially_converted = to_cube[from_sys](coordinates)
        fully_converted = from_cube[to_sys](partially_converted)
        return fully_converted

    def set_coordinate_system(self, new_system):
        """
            Converts grid to the given coordinate system. Essentially removes and reinserts every
            item in the Grid.
        """

        if new_system not in CoordinateSystem:
            raise ValueError(f'Cannot switch to coordinate system {new_system}')

        # Handle the conveniency 'offset' option for coordinate_system
        if new_system is OFFSET and self.hexagon_type is POINTY:
            new_system = OFFSET_ODD_ROWS
        elif new_system is OFFSET and self.hexagon_type is FLAT:
            new_system = OFFSET_ODD_COLUMNS

        # Change the hexagon type if necessary
        if 'ROWS' in new_system.name:
            self.hexagon_type = POINTY
        elif 'COLUMNS' in new_system.name:
            self.hexagon_type = FLAT

        tmp = []
        old_system = self.coordinate_system
        self.coordinate_system = new_system
        while self:
            old_key, value = self.popitem()
            new_key = self.convert(old_key, old_system, self.coordinate_system)
            tmp.append((new_key, value))

        for key, value in tmp:
            self[key] = value
