class Cell(object):
    """
        Implements a hexagonal Cell.
    """
    def __init__(self, coordinates, cell_type='pointy-topped'):
        """
            Constructs either a 'pointy-topped' (default) hexagonal cell, or a
            'flat-topped' cell.
        """

        if cell_type.lower() not in ['pointy-topped', 'flat-topped']:
            raise ValueError('cell_type must be one of: \'pointy-topped\' or \'flat-topped\'')

        self.cell_type = cell_type.lower()
        self.coordinates = coordinates
        # Cells are containers
        self.data = None

    def __repr__(self):
        return f'<Cell {id(self)}>'

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self):
        # TODO: Make Cells hashable by their coordinates
        raise NotImplementedError
