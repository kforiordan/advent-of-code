import sys
import pprint


def get_edges(fh):
    return [tuple(line.strip().split('-')) for line in fh]


def build_path_graph(edges):
    graph = {}
    for (a,b) in edges:
        if a in graph:
            graph[a].update(set([b]))
        else:
            graph[a] = set([b])
        # And the same but in the opposite direction
        if b in graph:
            graph[b].update(set([a]))
        else:
            graph[b] = set([a])

    return graph


def is_small(cave):
    return cave.islower()


def is_big(cave):
    return cave.isupper()


def find_paths(graph, cave:str, path_so_far:list[str]) -> list[list[str]]:
    paths = []

    if cave in path_so_far:
        if is_small(cave):
            return None

    path = path_so_far.copy()
    path.append(cave)

    if cave == 'end':
        return [path]

    for next_hop in graph[cave]:
        sub_paths = find_paths(graph, next_hop, path)
        if sub_paths != None:
            for p in sub_paths:
                paths.append(p)

    return paths


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=False)

    path_graph = build_path_graph(get_edges(sys.stdin))

    paths = find_paths(path_graph, 'start', [])

    print("Number of paths: {}".format(len(paths)))
