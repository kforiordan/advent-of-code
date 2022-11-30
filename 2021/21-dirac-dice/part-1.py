import sys
import pprint

def get_starting_positions(fh):
    # Sorry not sorry
    return [int(line.strip().split(' ')[4]) - 1 for line in fh]


def roll(dirac_counter, n):
    rolls = []
    for i in range(0, n):
        rolls.append((dirac_counter % 100) + 1)
        dirac_counter += 1
    return(dirac_counter, sum(rolls))


def move(pos, hops):
    return ((pos + hops) % 10) + 1


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=False)
    scores = [0, 0]

    positions = get_starting_positions(sys.stdin)

    dirac_counter = 0
    j=0
    solution=None
    while solution == None:
        for i,p in enumerate(positions):
            dirac_counter, hops = roll(dirac_counter, 3)
            score = move(p, hops)
            scores[i] += score
            positions[i] = score - 1
            #print("Iteration {}:  player {} -> score {}".format(j, i, scores[i]))
            j += 1
            if max(scores) >= 1000:
                #print("counter: {}, loser: {}".format(dirac_counter, min(scores)))
                solution = dirac_counter * min(scores)
                break
    print("Solution: {}".format(solution))
