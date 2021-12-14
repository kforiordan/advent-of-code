import sys
import pprint

def get_template(fh):
    template = []
    for line in fh:
        if len(template) > 0:
            break
        template = line.strip()

    return template

def get_pair_insertion_rules(fh):
    rules = {}

    for line in fh:
        a, junk, b = line.strip().split()
        rules[a] = b

    return rules


if __name__ == "__main__":
    template = get_template(sys.stdin)
    rules = get_pair_insertion_rules(sys.stdin)
