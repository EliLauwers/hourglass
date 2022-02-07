from Board import Board


class Hourglass:
    def __init__(self, dim, p1 = None, p2 = None):

        self.dim = dim
        self.top = Board(self.dim, p1)
        self.bottom = Board(self.dim, p2)
        self.gravity = "DR"
        self.initial_gravity = "DR"

    def __str__(self):
        resp = [str(board) for board in [self.top, self.bottom]]
        return ("\n" + "#" * self.dim * 2 + "\n").join(resp)

    def __repr__(self):
        points = [board.points for board in [self.top, self.bottom]]
        string = f"Hourglass({self.dim}, points = {points})"
        return string

    def update_gravity(self, gravity):
        assert gravity in ["U", "D", "L", "R", "UL", "UR", "DR", "DL"], "Invalid gravity"
        self.gravity = gravity
        return

    def follow(self, gravity):
        follow_states = []
        for board in [self.top, self.bottom]:
            something, follow_state = board.follow(gravity)
            follow_states.append(follow_state)
        return self, follow_states

    def position_boards(self):
        if self.gravity == self.initial_gravity:
            return self.top, self.bottom
        return self.bottom, self.top

    def drop_sand(self):
        """
        Takes a sand drop from the top board and puts it at the bottom
        :return: None
        """
        # get top board
        assert self.gravity in ["UL","DR"], "invalid gravity"
        top, bottom = self.position_boards()
        # check if any sand can drop
        if top.points == []:
            # the top board is empty
            return self, False
        # Sample one of the top points, where the sum is smallest
        sums = [sum(p) for p in top.points]
        dir_of_interest = min(sums) if top == self else max(sums)
        index = sums.index(dir_of_interest)
        poi = top.points[index]
        # remove that point from the top board and insert it in the bottom board
        top.points.remove(poi)
        insert_place = (0, 0) if top == self.top else (self.dim - 1, self.dim - 1)
        bottom.points.insert(0, insert_place)
        return self, True
