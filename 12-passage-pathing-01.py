import sys
import pprint


def get_edges(fh):
    return [tuple(line.strip().split('-')) for line in fh]


def build_path_graph(edges):
    graph = {}
    for (a,b) in edges:
        if a in graph:
            graph[a].append(b)
        else:
            graph[a] = [b]
    return graph


def is_minor(cave):
    return cave.islower()


def is_big(cave):
    return cave.isupper()


def find_paths(graph, start='start', path=None):
    paths = []

    if path == None:
        path = [start]
    else:
        if start in path:
            if is_minor(start):
                return []
            else:
                for next_hop in graph[start]:
                    if next_hop == "end":
                        
                    else:
                        subpath = path.copy()
                        subpaths = find_paths(graph, next_hop, subpath)
                        for p in subpaths:
                            if len(p) > 0:
                                paths.append(p)
        else:
            for next_hop in graph[start]:
                if next_hop == "end":
                    paths.append(path.append("end"))
                else:
                    subpath = path.copy()
                    subpaths = find_paths(graph, next_hop, subpath)
                    for p in subpaths:
                        paths.append(p)

    return paths


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=False)
    path_graph = build_path_graph(get_edges(sys.stdin))
    paths = find_paths(path_graph)
    pp.pprint(path_graph)
    print("-- ")
    pp.pprint(paths)
