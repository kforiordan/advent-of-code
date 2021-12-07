
import sys
import pprint


def get_lanternfish(fh):
    fish = []

    for line in fh:
        line = line.strip()
        if len(line) == 0:
            continue
        elif len(fish) == 0:
            fish = list(map(int,line.split(',')))

    return fish


def lanternfish_census(lanternfish):
    magic_max_cycle_number = 8
    census = [0 for x in range(magic_max_cycle_number + 1)]

    for f in lanternfish:
        census[f] += 1

    return census


def count_fish(census):
    return sum(census)


def day(census):
    new_census = lanternfish_census([])
    magic_spawn_number = 8
    magic_new_cycle_number = 6
    spawners = 0

    for i in range(len(census)):
        if i == 0:
            spawners = census[i]
            new_census[i] = 0
        else:
            new_census[i-1] = census[i]
            new_census[i] = 0

    new_census[magic_spawn_number] = spawners
    new_census[magic_new_cycle_number] += spawners

    return new_census


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=True)

    lanternfish = get_lanternfish(sys.stdin)
    census = lanternfish_census(lanternfish)

    n_days = 256
    i = 0
    while i < n_days:
        census = day(census)
        i = i + 1

    print("After day {} count is {}".format(i, count_fish(census)))
