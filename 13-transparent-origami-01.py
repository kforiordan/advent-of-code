import sys
import pprint

def get_points(fh):
    points = []
    for line in fh:
        point = line.strip().split(',')
        if len(point) < 2:
            break
        points.append(tuple(map(int,point)))
    return points


def get_fold_lines(fh):
    fold_lines = []
    for line in fh:
        junk, junk, fold_line = line.strip().split()
        axis, coord = fold_line.split('=')
        fold_lines.append((axis,int(coord)))
    return(fold_lines)


if __name__ == "__main__":
    points = get_points(sys.stdin)
    fold_lines = get_fold_lines(sys.stdin)
