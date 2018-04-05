"""
Defines a configurable hexagonal Grid. The Grid subclasses dict,
but adds convenience wrappers for different hexagon types, different
coordinate systems, and several operations on the Grid.

Example:
>>> g = Grid()
>>> g[1, 0] = '1 0'
>>> g[0, 0] = '0 0'
>>> g.items()
dict_items([((1, 0), '1 0'), ((0, 0), '0 0')])
>>> g[0, 0]
'0 0'
>>> g[-1, 1]
Traceback (most recent call last):
...
KeyError: 'No item found at (-1, 1)'
"""

from .grid import Grid
from .draw import DrawGrid

from .enums import HexagonType, CoordinateSystem
from .enums import FLAT, POINTY
from .enums import OFFSET, CUBIC, AXIAL
from .enums import OFFSET_EVEN_COLUMNS, OFFSET_ODD_COLUMNS, OFFSET_EVEN_ROWS, OFFSET_ODD_ROWS
