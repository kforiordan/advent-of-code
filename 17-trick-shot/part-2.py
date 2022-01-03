import sys
import pprint

def step(position, velocity):
    (pos_x, pos_y) = position
    (vel_x, vel_y) = velocity

    # 1. increase x pos by x velocity:
    pos_x += vel_x

    # 2. increase y pos by y velocity:
    pos_y += vel_y

    # 3. Due to drag, x velocity tends towards 0
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


def launch(initial_pos, initial_vel, target):
    final_state = None

    pos = initial_pos
    vel = initial_vel
    positions = [initial_pos]
    while final_state == None:
        if within_area(pos, target):
            final_state = True
        elif lost(pos, vel, target):
            final_state = False
        else:
            pos, vel = step(pos, vel)
            positions.append(pos)

    return final_state, positions


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    initial_pos = (0,0)

    test_target_area = ([20,30],[-10,-5])
    prod_target_area = ([94,151],[-156,-103])

    target_area = prod_target_area

    good_velocities = []
    low_x  = min([initial_pos[0],min(target_area[0])])
    high_x = max(target_area[0])
    low_y  = min(target_area[1])
    high_y = 1000	# This is shameful.
    for y in range(low_y, high_y + 1):
        for x in range(low_x, high_x + 1):
            state, positions = launch(initial_pos, (x, y), target_area)
            if state == True:
                good_velocities.append((x,y))

    print(len(good_velocities))
