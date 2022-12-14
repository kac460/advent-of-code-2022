from __future__ import annotations
from collections import deque
from typing import Any

_FILENAME = 'day-12/input.txt'
def read_input() -> list[str]:
    with open(_FILENAME) as f:
        # strip newline char
        return [line[:len(line)-1] for line in f.readlines()]

def get_graph() -> dict[tuple[int, int], set[int]]:
    lines = read_input()
    graph = {}
    valid_indices = lambda i, j: i >= 0 and i < len(lines) and j >= 0 and j < len(lines[i])
    neighbor_in_reach = lambda v, n: ord(n) <= ord(v) + 1 or v == 'S'
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            neighbor_indices = (
                (i-1, j),
                (i, j-1),
                (i, j+1),
                (i+1, j)
            )
            graph[(i, j)] = {
                neighbor_index
                for neighbor_index in neighbor_indices
                if (
                    valid_indices(*neighbor_index) 
                    and 
                    neighbor_in_reach(lines[i][j], lines[neighbor_index[0]][neighbor_index[1]])
                )
            }
    return graph

def get_s_e() -> tuple[int, int]:
    lines = read_input()
    s = e = None
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == 'S':
                s = (i, j)
                if e:
                    return s, e
            elif lines[i][j] == 'E':
                e = (i, j)
                if s:
                    return s, e
                


def bfs(graph: dict[Any, set[int]], s: tuple[int,int], e: tuple[int,int]) -> list[tuple[int, int]]:
    q = deque()
    parents = {}
    parents[s] = None 
    q.append(s)
    while len(q) > 0:
        v = q.popleft()
        if v == e:
            break
        for neighbor in graph[v]:
            if neighbor not in parents:
                parents[neighbor] = v
                q.append(neighbor)
    if v != e:
        return None
    backwards_path = []
    v = e
    while parents[v] is not None:
        backwards_path.append(parents[v])
        v = parents[v]
    return list(reversed(backwards_path))


def get_as() -> list[tuple[int, int]]:
    lines = read_input()
    return [
        (i, j)
        for i in range(len(lines))
        for j in range(len(lines[i]))
        if lines[i][j] == 'a'
    ]


if __name__ == '__main__':
    print('PART 1')
    graph = get_graph()
    s, e = get_s_e()
    path = bfs(graph, s, e)
    #print(path)
    #print(f'{s} {e}')
    print(len(path))
    print('----')
    print('PART 2')
    nadirs = get_as() + [s]
    nadir_paths = filter(
        lambda path: path is not None, 
        [bfs(graph, nadir, e) for nadir in nadirs]
    )
    smallest_nadir_path_len = min([len(path) for path in nadir_paths])
    print(smallest_nadir_path_len)
