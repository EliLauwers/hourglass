import time
from Hourglass import Hourglass

def create_some_points(dim):
    p1 = []
    p2 = []
    for x in range(dim):
        for y in range(dim):
            point = (x, y)
            if sum(point) < dim / 2 - 1:
                p1.append(point)
                p2.append(point)
    return p1, p2


if __name__ == "__main__":
    dim = 8
    p1, p2 = create_some_points(dim)
    hourglass = Hourglass(dim, p1 = p1, p2 = p2)
    dirs = ["U", "D", "L", "R", "UL", "UR", "DR", "DL"]
    try:
        counter = 0
        wait = .05
        drop_wait = hourglass.dim
        gravity = "DR"
        while True:
            counter += 1
            # update in increments of .2 seconds
            time.sleep(wait)
            print(hourglass)
            # update gravity for the hourglass
            gravity = gravity
            # check if any point can follow
            glass, follow_states = hourglass.follow(gravity)
            # if any point can follow, we are in the follow state
            counter = 0 if any(follow_states) else counter
            # sand can only be dropped when the board has the right gravity directions
            if gravity not in ["UL", "DR"]:
                continue
            # only drop sand when there are a number of empty drop waits
            if counter < drop_wait:
                continue
            # drop sand
            glass, drop_state = hourglass.drop_sand()
            counter = 0 if drop_state else counter
            # only switch gravity when no points can follow and no sand can drop
            if counter < (2 * drop_wait):
                continue
            # change gravity to other direction
            gravity = "UL"
            hourglass.update_gravity(gravity)

    except KeyboardInterrupt:
        print("Loop was stopped")
        pass






