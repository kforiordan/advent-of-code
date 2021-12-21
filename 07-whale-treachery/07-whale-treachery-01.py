
import sys
import pprint

def get_positions(fh):
    positions = []

    for line in fh:
        line = line.strip()
        if len(line) == 0:
            continue
        elif len(positions) == 0:
            positions = list(map(int,line.split(',')))

    return positions


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=True)
    positions = get_positions(sys.stdin)

    optimal_position = -1
    cost = -1
    for c in range(min(positions), max(positions)+1):
        p = sum(list(map(lambda x: abs(x - c), positions)))
        if cost == -1 or p < cost:
            cost = p
            optimal_position = c

    print(f'Optimal position = {optimal_position}')
    print(f'Cost = {cost}')
