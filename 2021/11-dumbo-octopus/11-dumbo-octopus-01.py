
import sys
import pprint


def get_octopodes(fh):
    return [list(map(int,list(line.strip()))) for line in fh]


def incr_all(octopodes):
    for y in range(0,len(octopodes)):
        for x in range(0,len(octopodes[y])):
            octopodes[y][x] += 1


def deplete_flashers(octopodes, flashed):
    for y in range(0,len(octopodes)):
        for x in range(0,len(octopodes[y])):
            if flashed[y][x]:
                octopodes[y][x] = 0


def adjacent_points(octopodes, x, y):
    (min_y, max_y) = 0, len(octopodes) - 1
    (min_x, max_x) = 0, len(octopodes[0]) - 1

    pm = lambda a: [a-1, a, a+1]
    y_bound = lambda a: a >= min_y and a <= max_y
    x_bound = lambda a: a >= min_x and a <= max_x

    adjacent_points = [ (x2,y2) for y2 in pm(y) if 1 for x2 in pm(x) \
                        if (x2,y2) != (x,y) and y_bound(y2) and x_bound(x2)]

    return adjacent_points


def incr_adjacent(octopodes, x, y):
    for (x2, y2) in adjacent_points(octopodes, x, y):
        octopodes[y2][x2] += 1


def flash_flashers(octopodes, flashed, flash_threshold):
    flash_count = 0

    for y in range(0,len(octopodes)):
        for x in range(0,len(octopodes[y])):
            if octopodes[y][x] > flash_threshold:
                if flashed[y][x] == False:
                    flash_count += 1
                    incr_adjacent(octopodes, x, y)
                    flashed[y][x] = True

    return flash_count


def step(octopodes, flash_threshold):

    # We'll use this to track which octopodes flashed in this step.
    flashed = []
    for y in range(0,len(octopodes)):
        flashed.append([False for x in range(0,len(octopodes[y]))])

    # First, the energy level of each octopus increases by 1.
    incr_all(octopodes)

    # Then, any octopus with an energy level greater than 9 flashes.
    flash_count = flash_flashers(octopodes, flashed, flash_threshold)
    total_flash_count = flash_count
    while flash_count > 0:
        flash_count = flash_flashers(octopodes, flashed, flash_threshold)
        total_flash_count += flash_count

    # Finally, any octopus that flashed during this step has its energy
    # level set to 0
    deplete_flashers(octopodes, flashed)

    return total_flash_count


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=False)

    magic_flash_threshold = 9
    octopodes = get_octopodes(sys.stdin)

    pp.pprint(octopodes)

    total_flash_count = 0
    for i in range(1, 101):
        flash_count_this_step = step(octopodes, magic_flash_threshold)
        total_flash_count += flash_count_this_step
        print("Step: {};  Flashes: {};  Total Flashes: {}".format(
            i, flash_count_this_step, total_flash_count))
