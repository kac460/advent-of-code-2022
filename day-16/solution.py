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


def most_pressure_to_release(graph: dict[str, list[str]], rates: dict[str, int], s: str = 'AA', start_time: int = 30):
    # idea: make memo 3d
    # 3rd dimension would be frozenset of which valves are open
    # return memo[(s, 29?, empty_frozenset)]
    # val(v, t, open):
    #   skip if v in open; otherwise max(skip, release)
    #   skip: max(val(c, t-1, open) for c in graph[v])
    #   release: rates[v] * (t-1) + max(val(c, t-2, open) for c in graph[v])

    # would never open valves with flow rate = 0
    possible_opens = powerset({v for v in rates if rates[v] > 0})
    memo = {}
    #memo = {(v, -1): 0 for v in graph}
    memo.update({(v, 0, p_o): 0 for v in graph for p_o in possible_opens})
    memo.update({(v, 1, p_o): 0 for v in graph for p_o in possible_opens})
    for t in range(2, start_time+1):
        # Goal: set memo[(v, t)] for time 0 <= t <= start_time
        #   (we don't need to check beyond start_time - dist)
        # if t = 1: 
        #   memo[(v, t)] = rates[v]
        # Otherwise: 
        #   (Either release v then move to best child or immediately move to best child)
        #   (note in our input every v has non-empty neighbor list graph[v])
        #   Release v: rates[v] + max(memo[(c, t-2)] for c in graph[v]) 
        #   Move to best child: max(memo[(c, t-1) for c in graph[v]])
        # apparently I misinterpreted the question :(

        for v in graph:
            for possible_open in possible_opens:
                local_p_os = frozenset(
                    p_o for p_o in possible_opens 
                    # we know at least those in p_o must be open from here
                    if p_o.issuperset(possible_open)
                )
                skip = max(memo[(c, t-1, p_o)] for c in graph[v] for p_o in local_p_os)
                if v in possible_open:
                    memo[(v, t, possible_open)] = skip
                else: 
                    # if open v, eliminate those p_os where v not in p_o
                    new_p_os = frozenset({p_o for p_o in local_p_os if v in p_o})
                    release = rates[v] * (t-1) + (max(
                        memo[(c, t-2, p_o)] 
                        for c in graph[v] for p_o in new_p_os
                    ) if len(new_p_os) > 0 else 0)
                    memo[(v, t, possible_open)] = max(release, skip)
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
    main(test=True)