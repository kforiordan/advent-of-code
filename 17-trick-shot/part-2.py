import sys
import pprint

def step(position, velocity):
    (pos_x, pos_y) = position
    (vel_x, vel_y) = velocity

    # 1. increase x pos by x velocity:
    pos_x += vel_x

    # 2. increase y pos by y velocity:
    pos_y += vel_y

    # 3. Due to drag, x tends 1 towards 0
    if vel_x > 0:
        vel_x -= 1

    # 4. Due to gravity, y velocity decreases by 1
    vel_y -= 1

    return ((pos_x, pos_y), (vel_x, vel_y))


def lost(pos, velocity, target_area):
    (pos_x, pos_y) = pos
    (vel_x, vel_y) = velocity
    (xs, ys) = target_area

    # FIXME: Not sure this is correct.  Think about this later.
    if pos_x > max(xs) or pos_y < min(ys):
        return True

    return False


def within_area(pos, target_area):
    (pos_x, pos_y) = pos
    (xs, ys) = target_area
    return pos_x <= max(xs) and pos_x >= min(xs) and \
        pos_y <= max(ys) and pos_y >= min(ys)


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    initial_pos = (0,0)

    test_target_area = ([20,30],[-10,-5])
    test_target_area = ([94,151],[-156,-103])
