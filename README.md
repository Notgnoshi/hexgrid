# hexgrid

Implements a hexagonal grid data structure in Python.

Supports different coordinate systems for flat-topped and pointy-topped hexagons, including axial, cubic, and rectangular offset coordinate systems. Multiple offsets are supported, including odd and even variants of row and column offsets.

## `Grid`

Implements a hexagonal grid container class with flexible coordinate systems.

## TODO list

* Documentation and examples
* `shortest_path` weighting. Maybe now is the time to think about a `Cell` class?
* Unit test `shortest_path`. Do something harder than a short, direct linear path.
* `convex hull`
* `nearest_neighbors`
* Disjoint sets?
* Draw `Grid`s.
  * Make work inline in Jupyter Notebooks
  * Pretty colors
  * SVG? Might work better with Jupyter...
  * Make `draw` a method of `Grid`?
  * What happens if you try to draw nothing? (hint: it crashes)
* Generate different kinds of `Grid`s: triangles, circles, parallelograms, etc
