#!/usr/bin/env python3

import sys
from collections import deque
from copy import deepcopy
from functools import reduce

class Monkey:
    _monkey_str = "Monkey"
    _items_str = "  Starting items: "
    _op_str = "  Operation: new = old "
    _test_str = "  Test: divisible by "
    _ift_str = "    If true: throw to monkey "
    _iff_str = "    If false: throw to monkey "

    def __init__(self, desc=None):
        monkeys = None
        for line in desc:
            if line[0:len(self._monkey_str)] == self._monkey_str:
                self.idx = int(line[len(self._monkey_str):].rstrip(':'))
            elif line[0:len(self._items_str)] == self._items_str:
                self.items = deque(map(int, line[len(self._items_str):].split(', ')))
            elif line[0:len(self._op_str)] == self._op_str:
                self.operation = line[len(self._op_str):].split(' ')
            elif line[0:len(self._test_str)] == self._test_str:
                self.test = int(line[len(self._test_str):])
            elif line[0:len(self._ift_str)] == self._ift_str:
                self.if_true = int(line[len(self._ift_str):])
            elif line[0:len(self._iff_str)] == self._iff_str:
                self.if_false = int(line[len(self._iff_str):])
        self.inspection_count = 0
        self.allow_relief = True

    def relieve(self, item):
        # "... our relief that the monkey's inspection didn't damage
        # the item causes your worry level to be divided by three and
        # rounded down to the nearest integer"
        return int(item/3)

    def apply_operation(self, item):
        op, arg = self.operation
        if arg == 'old':
            arg = item
        else:
            arg = int(arg)
        if op == '+':
            item += arg
        elif op == '*':
            item *= arg
        return item

    def apply_test(self, item):
        return item % self.test == 0

    def throw_item(self, item, target):
        self.monkeys[target].items.append(item)

    def inspect_all(self):
        while len(self.items) > 0:
            self.inspect()

    def inspect(self):
        item = self.items.popleft()

        # Increase worry level according to self.operation
        item = self.apply_operation(item)

        if self.allow_relief:
            item = self.relieve(item)
        else:
            if item > max_worry:
                item = item % max_worry

        if self.apply_test(item):
            self.throw_item(item, self.if_true)
        else:
            self.throw_item(item, self.if_false)

        self.inspection_count += 1


    def __repr__(self):
        desc = ["Monkey {}:".format(self.idx),
                "  Items: {}".format(self.items),
                "  Operation: {}".format(self.operation),
                "  Test: {}".format(self.test),
                "    If true: {}".format(self.if_true),
                "    If false: {}".format(self.if_false),
                "  Inspection count: {}".format(self.inspection_count)]
        return "\n".join(desc)


def get_monkeys(fh):
    monkeys = []

    monkey_description = []

    for line in fh:
        line = line.rstrip('\n')
        if line == "":
            monkeys.append(Monkey(monkey_description))
            monkey_description = []
        else:
            monkey_description.append(line)
    monkeys.append(Monkey(monkey_description))

    # Now make all monkeys aware of each other:
    for monkey in monkeys:
        monkey.monkeys = monkeys # Monkeys monkeys monkeys monkeys

    return monkeys


if __name__ == "__main__":

    silver_monkeys = get_monkeys(sys.stdin)
    gold_monkeys = deepcopy(silver_monkeys)

    # Silver
    n_rounds = 20
    for round in range(1, n_rounds+1):
        for monkey in silver_monkeys:
            monkey.inspect_all()
    inspection_counts = sorted(map(lambda m: m.inspection_count, silver_monkeys))
    monkey_business = inspection_counts[-1] * inspection_counts[-2]
    print("Silver: {}".format(monkey_business))

    # Gold
    tests = []
    for monkey in gold_monkeys:
        monkey.monkeys = gold_monkeys
        monkey.allow_relief = False
        tests.append(monkey.test)

    # There was a clue in the problem spec: "Unfortunately, that
    # relief was all that was keeping your worry levels from reaching
    # ridiculous levels. You'll need to find another way to keep your
    # worry levels manageable."
    #
    # I figured it was just the massive sums that were causing
    # performance issues, so I worked out how to keep the worry level
    # to a reasonable number.
    max_worry = reduce(lambda x, y: x *  y, tests, 1)
    for monkey in gold_monkeys:
        monkey.max_worry = max_worry

    n_rounds = 10000
    for round in range(1, n_rounds+1):
        for monkey in gold_monkeys:
            monkey.inspect_all()
    inspection_counts = sorted(map(lambda m: m.inspection_count, gold_monkeys))
    monkey_business = inspection_counts[-1] * inspection_counts[-2]
    print("Gold: {}".format(monkey_business))
