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
            result = int(f(left) / f(right))
        elif op == "=":
            result = f(left) == f(right)

    return result


if __name__ == "__main__":
    monkeys = get_monkeys(sys.stdin)

    print("Silver: {}".format(monkey_math(monkeys, "root")))

    high = 1000000000000000000
    low = -1000000000000000000

    right_result = monkey_math(monkeys, monkeys["root"]["right"])
    print("right: {}".format(right_result))
    i = 0
    while True:
        monkeys["humn"] = {"number":high}
        print("Guessing left high={}".format(high))
        highleft = monkey_math(monkeys, monkeys["root"]["left"])

        monkeys["humn"] = {"number":low}
        print("Guessing left low={}".format(low))
        lowleft = monkey_math(monkeys, monkeys["root"]["left"])

        if highleft == right_result or lowleft == right_result:
            print("hallelujah {} high={}, high guess={}, low={}, low guess={}".format(i, high, highleft, low, lowleft))
            break
        if abs(highleft - right_result) >= abs(lowleft - right_result):
            high = int((high + low)/2)
        else:
            low = int((high + low)/2)

        if i > 2000:
            break
        i += 1


    monkeys["humn"] = {"number":3509819803067}
    print(monkey_math(monkeys, monkeys["root"]["left"]))
    print(monkey_math(monkeys, monkeys["root"]["right"]))

#    print("Gold: {}".format("lol"))
#    monkeys["humn"] = "XYZZY"
