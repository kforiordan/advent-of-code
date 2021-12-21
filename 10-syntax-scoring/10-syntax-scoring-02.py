
import sys
import pprint

def get_chunk_lines(fh):
    lines = []

    for line in fh:
        lines.append(list(line.strip()))

    return lines


def tag_match(o, c):
    return (o,c) in zip(openers, closers)


def get_score(stack):
    # I hate dynamic scope so much, but will admit it is convenient
    c2s_map = {k:v for k,v in zip(closers,scores)}
    score = 0
    while len(stack) > 0:
        o = stack.pop()
        c = o2c_map[o]
        s = c2s_map[c]
        score = (score * 5) + s

    return score


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=True)
    chunk_lines = get_chunk_lines(sys.stdin)

    openers = ['(', '[', '{', '<']
    closers = [')', ']', '}', '>']
    o2c_map = {k:v for (k,v) in zip(openers,closers)}
    scores = [1,2,3,4]

    corrupted_lines = []
    incomplete_lines = []

    line_no = 0
    line_scores = []
    for line in chunk_lines:
        line_no += 1
        stack = []

        corrupt = False
        for c in line:
            if c in openers:
                stack.append(c)
            elif c in closers:
                if tag_match(stack[-1], c):
                    stack.pop()
                else:
                    corrupted_lines.append(line)
                    corrupt = True
                    break

        if corrupt:
            continue
        else:
            incomplete_lines.append((line_no, line, stack))

    for (line_no, line, stack) in incomplete_lines:
        line_scores.append(get_score(stack))

    winner = sorted(line_scores)[round(len(line_scores)/2)]
    print(winner)
