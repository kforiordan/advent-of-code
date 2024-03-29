#!/usr/bin/env python3

import sys
import re
from collections import deque
from copy import deepcopy

# Reads diagram of stacks from fh, returns dict of crates per stack.
def get_stacks(fh):
    stacks = {}

    for line in fh:
        line = line.rstrip('\n')
        #[Z] [M] [P] <- a typical line of input.  It is left padded to
        # a uniform length, and from that length you could determine
        # the number of stacks (int((length+1)/4) but I'm going to
        # ignore that because I hate the idea of relying on
        # whitespace, especially copy&pasted whitespace.
        crates = get_crates(line)
        for s, c in crates.items():
            if s in stacks:
                stacks[s].appendleft(c)
            else:
                stacks[s] = deque(c)
        if line == "":
            break

    return stacks


# Returns stack-indexed dict of crates found on given line
def get_crates(line):
    crates = {}

    item_re = re.compile('\[([A-Z])\]')
    char_idx = 0
    stack_idx = 1
    while char_idx < len(line):
        line = line.rstrip(' \n')
        stack = line[char_idx:char_idx+3]
        m = item_re.search(stack)
        if m:
            crates[str(stack_idx)] = m.group(1)
        stack_idx += 1
        char_idx += 4	# 3 chars for crate, 1 for delimiting space.

    return crates


# From fh, reads and parses move instructions
def get_moves(fh):
    moves = []

    move_re = re.compile('^move ([0-9]+) from (\S+) to (\S+)$')
    for line in fh:
        line = line.rstrip('\n')
        m = move_re.search(line)
        if m:
            moves.append({"n":int(m.group(1)), "from":m.group(2), "to":m.group(3)})

    return moves


def apply_moves(stack, moves, move_function=None):
    if move_function == None:
        move_function = apply_move_9000
    for move in moves:
        move_function(stack, move)
    return stack


def apply_move_9000(stack, move):
    if move["n"] == 0:
        return stack
    else:
        c = stack[move["from"]].pop()	# pop the 'from' stack
        stack[move["to"]].append(c)	# push it onto the 'to' stack
        move["n"] -= 1
        return apply_move_9000(stack, move)


# I probably should have just used list slices and .extend(), but here
# we are.
def apply_move_9001(stack, move, crane=None):
    if move["n"] == 0:
        if len(crane) == 0:
            return stack
        else:
            c = crane.pop()		# pop crate from the crane and
            stack[move["to"]].append(c)	# push it onto the 'to' stack
            return apply_move_9001(stack, move, crane)
    else:
        c = stack[move["from"]].pop()	# pop the 'from' stack
        if crane == None:
            crane = []
        crane.append(c)			# push this crate to the crane
        move["n"] -= 1
        return apply_move_9001(stack, move, crane)


if __name__ == "__main__":

    stacks = get_stacks(sys.stdin)
    moves = get_moves(sys.stdin)

    silver_stacks = apply_moves(deepcopy(stacks), deepcopy(moves))
    silver = "".join([silver_stacks[k][-1] for k in sorted(silver_stacks)])

    gold_stacks = apply_moves(stacks, moves, apply_move_9001)
    gold = "".join([gold_stacks[k][-1] for k in sorted(gold_stacks)])

    print(f'Silver: {silver}')
    print(f'Gold: {gold}')
