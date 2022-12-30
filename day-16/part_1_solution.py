# Idea: assign a value for each node, time pair
# A node n's value at time t is the amount of pressure releasable at that node
# I.e., val(n, t) is computed as
#   max(p(n)+max(val(c, t-2) for c in children(n)), max(val(c, t-1) for c in children(n)))
# Maybe do this via DP? Starting from the bottom (now we here)

from __future__ import annotations
from collections import deque
from itertools import chain, combinations

def powerset(s: set) -> frozenset[frozenset]:
    # powerset({1,2,3}) --> {() (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)}
    return frozenset(frozenset(e) for e in chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

_NAME = 1
_RATE = 4
_FIRST_NEIGHBOR = 9
def get_valves(filename, graph: dict[str, list[str]], rates: dict[str, int]) -> None:
    with open(filename) as f:
        lines = [line.split() for line in f.readlines()]
    for line in lines:
        name = line[_NAME]
        rate = int(line[_RATE].split('=')[1][:-1])
        neighbors = [token.strip(',') for token in line[_FIRST_NEIGHBOR:]]
        rates[name] = rate
        graph[name] = neighbors


def dist(s: str, e: str, graph: dict[str, list[str]]) -> int:
    q = deque()
    parents = {s: None}
    q.append(s)
    while len(q) > 0:
        v = q.popleft()
        if v == e:
            break
        for neighbor in graph[v]:
            if neighbor not in parents:
                parents[neighbor] = v
                q.append(neighbor)
    path_len = 0
    v = e
    while v != s:
        v = parents[v]
        path_len += 1
    return path_len


def most_pressure_to_release_rec(
    graph: dict[str, list[str]], 
    rates: dict[str, int], 
    s: str, 
    t: int,
    memo: dict[tuple[str, int, frozenset]] = None,
    open_valves: frozenset[frozenset[str]] = frozenset()
) -> int:
    if memo is None:
        memo = {}
        possible_opens = powerset(
            {
                v for v in rates 
                if (
                    rates[v] > 0
                    and
                    dist(s, v, graph) < t
                )
            }
        )
        memo.update({(v, 0, p_o): 0 for v in graph for p_o in possible_opens})
        memo.update({(v, 1, p_o): 0 for v in graph for p_o in possible_opens})
    if (s, t, open_valves) in memo:
        return memo[(s, t, open_valves)]
    # memo[(s, start_time, frozenset({}))]
    # best we can do if we skip opening s
    skip = max(
        most_pressure_to_release_rec(
            graph=graph,
            rates=rates, 
            s=neighbor,
            t=t-1,
            memo=memo,
            open_valves=open_valves
        ) for neighbor in graph[s]
    )
    # if s is already open, obviously we skip oppening s s
    if s in open_valves:
        memo[(s, t, open_valves)] = skip
        return skip
    # Compute best if we open s
    new_open_valves = open_valves.union({s})
    release = rates[s] * (t-1) + (max(
        most_pressure_to_release_rec(
            graph=graph,
            rates=rates,
            s=neighbor,
            t=t-2,
            memo=memo,
            open_valves=new_open_valves,
        ) for neighbor in graph[s]
    ) if len(new_open_valves) > 0 else 0)
    if release > skip:
        memo[s, t, open_valves] = release
        return release
    memo[s, t, open_valves] = skip
    return skip


def most_pressure_to_release(graph: dict[str, list[str]], rates: dict[str, int], s: str = 'AA', start_time: int = 30) -> int:
    # idea: make memo 3d
    # 3rd dimension would be frozenset of which valves are open
    # return memo[(s, 29?, empty_frozenset)]
    # val(v, t, open):
    #   skip if v in open; otherwise max(skip, release)
    #   skip: max(val(c, t-1, open) for c in graph[v])
    #   release: rates[v] * (t-1) + max(val(c, t-2, open) for c in graph[v])

    # would never open valves with flow rate = 0
    possible_opens = powerset(
        {
            v for v in rates 
            if (
                rates[v] > 0
                and
                dist(s, v, graph) < start_time - 1
            )
        }
    )
    print(len(possible_opens))
    memo = {}
    memo.update({(v, 0, p_o): 0 for v in graph for p_o in possible_opens})
    memo.update({(v, 1, p_o): 0 for v in graph for p_o in possible_opens})
    for t in range(2, start_time+1):
        print(t)
        for v in graph:
            for open_valves in possible_opens:
                # only need to check the child opens?
                # (or something like that)
                '''local_p_os = frozenset(
                    p_o for p_o in possible_opens 
                    # we know at least those in p_o must be open from here
                    if p_o.issuperset(open_valves)
                )'''
                #skip = max(memo[(c, t-1, p_o)] for c in graph[v] for p_o in local_p_os)
                skip = max(memo[(c, t-1, open_valves)] for c in graph[v])
                if rates[v] == 0 or v in open_valves:
                    memo[(v, t, open_valves)] = skip
                else: 
                    # if open v, eliminate those p_os where v not in p_o
                    '''new_p_os = frozenset({p_o for p_o in local_p_os if v in p_o})
                    release = rates[v] * (t-1) + (max(
                        memo[(c, t-2, p_o)] 
                        for c in graph[v] for p_o in new_p_os
                    ) if len(new_p_os) > 0 else 0)'''
                    new_open_valves = open_valves.union({v})
                    release = rates[v] * (t-1) + max(
                        memo[(c, t-2, new_open_valves)]
                        for c in graph[v]
                    )
                    memo[(v, t, open_valves)] = max(release, skip)
    return memo[(s, start_time, frozenset({}))]


def main(test: bool = False) -> None:
    if test:
        filename = 'day-16/test.txt'
    else:
        filename = 'day-16/input.txt'
    graph = {}
    rates = {}
    get_valves(filename, graph, rates)
    print(most_pressure_to_release(graph, rates))
    

if __name__ == '__main__':
    main(test=False)