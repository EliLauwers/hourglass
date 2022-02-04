from Board import Board
from asciimatics.screen import Screen
import time

class Hourglass:
    def __init__(self, dim, p1 = None, p2 = None):

        self.dim = dim
        self.top = Board(self.dim, p1)
        self.bottom = Board(self.dim, p2)
        self.gravity = "DR"
        self.initial_gravity = "DR"

    def update_gravity(self, gravity):
        assert gravity in ["U", "D", "L", "R", "UL", "UR", "DR", "DL"], "Invalid gravity"
        self.gravity = gravity
        dirs = ["U", "D", "L", "R", "UL", "UR", "DR", "DL"]
        arrows = ["↑", "↓", "←", "→", "↖", "↗", "↘", "↙"]
        arrows = {dir : arrow for dir, arrow in zip(dirs, arrows)}
        return arrows[gravity] * self.dim * 2


    def follow(self, gravity):
        follow_states = []
        for board in [self.top, self.bottom]:
            something, follow_state = board.follow(gravity)
            follow_states.append(follow_state)
        return self, follow_states

    def __str__(self):
        resp = [str(board) for board in [self.top, self.bottom]]
        return ("\n" + "#" * self.dim * 2 + "\n").join(resp)

    def __repr__(self):
        points = [board.points for board in [self.top, self.bottom]]
        string = f"Hourglass({self.dim}, points = {points})"
        return string

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
            return
        # Sample one of the top points, where the sum is smallest
        sums = [sum(p) for p in top.points]
        index = sums.index(min(sums))
        poi = top.points[index]
        # remove that point from the top board and insert it in the bottom board
        top.points.remove(poi)
        bottom.points.insert(0, (0,0))
        return



if __name__ == "__main__":
    # from math import ceil
    from random import randint
    def demo(screen):
        dim = 8
        p1 = [(x, y) for x in range(dim) for y in range(dim)][1:]
        p2 = [(0,0)]
        hourglass = Hourglass(dim, p1 = p1, p2 = p2)
        dirs = ["U", "D", "L", "R", "UL", "UR", "DR", "DL"]
        try:
            last_update = None
            update_time = time.time()
            while True:
                # update in increments of .2 seconds
                if time.time() < update_time + .4:
                    continue
                screen.refresh()
                # update gravity for the hourglass
                # gravity = random.choice(dirs)
                gravity = "DR"
                # screen.print_at(hourglass.update_gravity(gravity), 0, 0)
                # check if any point can follow
                glass, follow_states = hourglass.follow(gravity)
                for i, line in enumerate(str(hourglass).split("\n")):
                    screen.print_at(line, 0, i)
                # if any point can follow, we are in the follow state
                if any(follow_states):
                    last_update = None
                    # there was a follow, no sand will be dropped
                    continue

                # sand can only be dropped when the board is upside down
                if gravity not in ["UL", "DR"]:
                    continue

                # there wasn't a follow => drop state
                if not last_update:
                    last_update = time.time()
                    continue

                # only drop sand in half a second increments
                if time.time() < last_update + 1:
                    continue
                hourglass.drop_sand()


        except KeyboardInterrupt:
            print("Loop was stopped")
            pass


    Screen.wrapper(demo)




