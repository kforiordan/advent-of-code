#!/usr/bin/env python3

import sys
import re


class Valve:
    def __init__(self, desc):
        # Sample input: Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        valve_re = re.compile('^Valve ([a-zA-Z]+) has flow rate=([0-9]+); tunnel.? lead.? to valve.? (.*)$')
        m = valve_re.match(desc)
        if (m):
            self.id = m.group(1)
            self.flow_rate = int(m.group(2))
            self.tunnels = m.group(3).split(', ')
            self.is_open = False

    def __repr__(self):
        return "Valve(id={}, flow_rate={}, tunnels={})".format(
            self.id, self.flow_rate, ",".join(sorted(self.tunnels)))


def get_valves(fh):
    graph = {}

    for line in fh:
        valve = Valve(line.rstrip('\n'))
        graph[valve.id] = valve

    for k,v in graph.items():
        for tunnel in t.
    return graph


if __name__ == "__main__":
    graph = get_valves(sys.stdin)

    flow_rate = 0
    open_valves = []
    total_flow = 0
    time_remaining = 30

    # "You start at valve AA"
    pos = "AA"

