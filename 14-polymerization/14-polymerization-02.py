import sys
import pprint
from collections import defaultdict
import itertools

def get_template(fh):
    template = []

    for line in fh:
        if len(template) > 0:
            # This is so stupid.  I should learn how to read a single
            # line from a filehandle - as soon as I finish the puzzles
            # I'm already behind schedule on!
            break
        template = list(line.strip())

    return template


def get_pair_insertion_rules(fh):
    rules = {}

    for line in fh:
        a, junk, b = line.strip().split()
        rules[a] = b

    return rules


def apply_rule(rules, s):
    if s in rules:
        l = ''.join([s[0],rules[s]])
        r = ''.join([rules[s],s[1]])
        return([l,r])
    else:
        return([s])


def step(rules, pair_counts):

    counts_this_step = defaultdict(int)
    for p in pair_counts:
        if p in rules:
            if pair_counts[p] > 0:
                counts_this_step[p] -= pair_counts[p]
                for (pa,pb) in pairwise(apply_rule(rules,p)):
                    counts_this_step[pa] += pair_counts[p]
                    counts_this_step[pb] += pair_counts[p]

    for p in counts_this_step:
        pair_counts[p] += counts_this_step[p]


# This was just used for data exploration, ignore.
def get_all_elements(rules, template):
    elements = set(''.join(
        map(lambda s: ''.join(s),
            [rules.keys(), rules.values(), template])))
    return elements


# pairwise is missing from python 3.9, but the documentation suggests
# this implementation:
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=False)
    template = get_template(sys.stdin)
    rules = get_pair_insertion_rules(sys.stdin)

    pair_counts = defaultdict(int)
    for p in pairwise(template):
        pair_counts[''.join(p)] += 1

    for i in range(0,40):
        step(rules, pair_counts)

    char_counts = defaultdict(int)
    for p in pair_counts:
        (c1,c2) = tuple(p)
        char_counts[c1] += pair_counts[p]
        char_counts[c2] += pair_counts[p]

    for p in char_counts:
        char_counts[p] = int(round((char_counts[p] / 2) + 0.1))

    min_freq = min(char_counts.values())
    max_freq = max(char_counts.values())
    solution = max_freq - min_freq
    print(solution)





