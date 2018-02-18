# hexgrid

Implements a hexagonal grid data structure in Python.

Supports different coordinate systems for flat-topped and pointy-topped hexagons, including axial, cubic, and rectangular offset coordinate systems. Multiple offsets are supported, including odd and even variants of row and column offsets.

## `Grid`

Implements a hexagonal grid container class with flexible coordinate systems.

## TODO list

* `within`, `ring`, and `spiral`.
* Documentation and examples
* `shortest_path(coord1, coord2)`
* `convex hull`
* `nearest_neighbors`
* Disjoint sets?
* Draw `Grid`s.
  * Make work inline in Jupyter Notebooks
  * Pretty colors
  * SVG? Might work better with Jupyter...
  * Make `draw` a method of `Grid`?
