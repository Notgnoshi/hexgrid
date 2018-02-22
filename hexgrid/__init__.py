"""
Defines a configurable hexagonal grid.
"""

from tests import run_once

from .grid import Grid
from .draw import DrawGrid

from .enums import HexagonType, CoordinateSystem
from .enums import FLAT, POINTY
from .enums import OFFSET, CUBIC, AXIAL
from .enums import OFFSET_EVEN_COLUMNS, OFFSET_ODD_COLUMNS, OFFSET_EVEN_ROWS, OFFSET_ODD_ROWS


@run_once
def load_tests(loader, tests, ignore):
    import doctest
    tests.addTests(doctest.DocTestSuite('hexgrid'))
    tests.addTests(doctest.DocTestSuite('hexgrid.enums'))
    tests.addTests(doctest.DocTestSuite('hexgrid.grid'))
    tests.addTests(doctest.DocTestSuite('hexgrid.draw'))
    tests.addTests(doctest.DocTestSuite('hexgrid.utils'))
    return tests
