#!/usr/bin/env python3
"""
    An example of drawing a simple grid.
"""

import sys
sys.path.append('..')

from hexgrid import Grid, DrawGrid
from hexgrid import FLAT, OFFSET


def main():
    grid = Grid(coordinate_system=OFFSET, hexagon_type=FLAT)

    grid[-1, -1] = None
    grid[0, 0] = None
    grid[0, 1] = None
    grid[1, 0] = None
    grid[1, 1] = None
    grid[1, 2] = None

    neighbors = grid.neighbor_coordinates((0, 0))

    line = grid.line_coordinates((0, 0), (4, 4), validate=False)

    draw = DrawGrid(grid)
    draw.draw_hexagons(grid.keys(), labels=True, fill='#7070ff')
    draw.draw_hexagons(neighbors, labels=True, fill='#ff7070')
    draw.draw_hexagons(line, labels=True, fill='#70ff70')
    draw.draw()


if __name__ == '__main__':
    main()
