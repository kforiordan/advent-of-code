import sys
import copy
import pprint


# "... every snailfish number is a pair - an ordered list of two
# elements. Each element of the pair can be either a regular number or
# another pair. ... Pairs are written as [x,y], where x and y are the
# elements within the pair."
#
# "To add two snailfish numbers, form a pair from the left and right
# parameters of the addition operator. For example, [1,2] + [[3,4],5]
# becomes [[1,2],[[3,4],5]]."
#
# "... snailfish numbers must always be reduced ..."
#
# "To reduce a snailfish number, you must repeatedly do the first
# action in this list that applies to the snailfish number:
#
#    If any pair is nested inside four pairs, the leftmost such pair explodes.
#
#    If any regular number is 10 or greater, the leftmost such regular
#    number splits."
#
# "During reduction, at most one action applies, after which the
# process returns to the top of the list of actions. For example, if
# split produces a pair that meets the explode criteria, that pair
# explodes before other splits occur."
#
# "To explode a pair, the pair's left value is added to the first
# regular number to the left of the exploding pair (if any), and the
# pair's right value is added to the first regular number to the right
# of the exploding pair (if any). Exploding pairs will always consist
# of two regular numbers. Then, the entire exploding pair is replaced
# with the regular number 0."
#
# "To split a regular number, replace it with a pair; the left element
# of the pair should be the regular number divided by two and rounded
# down, while the right element of the pair should be the regular
# number divided by two and rounded up."

# class SnailNumber():
#     # I don't think I can do this in python, and sure what do types
#     # even matter to python.
#     #
#     # val: int or SnailNumber

#     def __init__(self, a, b=None):
#         if b == None:
#             if isinstance(a, SnailNumber):
#                 self.val = copy.deepcopy(a)
#             else:
#                 # I'm assuming an int here.
#                 self.val = a

#     def add(self, a):
#         return([copy.deepcopy(self.val), a])

#     def split(


def add(a, b):
    return [a,b]


def explode(l):
    # Oh no, I need BFS, I think.
    return []


def split(n):
    # >>> round(11/2)
    # 6
    # >>> round(9/2)
    # 4
    #
    # Ok.
    #
    return([round((n-0.25)/2),round((n+0.25)/2)])



if __name__ == "__main__":
    
