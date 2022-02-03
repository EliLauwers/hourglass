import re
import random
import time
from numpy.random import choice

class Board:
    def __init__(self, dim, points = None):
        self.dim = dim
        # if no points were supplied, create new points
        points = self.create_points() if not points else points
        # check if no point lays outside of the board
        points_check = [all([el <= dim - 1 for el in point]) for point in points]
        assert all(points_check), "Points exceed dimension"
        self.points = points

    def __repr__(self):
        """
        Create a string representation of the matrix
        :return: string
        """
        str = f"Board({self.dim}, points={self.points})"
        return str

    def __str__(self):
        """
        Creates a matrix representation of the board
        """
        matrix = []
        for x in range(self.dim):
            row = []
            for y in range(self.dim):
                val = "X" if (x, y) in self.points else "-"
                row.append(val)
            matrix.append(" ".join(row))
        return "\n".join(matrix)

    def print_lights(self, raw = True):
        """
        Pivots the matrix 45 degrees and prints
        :param raw: should original coords be printed (False) or raw points (True)
        :return: string representation of the board
        """
        # create lens out of the dims
        lens = [self.dim]
        for i in range(self.dim - 1, 0, -1):
            lens.append(i)
            lens.insert(0, i)

        # points to array
        array = []
        for x in range(self.dim):
            row = []
            for y in range(self.dim):
                if raw:
                    val = "X" if (x, y) in self.points else "-"
                else:
                    val = f"{x}.{y}"
                row.append(val)
            array.append(row)

        # create the printed matrix
        betw_elements = 3 * ' ' if raw else 5 * ' '
        center = 4 * self.dim + 2 if raw else 7 * self.dim + 2
        new = []
        for length in lens:
            new_row = []
            for ri in range(length):
                ri = length - ri - 1
                val = array[ri][0]
                new_row.append(val)
                del array[ri][0]
                if array[ri] == []:
                    del array[ri]
            new.append(f"{betw_elements.join(new_row).center(center)}")

        return "\n".join([row for row in new])

    def create_points(self):
        """
        Used when no points are supplied
        :return: a list of points needed in the init
        """
        # create a half empty matrix
        locs = [(x, y) for x in range(self.dim) for y in range(self.dim)]
        points = []
        for loc in locs:
            if sum(loc) > (self.dim - 1):
                points.append(loc)
        return points

    def neighbor(self, point, direction):
        """
        Get the neighbor of a point in a given direction. Checks whether the point can be occupied
        :param point:
        :param direction:
        :return:
        """
        col, row = point

        if "U" in direction:
            col -= 1
        elif "D" in direction:
            col += 1

        if "R" in direction:
            row += 1
        elif "L" in direction:
            row -= 1

        row_inrange = 0 <= row < self.dim
        col_inrange = 0 <= col < self.dim
        if not all([row_inrange, col_inrange]):
            return None
        if (col, row) in self.points:
            return None
        return (col, row)

    def follow(self, gravity = "DR"):
        assert gravity in ["U", "D", "L", "R", "UL", "UR", "DR", "DL"], "Invalid gravity"
        point = self.points[0]
        # check if the point can fall down to gravity
        gravpoint = self.neighbor(point, gravity)
        if gravpoint:
            self.points.remove(point)
            self.points.append(gravpoint)
            return self
        # the point cannot fall down
        # let the point fall to a side
        side_dirs = side_directions(gravity)
        side_points = []
        for dir in side_dirs:
            p = self.neighbor(point, dir)
            if not p:
                continue
            side_points.append(p)
        if len(side_points) == 2:
            self.points.remove(point)
            self.points.append(random.choice(side_points))
        elif side_points != []:
            self.points.remove(point)
            self.points.append(side_points[0])
        else:
            # nothing happend, put the point back
            self.points.remove(point)
            self.points.append(point)

        return self



    def pull(self, gravity = "DR", debug = False, wait = 1.25):
        """
        Moves all points in given direction
        """
        if debug:
            print(self)
            print(gravity.center(self.dim * 3, "="))
            assert isinstance(wait, float) or isinstance(wait, int), "numeric data for wait"
            time.sleep(wait)

        assert gravity in ["U", "D", "L", "R", "UL", "UR","DR","DL"], "Invalid gravity"
        side_dirs = side_directions(gravity)
        prev_point = None
        while True:
            gravpoints = [self.neighbor(p, direction=gravity) for p in self.points]
            first, second = [[self.neighbor(p, dir) for p in self.points] for dir in side_dirs]
            if not any(gravpoints + first + second):
                return self

            if debug and prev_point:
                print(self)
                print(gravity.center(self.dim * 3, "="))
                time.sleep(wait)

            if prev_point:
                # check if this point can fall further
                gravpoint = self.neighbor(prev_point, direction=gravity)
                if gravpoint:
                    self.points.remove(prev_point)
                    self.points.add(gravpoint)
                prev_point = gravpoint
            else:
                # check if any point can fall into gravity
                points_copy = self.points.copy()
                gravpoints = [self.neighbor(p, direction=gravity) for p in points_copy]
                first, second = [[self.neighbor(p, dir) for p in points_copy] for dir in side_dirs]
                if any(gravpoints):
                    # iterate over all points with their gravpoint
                    for point, gravpoint in zip(points_copy, gravpoints):
                        if point not in self.points:
                            continue
                        # if a gravpoint can be found ..
                        if not gravpoint:
                            continue
                        # update the points list
                        self.points.remove(point)
                        self.points.add(gravpoint)
                        prev_point = gravpoint
                elif any([first, second]):
                    for point, two_points in zip(points_copy, zip(first, second)):
                        if point not in self.points:
                            continue
                        if not any(two_points):
                            continue
                        if all(two_points):
                            newpoint = random.choice(two_points)
                        elif two_points[0]:
                            newpoint = two_points[0]
                        elif two_points[1]:
                            newpoint = two_points[1]
                        # update the points list
                        self.points.remove(point)
                        # by inserting it at the front, we ensure that the point will be chosen the next time
                        self.points.add(newpoint)
                        prev_point = newpoint
        return self


def side_directions(direction):
    """
    Returns the both wanted sides
    :param direction:
    :return: list
    """
    # if a combined dir has been provided, return the two main dirs
    if len(direction) == 2:
        return list(direction)
    # else, we need to find the sides of a main dir
    horizontal = ["L", "R"]
    vertical = ["U","D"]
    if direction in horizontal:
        return [f"{v}{direction}" for v in vertical]
    return[f"{direction}{h}" for h in horizontal]





if __name__ == "__main__":
    from math import ceil
    dim = 6
    el = ceil(dim / 2)
    points = [
        (el, el),
        (el - 1, el),
        (el, el - 1)
    ]
    board = Board(dim, points)
    dirs = ["U", "D", "L", "R", "UL", "UR","DR","DL"]
    arrows = ["↑","↓","←","→","↖","↗","↘","↙"]
    gravity = dirs[0]
    while True:
        sides = side_directions(gravity)
        probs = [.5 if dir == gravity else .2 if dir in sides else .10 / 5 for dir in dirs]
        gravity = choice(dirs, 1, probs)
        for i in range(10):
            print(arrows[dirs.index(gravity)] * dim * 2)
            print(board.follow(gravity))
            time.sleep(1)

