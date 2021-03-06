#!/usr/bin/env python3
"""
    An example of drawing a simple grid.
"""

import sys
sys.path.append('..')

from hexgrid import Grid, DrawGrid, HexagonType, CoordinateSystem
from hexgrid import FLAT, OFFSET


def main():
    # grid = Grid(coordinate_system=OFFSET, hexagon_type=FLAT)

    # grid[-1, -1] = None
    # grid[-1, 0] = None
    # grid[0, 0] = None
    # grid[0, 1] = None
    # grid[1, 0] = None
    # grid[1, 1] = None
    # grid[1, 2] = None
    # path = grid.shortest_path_coordinates((-1, -1), (1, 2))
    # print(path)

    grid = Grid(hexagon_type=HexagonType.FLAT, coordinate_system=CoordinateSystem.CUBIC)

    for i in range(-3, 4):
        for j in range(-3, 4):
            c = Grid.convert((i, j), CoordinateSystem.AXIAL, CoordinateSystem.CUBIC)
            grid[c] = None

    path = grid.shortest_path_coordinates((-3, 2, 1), (3, -2, -1))

    draw = DrawGrid(grid)
    draw.draw_hexagons(grid.keys(), labels=True, fill='#7070ff')
    draw.draw_hexagons(path, labels=True, fill='#ff7070')
    draw.draw()


if __name__ == '__main__':
    main()
