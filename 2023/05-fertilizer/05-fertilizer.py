#!/usr/bin/env python3

import re
import sys

def get_seeds_and_maps(fh):
    seeds = []
    maps = {}

    for line in fh:
        line.strip()
        junk,seeds_text = line.split(':')
        seeds = map(int,seeds_text.strip().split(' '))
        break

    map_key_re = re.compile('^([a-z]+)-to-([a-z]+) map:')
    abc_re = re.compile('^([0-9]+) *([0-9]+) *([0-9]+)')
    these_rules = []
    mapping_id = None
    for line in fh:
        line.strip()
        m = map_key_re.match(line)
        if m:
            mapping_id = "{}->{}".format(m.group(1), m.group(2))
        else:
            m = abc_re.match(line)
            if m:
                a,b,c = list(map(int,[m.group(1), m.group(2), m.group(3)]))
                rule = {'low': a, 'high': a+(c-1), 'addition': b-a}
                these_rules.append(rule)
            else:
                if mapping_id != None:
                    maps[mapping_id] = these_rules
                    these_rules = []
    maps[mapping_id] = these_rules

    return seeds, maps

if __name__ == "__main__":
    seeds, maps = get_seeds_and_maps(sys.stdin)

    seed2location = lambda x: 999
    locations = map(seed2location, seeds)
    print("Silver: {}".format(min(locations)))
