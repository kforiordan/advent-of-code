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


def explode_leftward(s, x):
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
                    new_left.append('{}'.format(x + n))
    return(''.join(reversed(new_left)))


def explode_rightward(s, x):
    return(''.join(reversed(explode_leftward(s, x))))


def explode_or_split(s):

    # For tracking whether we should explode or not
    explosion_threshold = 4
    depth = 0

    # For tracking numbers as encountered - split may be needed
    split_threshold = 10
    n = None

    # As we move from left to right through the string, we copy stuff leftwards
    left = []

    # We start with the whole string to our right
    right = list(s)

    # After a split or explode we just copy everything from right to left.
    just_sail_on_through = False

    for i,c in enumerate(right):
        #print('{}: "{}" "{}"'.format(i, s[0:i], c))
        if just_sail_on_through:
            left.append(c)
        else:
            if c == '[':
                depth += 1
                if depth > explosion_threshold:
                    left.append('0')
                else:
                    left.append(c)
            elif c == ',':
                # We need to process the left number of a pair
                if depth > explosion_threshold:
                    left = list(explode_leftward(left, n))
                else:
                    if n != None:
                        if n > split_threshold:
                            left.append(str(split_number(n)))
                            just_sail_on_through = True
                        else:
                            left.append(str(n))
                        n = None
                    left.append(c)
            elif c == ']':
                # We need to process the right number of a pair
                if depth > explosion_threshold:
                    right = list(explode_rightward(right, n))
                elif n != None:
                    if n > split_threshold:
                        left.append(str(split_number(n)))
                        left.append(c)
                        just_sail_on_through = True
                    else:
                        left.append(str(n))
                        left.append(c)
                    n = None
                depth -= 1
            elif c in '0123456789':
                if n == None:
                    n = int(c)
                else:
                    n = (n * 10) + int(c)

    return ''.join(left)


def reduce(s):
    r = s
    while True:
        r = explode_or_split(r)
        if r == s:
            break
    return(r)


def trivial_tests():
    tests = [
        {
            'input': '[[[[0,7],4],[15,[0,13]]],[1,1]]',
            'function': explode_or_split,
            'expected_output': '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
        },
        {
            'input': '[[[[[9,8],1],2],3],4]',
            'function': explode_or_split,
            'expected_output': '[[[[0,9],2],3],4]'
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

    trivial_tests()
