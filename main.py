import re

class Board:
    def __init__(self, dim, points = None):
        self.dim = dim
        # if no points were supplied, create new points
        points = self.create_points() if not points else points
        # check if no point lays outside of the board
        points_check = [all([el <= dim - 1 for el in point]) for point in points]
        assert all(points_check), "Points exceed dimension"
        self.points = set(points)

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

        if "U" in direction:
            y -= 1
        elif "D" in direction:
            y += 1

        if "L" in direction:
            x -= 1
        elif "R" in direction:
            x += 1

        # points must fall in the board
        if not 0 <= x < self.dim:
            return None
        if not 0 <= y < self.dim:
            return None
        return y, x

    def update(self, gravity = "DR"):
        """
        Moves all points in given direction
        """
        assert gravity in ["U", "D", "L", "R", "UR", "DR", "DL", "UL"], "Invalid gravity"
        point_found = True
        while point_found:
            point_found = False
            for point in self.points:
                # get the point in the wanted direction
                quest = self.neighbor(point, direction = gravity)

                if not quest:
                    continue

                neighbor_empty = quest not in self.points
                if neighbor_empty:
                    point_found = True
                    self.points.remove(point)
                    self.points.add(quest)
            x = 1
        return self








if __name__ == "__main__":

    board = Board(4)
    # print(board)
    # print(board.print_lights())

    for dir in ["U", "UR",  "R", "DR", "D", "DL", "L", "UL"]:
        print("Original")
        print(Board(4))
        print(f"Dir: {dir}")
        print(Board(4).update(dir))
        print("\n\n")
    # print("")
    # print(board)
    # print(board.print_lights())