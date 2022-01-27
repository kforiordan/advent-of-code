import sys
import copy
import pprint
from functools import reduce
from collections import defaultdict


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


# This is a poor check: we just count the number of brackets and
# return true if there's the same number of closing brackets as
# opening brackets; otherwise false.  It'll do.
#
def sn_is_well_formed(sn:str) -> bool:
    h = defaultdict(int)
    for c in sn:
        h[c] += 1
    if h['['] == h[']']:
        return(True)
    return(False)


# Adds a number or snailfish number (string) to another number
# (string) or snailfish number (string), returns a snailfish number
# (string).
#
def sn_add_only(a:str, b:str) -> str:
    return "[{},{}]".format(a,b)


# Performs snailfish number addition, then reduces the result.
#
def sn_add(a:str, b:str) -> str:
    result = sn_reduce(sn_add_only(a,b))
    return(result)


# Applies explode and split operations repeatedly for as long as they
# change the snailfish number.
#
def sn_reduce(sn:str) -> str:
    i = 0
    while True:
        prev = sn
        sn = sn_explode_only(sn);
        if sn == prev:
            sn = sn_split_only(sn)
            if sn == prev:
                break
        i += 1
    return sn


# Splits a number (int) into a snailfish number
#
def sn_split_number(n:int) -> str:
    # The 0.2 is just to skew the rounding so it goes our way
    return("[{},{}]".format(round((n-0.2)/2), round((n+0.2)/2)))


# Takes a snailfish number and an int, adds the int to the first digit
# found in the snailfish number, searching from end of snailfish
# number to beginning, i.e. leftwards.
#
def sn_explode_leftward(s:str, x:int) -> str:
    new_left = []
    n = []
    just_sail_on_through = False
    for i,c in enumerate(reversed(s)):
        if just_sail_on_through:
            new_left.append(c)
        else:
            if c in '0123456789':
                n.append(c)
            else:
                if n == []:
                    new_left.append(c)
                else:
                    new_left.append(str(x + list2num(list(reversed(n)))))
                    new_left.append(c)
                    n = []
                    just_sail_on_through = True
    return(''.join(reversed(new_left)))


# Like sn_explode_leftward, but from beginning to end.  Rightwards.
#
def sn_explode_rightward(s:str, x:int) -> str:
    new_right = []
    n = []
    just_sail_on_through = False
    added = False
    for i,c in enumerate(s):
        if just_sail_on_through:
            new_right.append(c)
        else:
            if c in '0123456789':
                n.append(c)
            else:
                if n:
                    added = True
                    new_right.append(str(x + list2num(n)))
                    new_right.append(c)
                    n = []
                    just_sail_on_through = True
                else:
                    new_right.append(c)

    return(''.join(new_right))


# Returns a list of numbers (ints), not digits, present in a simple
# snailfish number.  What bullshit is this?
#
def sn_numbers(l):
    numbers = []

    n = []
    for c in l:
        if c in '0123456789':
            n.append(c)
        elif c in ',]':
            numbers.append(list2num(n))
            n = []

    return(numbers)


# Returns a tuple containing the left and right parts of a snailfish
# number.  E.g. given "[a,b]", returns (a,b), regardless of whether a
# and/or b are simple numbers, snailfish numbers, whatever.
#
def sn_leftright(n:str):
    depth = 0
    left = []
    right = []
    e = left
    for c in n:
        if c == '[':
            if depth >= 1:
                e.append(c)
            depth += 1
        elif c == ',':
            if depth == 1:
                e = right
            else:
                e.append(c)
        elif c == ']':
            if depth > 1:
                e.append(c)
            depth -= 1
        elif c in '0123456789':
            e.append(c)

    return(tuple(map(lambda x: ''.join(x), [left, right])))


# Triple the left part of the snailfish number plus double the right
# part.  Recursively.
#
def sn_magnitude(sn, depth=0):
    left, right = sn_leftright(sn)

    left_magn = 0
    if sn_is_simple_number(left):
        left_magn = int(left) * 3
    else:
        left_magn = sn_magnitude(left, depth+1) * 3

    right_magn = 0
    if sn_is_simple_number(right):
        right_magn = int(right) * 2
    else:
        right_magn = sn_magnitude(right, depth+1) * 2

    return(left_magn + right_magn)


# ['3','7','9'] -> 379
def list2num(l):
    n = 0
    for i,x in enumerate(reversed(l)):
        n += int(x) * int((10**i))
    return n


# Returns true if everything in the list is a digit (string)
def sn_is_simple_number(l):
    return(len(l) > 0 and
           reduce(lambda x, y: x and y,
                  map(lambda c: c in '0123456789', l),
                  True))


def sn_explode_only(sn):
    explosion_threshold = 4
    depth = 0

    # As we move from left to right through the string, we copy stuff
    # to the target which, initially, is the left list.
    left, subj, right = [], [], []
    target = left

    for i,c in enumerate(list(sn)):
        if c == '[':
            depth += 1
            if depth > explosion_threshold:
                target = subj
            target.append(c)
        elif c == ',':
            target.append(c)
        elif c == ']':
            target.append(c)
            if depth > explosion_threshold:
                # We have reached the end of the snail number we are
                # exploding, so explode.
                left = sn_explode_leftward(left, sn_numbers(subj)[0])
                right = sn[i+1:]
                right = sn_explode_rightward(right, sn_numbers(subj)[1])
                subj = ['0']
                break
            depth -= 1
        elif c in '0123456789':
            target.append(c)

    return ''.join(map(lambda x: ''.join(x), [left, subj, right]))


def sn_split_only(sn):
    split_threshold = 10

    # As we move from left to right through the string, we copy stuff
    # first to the left list, then subj, then right; join all later.
    left, subj, right = [], [], []

    for i,c in enumerate(list(sn)):
        if c == '[':
            left.append(c)
        elif c in ',]':
            if sn_is_simple_number(subj):
                n = list2num(subj)
                if n >= split_threshold:
                    subj = sn_split_number(n)
                    right = sn[i:]
                    break
                else:
                    left.extend(subj)
                    left.append(c)
                    subj = []
            else:
                left.append(c)
        elif c in '0123456789':
            subj.append(c)

    return ''.join(map(lambda x: ''.join(x), [left, subj, right]))


def sn_sum_list(l, verbose=False):
    total = None
    for i,n in enumerate(l):
        if total == None:
            total = n
        else:
            new_total = sn_add(total, n)
            if verbose:
                print("{} + {} = {}".format(
                    *map(lambda x: ''.join(x), [total, n, new_total])))
            total = new_total

    return total


def trivial_tests(only=None, verbose=False):

    # Could use a lambda for 'function', but better name this way.
    def tt_add11(x):
        return(sn_add(x, '[1,1]'))

    tests = [
        {
            'input': ['3','7','9'],
            'function': list2num,
            'expected_output': 379,
        },
        {
            'name': "simple split",
            'input': '[[[[0,7],4],[15,[0,13]]],[1,1]]',
            'function': sn_split_only,
            'expected_output': '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
        },
        {
            'name': "simple explode",
            'input': '[[[[[9,8],1],2],3],4]',
            'function': sn_explode_only,
            'expected_output': '[[[[0,9],2],3],4]'
        },
        {
            'input': '[7,[6,[5,[4,[3,2]]]]]',
            'function': sn_explode_only,
            'expected_output': '[7,[6,[5,[7,0]]]]'
        },
        {
            'input': '[[6,[5,[4,[3,2]]]],1]',
            'function': sn_explode_only,
            'expected_output': '[[6,[5,[7,0]]],3]',
        },
        {
            'input': '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
            'function': sn_explode_only,
            'expected_output': '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]',
        },
        {
            'input': '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]',
            'function': sn_explode_only,
            'expected_output': '[[3,[2,[8,0]]],[9,[5,[7,0]]]]',
        },
        {
            'input': '[[[[4,3],4],4],[7,[[8,4],9]]]',
            'function': lambda x: sn_add(x, '[1,1]'),
            'expected_output': '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
        },
        {
            'input': ['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]', '[6,6]'],
            'function': sn_sum_list,
            'expected_output': '[[[[5,0],[7,4]],[5,5]],[6,6]]'
        },
        {
            'input': '[[1,2],[[3,4],5]]',
            'function': sn_magnitude,
            'expected_output': 143,
        },
        {
            'input': '[[[[3,0],[5,3]],[4,4]],[5,5]]',
            'function': sn_magnitude,
            'expected_output': 791,
        },
        {
            'input': '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]',
            'function': sn_magnitude,
            'expected_output': 1384,
        },
        {
            'input': '[[[[1,1],[2,2]],[3,3]],[4,4]]',
            'function': sn_magnitude,
            'expected_output': 445,
        },
        {
            'input': '[[[[5,0],[7,4]],[5,5]],[6,6]]',
            'function': sn_magnitude,
            'expected_output': 1137,
        },
        {
            'input': '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]',
            'function': sn_magnitude,
            'expected_output': 3488,
        },
        {
            'name': 'stupid',
            'input': '[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]]',
            'function': sn_reduce,
            'expected_output': '[[[[4,0],[5,4]],[[7,7],[6,0]]]]'
        },
        {
            'name': 'sn_add',
            'input': '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
            'function': lambda x: sn_add(x, '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]'),
            'expected_output': '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]',
        },
        {
            'name': 'first sum list test',
            'input': [
                '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
                '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
            ],
            'function': sn_sum_list,
            'expected_output': '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]',
        },
        {
            'input': [
                '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]',
                '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
            ],
            'function': sn_sum_list,
            'expected_output': '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]'
        },
        {
            'input': [
                '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]',
                '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
            ],
            'function': sn_sum_list,
            'expected_output': '[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]',
        },
        {
            'input': [
                '[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]',
                '[7,[5,[[3,8],[1,4]]]]',
            ],
            'function': sn_sum_list,
            'expected_output': '[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]'
        },
        {
            'input': [
                '[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]',
                '[[2,[2,2]],[8,[8,1]]]',
            ],
            'function': sn_sum_list,
            'expected_output': '[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]'
        },
        {
            'input': [
                '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
                '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
                '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
                '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
                '[7,[5,[[3,8],[1,4]]]]',
                '[[2,[2,2]],[8,[8,1]]]',
                '[2,9]',
                '[1,[[[9,3],9],[[9,0],[0,7]]]]',
                '[[[5,[7,4]],7],1]',
                '[[[[4,2],2],6],[8,7]]',
            ],
            'function': sn_sum_list,
            'expected_output': '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]',
        },
        {
            'input': [
                '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
                '[[[5,[2,8]],4],[5,[[9,9],0]]]',
                '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
                '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
                '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
                '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
                '[[[[5,4],[7,7]],8],[[8,3],8]]',
                '[[9,3],[[9,9],[6,[4,9]]]]',
                '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
                '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]',
            ],
            'function': sn_sum_list,
            'expected_output': '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]',
        },
        {
            'input': [
                '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
                '[[[5,[2,8]],4],[5,[[9,9],0]]]',
                '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
                '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
                '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
                '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
                '[[[[5,4],[7,7]],8],[[8,3],8]]',
                '[[9,3],[[9,9],[6,[4,9]]]]',
                '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
                '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]',
            ],
            'function': lambda x: sn_magnitude(sn_sum_list(x)),
            'expected_output': 4140
        },
    ]

    n_passed = 0
    result_strings = ["failed", "passed"]
    for i,t in enumerate(tests):
        if only == None or i in only or \
           ('name' in t and t['name'] in only):
            actual_output = t['function'](t['input'])
            result = actual_output == t['expected_output']
            if verbose or not result:
                test_title = f'Test {i}'
                if 'name' in t:
                    test_title = 'Test {}, {},'.format(i, t['name'])
                print("{} {}".format(test_title, result_strings[int(result)]))
                if not result:
                    print(" Function: {}".format(t['function']))
                    print("      for: {}".format(t['input']))
                    print("   wanted: {}".format(t['expected_output']))
                    print("  but got: {}".format(actual_output))
                    print("-- \n")
            n_passed += result

    n_tests = len(tests)
    if only != None:
        n_tests = len(only)
    if n_passed == n_tests:
        print("All {} trivial tests passed!".format(n_passed))
    else:
        print("Passed {} out of {} tests :-(".format(n_passed, n_tests))

    return n_passed == len(tests)


def get_snailfish_numbers(fh):
    return [line.strip() for line in fh]


if __name__ == "__main__":
    pp = pprint.PrettyPrinter()

    if trivial_tests(verbose=False):
        snailfish_numbers = get_snailfish_numbers(sys.stdin)
        print("Magnitude: {}".format(
            sn_magnitude(sn_sum_list(snailfish_numbers))))
