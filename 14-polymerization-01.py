import sys
import pprint

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


def step(rules, elements):
    result = []

    prev_e = None
    for e in elements:
        if prev_e == None:
            prev_e = e
        else:
            result.append(prev_e)
            s = ''.join([prev_e, e])
            if s in rules:
                result.append(rules[s])
            prev_e = e
    result.append(e)

    return result


def count_chars(s):
    freq = {}
    for c in s:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
    return freq

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=True)
    template = get_template(sys.stdin)
    rules = get_pair_insertion_rules(sys.stdin)

    t = template
    for i in range(0,10):
        t = step(rules, t)

    char_freqs = count_chars(t)
    min_freq = min(char_freqs.values())
    max_freq = max(char_freqs.values())

    solution = max_freq - min_freq
    print(solution)
