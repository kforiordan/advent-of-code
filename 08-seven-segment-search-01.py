
import sys
import pprint


def count_specific(haystacks, needles):
    yorn = lambda y: list(map(lambda x: 1 if x in needles else 0, y))
    return sum(list(map(sum, list(map(yorn, haystacks)))))


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=True)
    input_signals = []
    output_signals = []

    for line in sys.stdin:
        signals = []
        signals = line.strip().split()
        input_signals.append(signals[0:10])
        output_signals.append(signals[11:15])

    segment_counts = list(map(lambda x: list(map(len,x)),output_signals))

    # I'm not documenting this.  It's in the spec.
    count_1478 = count_specific(segment_counts,[2,4,3,7])

    print(count_1478)
