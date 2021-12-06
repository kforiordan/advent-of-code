
import sys
import pprint


def get_bingo_numbers(fh):
    numbers = []

    # I know this is terrible.
    for line in fh:
        if len(line.strip()) > 3:
            numbers = list(map(int, line.strip().split(',')))
            #pp.pprint(numbers)  # HOW THE FUCK IS pp IN SCOPE?
            break

    return numbers


def get_bingo_boards(fh):
    boards = []

    n = 0
    board = []
    for line in fh:
        line = line.strip()
        if len(line) == 0:
            if len(board) == 0:
                continue
            else:
                boards.append(board)
                board = []
                n = n + 1
        else:
            bingo_line = list(map(int, line.split()))
            board.append(bingo_line)

    if len(board) > 0:
        boards.append(board)

    return boards


def solve_boards_incrementally(boards, numbers):
    solutions = []
    numbers_so_far = []

    # Try with the first number, then the first two, then first three, etc.
    for n in numbers:
        numbers_so_far.append(n)
        solutions = solve_boards(boards, numbers_so_far)
        if len(solutions) > 0:
            break

    return solutions


def solve_boards(boards, numbers):
    solutions = []

    for board in boards:
        solution = solve_board(board, numbers)
        if len(solution) > 0:
            solutions.append(solution)

    # Returns a list of boards that have solutions
    return solutions


def solve_board(board, numbers):
    solution = []

    for row in board:
        if len(solve_seq(row, numbers)) > 0:
            solution = board
            break

    if len(solution) == 0:
        c = 0
        col_len = len(board)
        while c < col_len:
            col = [row[c] for row in board]
            if len(solve_seq(col, numbers)) > 0:
                solution = board
                break
            c = c + 1

    # Diagonals would go here but spec says no

    # Returns the board if it has a solution
    return solution


# O(n^2)
def solve_seq(row_or_col, numbers):
    solution = []

    c = 0
    for e in row_or_col:
        for n in numbers:
            if e == n:
                c = c+1
                break
    if c == len(row_or_col):
        solution = row_or_col

    return solution


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=True)

    numbers = get_bingo_numbers(sys.stdin)
    boards = get_bingo_boards(sys.stdin)

    # pp.pprint(numbers)
    # pp.pprint(boards)
    # exit(0)

    solutions = solve_boards_incrementally(boards, numbers)
    pp.pprint(numbers)
    pp.pprint(solutions)

