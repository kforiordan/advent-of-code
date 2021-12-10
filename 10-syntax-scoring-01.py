
import sys
import pprint

def get_chunk_lines(fh):
    lines = []

    for line in fh:
        lines.append(list(line.strip()))

    return lines


def tag_match(o, c):
    return (o,c) in zip(openers, closers)

def get_score(c):
    h = {k:v for (k,v) in zip(closers,scores)}
    return h[c]

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=True)
    chunk_lines = get_chunk_lines(sys.stdin)

    openers = ['(', '[', '{', '<']
    closers = [')', ']', '}', '>']
    scores = [3, 57, 1197, 25137]

    stack = []
    line_no = 0
    score = 0
    for line in chunk_lines:
        line_no += 1
        for c in line:
            if c in openers:
                stack.append(c)
            elif c in closers:
                if tag_match(stack[-1], c):
                    stack.pop()
                else:
                    s = "{}: Expected {}, but found {} instead."
                    print(s.format(line_no, stack[-1], c))
                    score += get_score(c)
                    break

    print("Score: {}".format(score))
