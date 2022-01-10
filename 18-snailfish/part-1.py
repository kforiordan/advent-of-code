import sys
import copy
import pprint
from functools import reduce


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

def sn_add_only(a:str, b:str):
    return "[{},{}]".format(a,b)


def sn_add(a:str, b:str):
    return(reduce(sn_add_only(a,b)))


def sn_explode():
    return []


def sn_split_number(n):
    # >>> round(11/2)
    # 6
    # >>> round(9/2)
    # 4
    #
    # Ok.
    #
    return("[{},{}]".format(round((n-0.25)/2), round((n+0.25)/2)))


# Takes a
def sn_explode_leftward(s:str, x:int) -> str:
    return("EL")
    new_left = []
    n = None
    just_sail_on_through = False
    for i,c in enumerate(reversed(s)):
        if just_sail_on_through:
            new_left.append(c)
        else:
            if c in '0123456789':
                if n == None:
                    n = int(c)
                else:
                    n = (n * 10) + int(c)
            else:
                if n == None:
                    new_left.append(c)
                else:
                    new_left.append(str(x + n))
                    new_left.append(c)
                    just_sail_on_through = True
    return(''.join(reversed(new_left)))


def sn_explode_rightward(s, x):
    return("ER")


def sn_explode_or_split(s):

    # Thresholds for when to explode or split.
    explosion_threshold = 4
    split_threshold = 10

    # For tracking whether we should explode or not
    depth = 0

    # For tracking numbers as encountered - split may be needed
    n = None

    # As we move from left to right through the string, we copy stuff leftwards
    left = []
    subj = []
    right = []

    def is_number(l):
        return(len(l) > 0 and
               reduce(lambda x, y: x and y,
                      map(lambda c: c in '0123456789', l),
                      True))

    def list2num(l):
        n = 0
        for i,x in enumerate(reversed(l)):
            n += int(x) * int((10**i))
        return n

    # After a split or explode we just copy everything from right to left.
    just_sail_on_through = False

    for i,c in enumerate(list(s)):
        if c == '[':
            depth += 1
            if depth > explosion_threshold:
                subj.append(c)
            else:
                left.append(c)
        elif c == ',':
            if depth > explosion_threshold:
                subj.append(c)
            else:
                if is_number(subj):
                    if list2num(subj) > split_threshold:
                        subj = sn_split_number(list2num(subj))
                        right = s[i:]
                        break
                    else:
                        left.extend(subj)
                        left.append(c)
                        subj = []
                else:
                    left.append(c)
        elif c == ']':
            if depth > explosion_threshold:
                subj.append(c)
            else:
                if is_number(subj):
                    if list2num(subj) > split_threshold:
                        left.append(c)
                        subj = sn_split_number(subj)
                        right = s[i+1:]
                        break
                    else:
                        left.extend(subj)
                        left.append(c)
                        subj = []
                else:
                    left.append(c)
            depth -= 1
        elif c in '0123456789':
            subj.append(c)

    print("L:{};  S:{};  R:{};".format(*map(lambda x: ''.join(x), [left, subj, right])))
    return ''.join(map(lambda x: ''.join(x), [left, subj, right]))


def sn_reduce(s):
    r = s
    prev = None
    while True:
        prev = r
        r = sn_explode_or_split(r)
        if r == prev:
            break
    return(r)


def trivial_tests():

    # Could be a lambda value for the 'function' key, but we get a
    # better function name this way.
    def tt_add11(x):
        sn_add_only(x, '[1,1]')

    tests = [
        {
            'input': '[[[[0,7],4],[15,[0,13]]],[1,1]]',
            'function': sn_explode_or_split,
            'expected_output': '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
        },
        {
            'input': '[[[[[9,8],1],2],3],4]',
            'function': sn_explode_or_split,
            'expected_output': '[[[[0,9],2],3],4]'
        },
        {
            'input': '[[[[4,3],4],4],[7,[[8,4],9]]]',
            'function': tt_add11,
            'expected_output': '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
        }
    ]

    n_passed = 0
    result_strings = ["failed", "passed"]
    for i,t in enumerate(tests):
        actual_output = t['function'](t['input'])
        result = actual_output == t['expected_output']
        print("Test {} {}".format(i, result_strings[int(result)]))
        if not result:
            print(" Function: {}".format(t['function']))
            print("      for: {}".format(t['input']))
            print("   wanted: {}".format(t['expected_output']))
            print("  but got: {}".format(actual_output))
        n_passed += result

    if n_passed == len(tests):
        print("All {} trivial tests passed!".format(n_passed))
    else:
        print("Passed {} out of {} tests :-(".format(n_passed, len(tests)))

    return n_passed == len(tests)


if __name__ == "__main__":

    pp = pprint.PrettyPrinter()
    trivial_tests()
