import re
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
                val = "X" if (x, y) in self.points else "O"
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
                    val = "X" if (x, y) in self.points else "O"
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
        y, x = point

        dct = {
            "U": (x, y - 1),
            "D": (x, y + 1),
            "L": (x - 1, y),
            "R": (x + 1, y),
            "UR": (x + 1, y-1),
            "DR": (x + 1, y + 1),
            "DL": (x - 1, y + 1),
            "UL": (x - 1, y-1)
        }
        resp = [None, []]
        # if we need a main dir (U, D, L, R), then we need to search for double characet
        needed_len = 2 if len(direction) == 1 else 2
        for k, point in zip(dct.keys(), dct.values()):

            x_inrange = 0 <= point[0] < self.dim
            y_inrange = 0 <= point[1] < self.dim

            if not all([x_inrange, y_inrange]):
                continue

            # check if we need to add it to the response object
            if k == direction:
                resp[0] = point
                continue

            # The key might still be a side key
            if len(k) != needed_len:
                continue

            wanted_key = direction in k if needed_len == 2 else k in direction
            if not wanted_key:
                continue

            if point not in self.points:
                resp[1].append(point)
        return resp

    def update(self, gravity = "DR"):
        """
        Moves all points in given direction
        """
        assert gravity in ["U", "D", "L", "R"], "Invalid gravity"
        i = -1
        while i < len(self.points):
            i += 1
            point = self.points[i]
            # get the point in the wanted direction
            gravpoint, sides = self.neighbor(point, direction = gravity)

            if gravpoint is None and sides == []:
                continue

            if gravpoint is not None and gravpoint not in self.points:
                i = 0
                self.points.remove(point)
                self.points.append(gravpoint)

            elif sides != []:
                i = 0
                self.points.remove(point)
                self.points.append(random.choice(sides))

        return self








if __name__ == "__main__":

    board = Board(4)
    print(board.update("U"))
    # print(board)
    # print(board.print_lights())


    # print("")
    # print(board)
    # print(board.print_lights())