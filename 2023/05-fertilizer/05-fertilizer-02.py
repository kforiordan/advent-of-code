#!/usr/bin/env python3

import re
import sys

def get_seeds_and_maps(fh):
    seeds = []
    maps = {}

    for line in fh:
        line.strip()
        junk,seeds_text = line.split(':')
        seeds = list(map(int,seeds_text.strip().split(' ')))
        break

    map_key_re = re.compile('^([a-z]+)-to-([a-z]+) map:')
    abc_re = re.compile('^([0-9]+) *([0-9]+) *([0-9]+)')

    type_src, type_dst = None, None
    obj_dst, obj_src, obj_range = None, None, None
    low, high, addition = None, None, None
    ruleset = []
    for line in fh:
        line.strip()
        m = map_key_re.match(line)
        if m:
            type_src = m.group(1)
            type_dst = m.group(2)
        else:
            m = abc_re.match(line)
            if m:
                obj_dst, obj_src, obj_range = list(map(int,[m.group(1), m.group(2), m.group(3)]))
                ruleset.append({'low':obj_src, 'high':obj_src+(obj_range-1), 'addition':obj_dst-obj_src})
            else:
                if type_src:
                    maps[type_src] = {'type_src':type_src, 'type_dst':type_dst,
                                      'rules':sorted(ruleset, key=lambda x: x['low'])}

                    type_src = None
                    ruleset = []
    if type_src:
        maps[type_src] = {'type_src':type_src, 'type_dst':type_dst,
                          'rules':sorted(ruleset, key=lambda x: x['low'])}

    return seeds, maps

if __name__ == "__main__":
    seeds, maps = get_seeds_and_maps(sys.stdin)

    translation_order = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity' ] # , 'location']
    # print("-- ")
    # print(seeds)
    # for t in translation_order:
    #     print(maps[t])

    print(maps)
    print(maps)
    i = 0
    low, high = None, None
    path = {}
    while i < len(seeds):
        low = seeds[i]
        high = low+(seeds[i+1]-1)

        print(low)
        print(high)
        for t in translation_order:
            print(t)
            print(maps[t])
            for r in maps[t]["rules"]:
                if low >= r["low"] and low <= r["high"]:
                    if high <= r["high"]:
                        print("all contained")
                    else:
                        left_low = low
                        left_high = r["high"]
                        right_low = left_high+1
                        right_high = high
            exit(0)

        i += 2

