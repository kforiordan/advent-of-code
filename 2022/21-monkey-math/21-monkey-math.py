#!/usr/bin/env python

import sys
import re

def get_monkeys(fh):
    monkeys = {}
    number_re = re.compile('([0-9]+)')
    op_re = re.compile('([a-z]+) ([^ a-z]+) *([a-z]+)')
    for line in fh:
        line = line.strip()
        monkey, yells = line.split(": ")
        m = number_re.match(yells)
        if m:
            monkeys[monkey] = {"number":int(m.group(1))}
        else:
            m = op_re.match(yells)
            if m:
                monkeys[monkey] = {"op":m.group(2), "left":m.group(1), "right":m.group(3)}

    return monkeys


def monkey_math(monkeys, monkey):
    result = None
    m = monkeys[monkey]
    if "number" in m:
        result = m["number"]
    else:
        f = lambda x: monkey_math(monkeys, x)
        (op, left, right) = (m["op"], m["left"], m["right"])
        if op == "+":
            result = f(left) + f(right)
        elif op == "-":
            result = f(left) - f(right)
        elif op == "*":
            result = f(left) * f(right)
        elif op == "/":
            result = f(left) / f(right)
    return int(result)


if __name__ == "__main__":
    monkeys = get_monkeys(sys.stdin)
    print(monkey_math(monkeys, "root"))
