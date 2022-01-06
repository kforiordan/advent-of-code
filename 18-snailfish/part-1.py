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

# Trees be damned, what if I treated this as a mostly textual problem?

def add(a:str, b:str):
    return "[{},{}]".format(a,b)


def explode():

    return []


def split_number(n):
    # >>> round(11/2)
    # 6
    # >>> round(9/2)
    # 4
    #
    # Ok.
    #
    return("[{},{}]".format(round((n-0.25)/2), round((n+0.25)/2)))

def split(s):

    n = None
    left = []
    right = list(s)
    just_sail_on_through = False

    for i,c in enumerate(right):
        if just_sail_on_through:
            left.append(c)
        else:
            if c in '[],':
                if n != None:	# if n is a number
                    if n < 10:
                        left.append(str(n))
                    elif n >= 10:
                        left.append(str(split_number(n)))
                        just_sail_on_through = True	# No further processing
                    n = None
                left.append(c)
            elif c in '0123456789':
                if n == None:
                    n = int(c)
                else:
                    n = (n * 10) + int(c)

    return ''.join(left)


def reduce(s):
    i = 0
    r = s
    while True:
        r = explode(r)
        if r == s:
            r = split(r)
            if r == s:
                break
    return r



if __name__ == "__main__":
    a = '[[[[0,7],4],[15,[0,13]]],[1,1]]'
    a_bis = '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'

    print(split(a))
    print(a_bis)
