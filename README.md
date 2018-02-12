# hexgrid

Implements a hexagonal grid data structure in Python.

Supports different coordinate systems for flat-topped and pointy-topped hexagons, including axial, cubic, and rectangular offset coordinate systems. Multiple offsets are supported, including odd and even variants of row and column offsets.

## `Grid`

Implements a hexagonal grid container class with flexible coordinate systems.

## TODO list

* `distance`. I'm presuming that there is only one distance metric...
* `within`, `ring`, and `spiral`.
* Change `Grid` coordinate system for all current cells. `set_coordinate_system()` and `set_hexagon_type()`
* Documentation and examples
* Allow for variable number of integer arguments to `neighbors` and `neighbor_coordinates`. E.g. `neighbors(1, 1)` should return the same thing as `neighbors((1, 1))`.
* `shortest_path(coord1, coord2)`
* Draw `Grid`s. This will take some research. This should preferably work inline in a Jupyter Notebook or pop up in a new window otherwise.
* `convex hull`
* `nearest_neighbors`
* Anything I can think of that a game might need.
