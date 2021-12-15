import sys
import pprint


def get_map(fh):
    return [list(line.strip()) for line in fh]


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()

    map = get_map(sys.stdin)
