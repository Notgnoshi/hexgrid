"""
hexgrid internal utils. Not intended for external use.
"""
import heapq

def tuple_add(t1, t2):
    """
        Adds two tuples componentwise

        Example
        >>> t1 = (1, 2, 3)
        >>> t2 = (4, 5, 6)
        >>> tuple_add(t1, t2)
        (5, 7, 9)
    """
    return tuple(r + s for r, s in zip(t1, t2))


def tuple_multiply(t, k):
    """
        Multiplies the tuple `t` by the scalar `k`

        Example
        >>> t = (1, 2, 3)
        >>> tuple_multiply(t, -1)
        (-1, -2, -3)
    """
    return tuple(k * t_i for t_i in t)


class PriorityQueue(object):
    """
        Implements a priority queue using a heap
    """
    def __init__(self):
        self.elements = []

    def empty(self):
        """
            Returns True if the queue is empty, False otherwise
        """
        return len(self.elements) == 0

    def put(self, item, priority):
        """
            Places an item in the priority queue given that item and its priority
        """
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        """
            Gets the item at the front of the priority queue
        """
        return heapq.heappop(self.elements)[1]


def __heuristic(a, b):
    """
        The heuristic for A* Grid search
    """
    return sum(abs(ai - bi) for ai, bi in zip(a, b))


def a_star_search(grid, start, goal):
    """
        Runs A* on a given Grid to find the shortest weighted path from start to goal.
    """
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for coord in grid.neighbor_coordinates(current):
            # TODO: Pass in a cost function?
            new_cost = cost_so_far[current] + 1 # grid.cost(current, coord)

            if coord not in cost_so_far or new_cost < cost_so_far[coord]:
                cost_so_far[coord] = new_cost
                priority = new_cost + __heuristic(goal, coord)
                frontier.put(coord, priority)
                came_from[coord] = current

    return came_from
