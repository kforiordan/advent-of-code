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
                rule = {'low': b, 'high': b+(c-1), 'addition': a-b}
                these_rules.append(rule)
            else:
                if mapping_id != None:
                    maps[mapping_id] = these_rules
                    these_rules = []
    maps[mapping_id] = these_rules

    return list(seeds), maps

if __name__ == "__main__":
    seeds, maps = get_seeds_and_maps(sys.stdin)

    def seed2soil(x):
        for rule in maps["seed->soil"]:
            if x >= rule["low"] and x <= rule["high"]:
                return x + rule["addition"]
        return x
    def soil2fertilizer(x):
        for rule in maps["soil->fertilizer"]:
            if x >= rule["low"] and x <= rule["high"]:
                return x + rule["addition"]
        return x
    def fertilizer2water(x):
        for rule in maps["fertilizer->water"]:
            if x >= rule["low"] and x <= rule["high"]:
                return x + rule["addition"]
        return x
    def water2light(x):
        for rule in maps["water->light"]:
            if x >= rule["low"] and x <= rule["high"]:
                return x + rule["addition"]
        return x
    def light2temperature(x):
        for rule in maps["light->temperature"]:
            if x >= rule["low"] and x <= rule["high"]:
                return x + rule["addition"]
        return x
    def temperature2humidity(x):
        for rule in maps["temperature->humidity"]:
            if x >= rule["low"] and x <= rule["high"]:
                return x + rule["addition"]
        return x
    def humidity2location(x):
        for rule in maps["humidity->location"]:
            if x >= rule["low"] and x <= rule["high"]:
                return x + rule["addition"]
        return x
    def seed2location(x):
        return humidity2location(temperature2humidity(light2temperature(water2light(fertilizer2water(soil2fertilizer(seed2soil(x)))))))

    locations = list(map(seed2location, seeds))
    print("Silver: {}".format(min(locations)))
