#!/usr/bin/env python3
import sys
sys.path.append('..')

from hexgrid import Grid, DrawGrid, HexagonType, CoordinateSystem


def main():
    g = Grid(hexagon_type=HexagonType.FLAT, coordinate_system=CoordinateSystem.OFFSET)

    for i in range(-3, 4):
        for j in range(-3, 4):
            g[i, j] = None

    draw_obj = DrawGrid(g)
    draw_obj.draw_hexagons(g.keys(), labels=True, fill='#7070ff')
    draw_obj.draw()

if __name__ == '__main__':
    main()
