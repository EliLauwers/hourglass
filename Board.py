import random

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
                val = "X" if (x, y) in self.points else " "
                row.append(val)
            matrix.append(" ".join(row))
        return "\n".join(matrix)

    def __eq__(self, other):
        return id(self) == id(other)

    def create_points(self):
        """
        Used when no points are supplied
        :return: a list of points needed in the init
        """
        # create a half empty matrix
        locs = [(x, y) for x in range(self.dim) for y in range(self.dim)]
        points = []
        for x, y in locs:
            loc_ind = x * self.dim + y
            if loc_ind >= ((self.dim ** 2) / 2):
                points.append((x, y))
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
        if len(self.points) == 0:
            return self, False

        point = self.points[0]
        # check if the point can fall down to gravity
        gravpoint = self.neighbor(point, gravity)

        if gravpoint:
            self.points.remove(point)
            self.points.append(gravpoint)
            follow_state = True
            return self, follow_state

        # the point cannot fall down
        # let the point fall to a side
        side_dirs = self.side_directions(gravity)
        side_points = []
        for dir in side_dirs:
            p = self.neighbor(point, dir)
            if p:
                side_points.append(p)

        if side_points != []:
            self.points.remove(point)
            self.points.append(random.choice(side_points))
            follow_state = True
            return self, follow_state

        # nothing happend, put the point back
        self.points.remove(point)
        self.points.append(point)
        # check if any point can follow in the near future
        follow_states = False
        dirs = [gravity] + side_dirs
        for dir in dirs:
            follow_states = any([self.neighbor(p, dir) for p in self.points])
            if follow_states:
                break


        return self, follow_states

    def side_directions(self, direction):
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
        vertical = ["U", "D"]
        if direction in horizontal:
            return [f"{v}{direction}" for v in vertical]
        return [f"{direction}{h}" for h in horizontal]

