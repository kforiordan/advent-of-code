import sys
import pprint

def step(position, velocity):
    (pos_x, pos_y) = position
    (v_x, v_y) = velocity

    # 1. increase x pos by x velocity:
    pos_x += v_x

    # 2. increase y pos by y velocity:
    pos_y += v_y

    # 3. Due to drag, x tends 1 towards 0
    if v_x > 0:
        v_x -= 1

    # 4. Due to gravity, y velocity decreases by 1
    v_y -= 1

    return ((pos_x, pos_y), (v_x, v_y))


def lost(pos, velocity, target_area):
    (pos_x, pos_y) = pos
    (v_x, v_y) = velocity
    (xs, ys) = target_area

    # We could tighten these bounds a lot more.
    if pos_x > max(xs):
        return True
    if pos_y < min(ys):
        return True

    return False


def within_area(pos, target_area):
    (pos_x, pos_y) = pos
    (xs, ys) = target_area
    return pos_x <= max(xs) and pos_x >= min(xs) and \
        pos_y <= max(ys) and pos_y >= min(ys)


def still_going(pos, velocity, target_area):
    if within_area(pos, target_area):
        return False
    elif lost(pos, velocity, target_area):
        return False
    else:
        return True


def try_velocity(initial_position, velocity, target_area):

    tmp_v = velocity
    position = initial_position
    high_y = position[1]
    while not lost(position, tmp_v, target_area) and \
          not within_area(position, target_area):
        #print("Trying {} -> {}".format(velocity, tmp_v))
        position, tmp_v = step(position, tmp_v)
        if position[1] > high_y:
            #print("      New high: {} (was {})".format(position[1], high_y))
            high_y = position[1]

    if within_area(position, target_area):
        return high_y
    else:
        return None



if __name__ == "__main__":
    pp = pprint.PrettyPrinter()
    initial_pos = (0,0)
    #target_area = ([20,30],[-10,-5])
    target_area = ([94,151],[-156,-103])

    ultimate_highest_y = initial_pos[1]
    ultimate_highest_v = initial_pos[1]
    for initial_y in range(0, 1000):		# LOLOLOLOLLOLOLOLOOOLOLL
        highest_y = initial_pos[1]
        highest_v = initial_pos[1]
        #initial_y = initial_pos[1]
        for v_x in range(0,target_area[0][1]):
            pos = initial_pos
            v_y = initial_y
            v = (v_x, v_y)
            high_y = try_velocity(pos, v, target_area)
            if high_y != None and high_y > highest_y:
                highest_y = high_y
                highest_v = v
        if highest_y > ultimate_highest_y:
            ultimate_highest_y = highest_y
            ultimate_highest_v = highest_v

    print("Highest y was {} with velocity {}".format(
        ultimate_highest_y, ultimate_highest_v))
