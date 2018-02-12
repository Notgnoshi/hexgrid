class Grid(dict):
    """
        Implements a configurable hexagonal Grid.
    """

    HEXAGON_TYPE_OPTIONS = ['pointy-topped',
                            'flat-topped',
                           ]

    COORDINATE_SYSTEM_OPTIONS = ['offset',
                                 'offset-odd-rows',
                                 'offset-odd-columns',
                                 'offset-even-rows',
                                 'offset-even-columns',
                                 'axial',
                                 'cube',
                                ]

    def __init__(self, hexagon_type='pointy-topped', coordinate_system='offset'):
        """
            Constructs an empty Grid with a given coordinate system and hexagon type. Choices for
            the hexagon type are:

                * 'pointy-topped'                 (default)
                * 'flat-topped'

            Coordinate system choices are one of the following:

                * 'offset' or 'offset-odd-rows'    (default if hexagon_type is 'pointy-topped')
                * 'offset-odd-columns'             (default if hexagon_type is 'flat-topped')
                * 'offset-even-rows'
                * 'offset-even-columns'
                * 'cube'
                * 'axial'

            All of the coordinate systems use ordered pairs to index Cells except the 'cube'
            coordinate system, which uses ordered (x, y, z) triples.

            Examples:

            >>> Grid()
            <Grid pointy-topped, offset-odd-rows>
            >>> Grid(hexagon_type='flat-topped')
            <Grid flat-topped, offset-odd-columns>
            >>> Grid(coordinate_system='axial')
            <Grid pointy-topped, axial>
        """
        # Check the hexagon_type and coordinate_system for option errors.
        if hexagon_type.lower() not in self.HEXAGON_TYPE_OPTIONS:
            raise ValueError(f"`hexagon_type` must be one of {self.HEXAGON_TYPE_OPTIONS}")
        if coordinate_system.lower() not in self.COORDINATE_SYSTEM_OPTIONS:
            raise ValueError(f"`coordinate_system` must be one of {self.COORDINATE_SYSTEM_OPTIONS}")

        # Handle the conveniency 'offset' option for coordinate_system
        if coordinate_system.lower() == 'offset' and hexagon_type.lower() == 'pointy-topped':
            coordinate_system = 'offset-odd-rows'
        elif coordinate_system.lower() == 'offset' and hexagon_type.lower() == 'flat-topped':
            coordinate_system = 'offset-odd-columns'

        # Make sure types are compatable.
        if hexagon_type.lower() == 'flat-topped' and 'row' in coordinate_system.lower():
            raise ValueError('Cannot offset by row when using flat-topped hexagons')
        if hexagon_type.lower() == 'pointy-topped' and 'column' in coordinate_system.lower():
            raise ValueError('Cannot offset by column when using pointy-topped hexagons')

        self.hexagon_type = hexagon_type.lower()
        self.coordinate_system = coordinate_system.lower()
        super().__init__()

    def __repr__(self):
        """
            The official string representation of a Grid. Displays the hexagon type and the
            coordinate system used.

            Examples:

            >>> Grid()
            <Grid pointy-topped, offset-odd-rows>
        """
        return f'<Grid {self.hexagon_type}, {self.coordinate_system}>'

    def neighbor_coordinates(self, coordinates):
        """
            Returns unvalidated neighboring cell coordinates to some given coordinates. Will happily
            return coordinates off the current grid, or coordinates to nonexistent items in the
            grid. Does not include the given coordinates.
        """

        def __add_coordinates(t1, t2):
            """Add two tuples componentwise"""
            return tuple(c1 + c2 for c1, c2 in zip(t1, t2))

        coordinates = self.convert(coordinates, self.coordinate_system, 'cube')
        cube_directions = [
            (+1, -1, 0), (+1, 0, -1), (0, +1, -1),
            (-1, +1, 0), (-1, 0, +1), (0, -1, +1)
        ]

        neighbors = []
        for direction in cube_directions:
            neighbors.append(__add_coordinates(direction, coordinates))
        return [self.convert(c, 'cube', self.coordinate_system) for c in neighbors]

    def neighbors(self, coordinates):
        """
            Returns the items in the neighboring cells of some given coordinate. Does not include
            the item at the given coordinates.
        """
        adjacents = []
        for neighbor in self.neighbor_coordinates(coordinates):
            if neighbor in self:
                adjacents.append(self[neighbor])

        return adjacents

    def _assert_valid_coordinates(self, coordinates):
        """
            Check coordinates for validity, raising a ValueError if they are invalid.
        """
        if isinstance(coordinates, int):
            raise NotImplementedError('integer indexing not supported')
        elif isinstance(coordinates, tuple):
            if self.coordinate_system == 'cube' and len(coordinates) != 3:
                raise ValueError('key must be a 3-tuple')
            elif self.coordinate_system != 'cube' and len(coordinates) != 2:
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

    def distance(self, coord1, coord2):
        """
            Returns the distance between two given cell coordinates.
        """
        raise NotImplementedError

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
            >>> Grid.convert((0, 0), 'axial', 'cube')
            (0, 0, 0)
        """
        # Cannot convert to or from the 'offset' system as it's an alias for one of two systems.
        if from_sys not in cls.COORDINATE_SYSTEM_OPTIONS[1:]:
            raise ValueError(f"`from_sys` must be one of {cls.COORDINATE_SYSTEM_OPTIONS[1:]}")
        if to_sys not in cls.COORDINATE_SYSTEM_OPTIONS[1:]:
            raise ValueError(f"`to_sys` must be one of {cls.COORDINATE_SYSTEM_OPTIONS[1:]}")

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
            'axial': __axial_to_cube,
            'offset-odd-rows': __odd_row_to_cube,
            'offset-odd-columns': __odd_column_to_cube,
            'offset-even-rows': __even_row_to_cube,
            'offset-even-columns': __even_column_to_cube,
            'cube': __identity,
        }

        from_cube = {
            'axial': __cube_to_axial,
            'offset-odd-rows': __cube_to_odd_row,
            'offset-odd-columns': __cube_to_odd_column,
            'offset-even-rows': __cube_to_even_row,
            'offset-even-columns': __cube_to_even_column,
            'cube': __identity,
        }

        partially_converted = to_cube[from_sys](coordinates)
        fully_converted = from_cube[to_sys](partially_converted)
        return fully_converted
