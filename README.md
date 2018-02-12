# hexgrid

Implements a hexagonal grid in Python.

Supports different coordinate systems for flat-topped and pointy-topped hexagons, including axial, cubic, and rectangular offset coordinate systems. Multiple offsets are supported, including odd and even variants of row and column offsets.

## `Grid`

Implements a hexagonal grid container class with flexible coordinate systems.

## `Cell`

I don't know what this is supposed to be. I'll probably remove it later.

## TODO list

* Make `Cell`s hashable by coordinates.
* Decide on core data structure for `Grid` to use. I think converting everything to 'offset-odd-row' internally and then using a 2D array will work nicely. However, I want `__setitem__` to not raise `IndexError`, and insert cells wherever (expand the grid dynamically because we don't construct it with a given size). So then I'd want a sparse data structure. Consider using a `dict` and hash by the coordinates.
* `_neighbor_coordinates`. Probably rename the function and make it public.
* `neighbors`. Return neighboring items if they exist.
* `__len__`,
* `__getitem__`, `__setitem__`, and `__delitem__`. Forcing the coordinates to be tuples allows them to be hashed.
* Figure out how to index `__getitem__` by an integer to allow looping.
* `distance`. I'm presuming that there is only one distance metric...
* `within`, `ring`, and `spiral`.
* More unit tests for `convert`. Possibly clean up `convert`s implementation?
* `__iter__` or similar: return an iterator over all the cells with data in them.
