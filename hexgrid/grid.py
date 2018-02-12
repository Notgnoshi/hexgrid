class Grid(object):
    """
        Implements a configurable hexagonal Grid.
    """

    HEXAGON_TYPE_OPTIONS = ['pointy-topped',
                            'flat-topped',
                           ]

    COORDINATE_SYSTEM_OPTIONS = ['offset',
                                 'offset-odd-row',
                                 'offset-odd-column',
                                 'offset-even-row',
                                 'offset-even-column',
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

                * 'offset' or 'offset-odd-row'    (default if hexagon_type is 'pointy-topped')
                * 'offset-odd-column'             (default if hexagon_type is 'flat-topped')
                * 'offset-even-row'
                * 'offset-even-column'
                * 'cube'
                * 'axial'

            All of the coordinate systems use ordered pairs to index Cells except the 'cube'
            coordinate system, which uses ordered (x, y, z) triples.

            Examples:

            >>> Grid()
            <Grid pointy-topped, offset-odd-row>
            >>> Grid(hexagon_type='flat-topped')
            <Grid flat-topped, offset-odd-column>
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
            coordinate_system = 'offset-odd-row'
        elif coordinate_system.lower() == 'offset' and hexagon_type.lower() == 'flat-topped':
            coordinate_system = 'offset-odd-column'

        # Make sure types are compatable.
        if hexagon_type.lower() == 'flat-topped' and 'row' in coordinate_system.lower():
            raise ValueError('Cannot offset by row when using flat-topped hexagons')
        if hexagon_type.lower() == 'pointy-topped' and 'column' in coordinate_system.lower():
            raise ValueError('Cannot offset by column when using pointy-topped hexagons')

        self.hexagon_type = hexagon_type.lower()
        self.coordinate_system = coordinate_system.lower()

    def __repr__(self):
        """
            The official string representation of a Grid. Displays the hexagon type and the
            coordinate system used.
        """
        return f'<Grid {self.hexagon_type}, {self.coordinate_system}>'

    def _neighbor_coordinates(self, coordinates):
        """
            Returns the neighbor cell coordinates to some given coordinates.
        """
        raise NotImplementedError

    def neighbors(self, coordinates):
        """
            Returns the neighbor cells to some given coordinates.
        """
        raise NotImplementedError

    def __len__(self):
        """
            Returns the number of Cells in the Grid.
        """

    def __getitem__(self, coordinates):
        """
            Returns the cell at the given coordinates if it exists.
        """
        raise NotImplementedError

    def __setitem__(self, coordinates, cell):
        """
            Set the cell at the given coordinates to the given cell.
        """
        raise NotImplementedError

    def __delitem__(self, coordinates):
        """
            Delete the cell at the given coordinates if it exists. Does not
            change the Grid dimensions, or adjacent cell coordinates, but does
            change the len() of the Grid.
        """
        raise NotImplementedError

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
            """Converts 'offset-odd-row' coordinates to 'cube' coordinates"""
            col, row = coord
            # In Python (unlike C++) % implements `modulo` and not `remainder`,
            # and thus works correctly with negative numbers.
            parity = row % 2
            x = col - (row - parity) / 2
            z = row
            y = -x-z
            return x, y, z

        def __even_row_to_cube(coord):
            """Converts 'offset-even-row' coordinates to 'cube' coordinates"""
            col, row = coord
            parity = row % 2
            x = col - (row + parity) / 2
            z = row
            y = -x-z
            return x, y, z

        def __odd_column_to_cube(coord):
            """Converts 'offset-odd-column' coordinates to 'cube' coordinates"""
            col, row = coord
            parity = col % 2
            x = col
            z = row - (col - parity) / 2
            y = -x-z
            return x, y, z

        def __even_column_to_cube(coord):
            """Converts 'offset-even-column' coordinates to 'cube' coordinates"""
            col, row = coord
            parity = col % 2
            x = col
            z = row - (col + parity) / 2
            y = -x-z
            return x, y, z

        def __cube_to_axial(coord):
            """Converts 'cube' coordinates to 'axial' coordinates"""
            x, _, z = coord
            q = x
            r = z
            return q, r

        def __cube_to_odd_row(coord):
            """Converts 'cube' coordinates to 'offset-odd-row' coordinates"""
            x, _, z = coord
            parity = z % 2
            col = x + (z - parity) / 2
            row = z
            return col, row

        def __cube_to_even_row(coord):
            """Converts 'cube' coordinates to 'offset-even-row' coordinates"""
            x, _, z = coord
            parity = z % 2
            col = x + (z + parity) / 2
            row = z
            return col, row

        def __cube_to_odd_column(coord):
            """Converts 'cube' coordinates to 'offset-odd-column' coordinates"""
            x, _, z = coord
            parity = x % 2
            col = x
            row = z + (x - parity) / 2
            return col, row

        def __cube_to_even_column(coord):
            """Converts 'cube' coordinates to 'offset-even-column' coordinates"""
            x, _, z = coord
            parity = x % 2
            col = x
            row = z + (x + parity) / 2
            return col, row

        to_cube = {
            'axial': __axial_to_cube,
            'offset-odd-row': __odd_row_to_cube,
            'offset-odd-column': __odd_column_to_cube,
            'offset-even-row': __even_row_to_cube,
            'offset-even-column': __even_column_to_cube,
            'cube': __identity,
        }

        from_cube = {
            'axial': __cube_to_axial,
            'offset-odd-row': __cube_to_odd_row,
            'offset-odd-column': __cube_to_odd_column,
            'offset-even-row': __cube_to_even_row,
            'offset-even-column': __cube_to_even_column,
            'cube': __identity,
        }

        partially_converted = to_cube[from_sys](coordinates)
        fully_converted = from_cube[to_sys](partially_converted)
        return fully_converted
