from enum import Enum, auto


class HexagonType(Enum):
    """Hexagons can be either flat-topped or pointy-topped."""
    POINTY = auto()
    FLAT = auto()


class CoordinateSystem(Enum):
    """Describes the different coordinate systems available."""
    OFFSET = auto()
    OFFSET_ODD_ROWS = auto()
    OFFSET_ODD_COLUMNS = auto()
    OFFSET_EVEN_ROWS = auto()
    OFFSET_EVEN_COLUMNS = auto()
    AXIAL = auto()
    CUBIC = auto()


POINTY = HexagonType.POINTY
FLAT = HexagonType.FLAT

OFFSET = CoordinateSystem.OFFSET
OFFSET_ODD_ROWS = CoordinateSystem.OFFSET_ODD_ROWS
OFFSET_EVEN_ROWS = CoordinateSystem.OFFSET_EVEN_ROWS
OFFSET_ODD_COLUMNS = CoordinateSystem.OFFSET_ODD_COLUMNS
OFFSET_EVEN_COLUMNS = CoordinateSystem.OFFSET_EVEN_COLUMNS
CUBIC = CoordinateSystem.CUBIC
AXIAL = CoordinateSystem.AXIAL
