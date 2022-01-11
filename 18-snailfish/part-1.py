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
    #print("ADDING {} to {}".format(a, b))
    return(sn_reduce(sn_add_only(a,b)))


def sn_reduce(s):
    r = s
    prev = None
    i = 0
    #print(" before: {}".format(r))
    while True:
        prev = r
        r = sn_explode_or_split(r)
        #print("  after: {}".format(r))
        if r == prev:
            break
    return(r)


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
    new_right = []
    n = []
    just_sail_on_through = False
    for i,c in enumerate(s):
        if just_sail_on_through:
            new_right.append(c)
        else:
            if c in '0123456789':
                n.append(c)
            else:
                if n == []:
                    new_right.append(c)
                else:
                    new_right.append(str(x + list2num(n)))
                    new_right.append(c)
                    just_sail_on_through = True
    return(''.join(new_right))


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


def sn_leftright(n):
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


def sn_magnitude(sn, depth=0):
    #print("SN ({}): {}".format(depth, sn))
    left, right = sn_leftright(sn)
    #print("  LEFT: {}".format(left))
    #print("  RIGH: {}".format(right))
    #print("-- ")

    left_magn = 0
    if sn_is_number(left):
        left_magn = int(left) * 3
    else:
        left_magn = sn_magnitude(left, depth+1) * 3

    right_magn = 0
    if sn_is_number(right):
        right_magn = int(right) * 2
    else:
        right_magn = sn_magnitude(right, depth+1) * 2

    return(left_magn + right_magn)


def list2num(l):
    n = 0
    for i,x in enumerate(reversed(l)):
        n += int(x) * int((10**i))
    return n


def sn_is_number(l):
    return(len(l) > 0 and
           reduce(lambda x, y: x and y,
                  map(lambda c: c in '0123456789', l),
                  True))

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
                if sn_is_number(subj):
                    if list2num(subj) >= split_threshold:
                        right = s[i:]
                        # print("SPLIT: L:{};  S:{};  R:{};".format(
                        #     *map(lambda x: ''.join(x), [left, subj, right])))
                        subj = sn_split_number(list2num(subj))
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
                right = s[i+1:]
                # print("EXPLOSION: L:{};  S:{};  R:{};".format(
                #     *map(lambda x: ''.join(x), [left, subj, right])))
                left = sn_explode_leftward(left, sn_numbers(subj)[0])
                right = sn_explode_rightward(right, sn_numbers(subj)[1])
                subj = ['0']
                break
            else:
                if sn_is_number(subj):
                    if list2num(subj) >= split_threshold:
                        right = s[i:]
                        # print("SPLIT: L:{};  S:{};  R:{};".format(
                        #     *map(lambda x: ''.join(x), [left, subj, right])))
                        subj = sn_split_number(list2num(subj))
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

#    print("L:{};  S:{};  R:{};".format(*map(lambda x: ''.join(x), [left, subj, right])))
    return ''.join(map(lambda x: ''.join(x), [left, subj, right]))


def sn_sum_list(l, verbose=False):
    total = None
    for i,n in enumerate(l):
        if total == None:
            total = n
#            print("INITIAL: {}".format(total))
        else:
#            print("      N: {}".format(n))
            new_total = sn_add(total, n)
#            print("  TOTAL: {}".format(new_total))
#            print("-- ")
            if verbose:
                print("{} + {} = {}".format(
                    *map(lambda x: ''.join(x), [total, n, new_total])))
            total = new_total

    return total


def trivial_tests(verbose=False):

    # Could use a lambda for 'function', but better name this way.
    def tt_add11(x):
        return(sn_add(x, '[1,1]'))

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
        actual_output = t['function'](t['input'])
        result = actual_output == t['expected_output']
        if verbose or not result:
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


def get_snailfish_numbers(fh):
    return [line.strip() for line in fh]


if __name__ == "__main__":

    pp = pprint.PrettyPrinter()
    if trivial_tests():
        snailfish_numbers = get_snailfish_numbers(sys.stdin)
        print(sn_sum_list(snailfish_numbers))
        print(sn_magnitude(sn_sum_list(snailfish_numbers)))
