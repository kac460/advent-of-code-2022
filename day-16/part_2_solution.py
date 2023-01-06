
from __future__ import annotations
from part_1_solution import (
    get_valves,
    powerset,
    dist
)
from collections import namedtuple

# it's probably not the best to have value stored in Move
# given you can get that via Memo
# but i feel this'll make my life easier
Move = namedtuple('Move', 'valve t open_valves value')
M = 0
E = 1
def best_next_move(
    graph: dict[str, list[str]], 
    rates: dict[str, int], 
    memo: dict[tuple[str, str, int, frozenset[str]], int],
    m_or_e: int,
    open_valves: frozenset[str],
    valve: str,
    other_valve: str,
    t: int,
    max_openable_valves: int,
):
    if m_or_e == M:
        children_val = lambda c, c_t, new_opens: memo[
            (c, other_valve, c_t, new_opens)][m_or_e]
    else:
        children_val = lambda c, c_t, new_opens: memo[
            (other_valve, c, c_t, new_opens)][m_or_e]
    skip_t = t - 1
    children = graph[valve]
    # TODO - use the right key for memo
    skip_valve = max(children, key=lambda c: children_val(c, skip_t, open_valves))
    skip_value = children_val(skip_valve, skip_t, open_valves)
    skip_move = Move(skip_valve, skip_t, open_valves, skip_value)
    if rates[valve] == 0 or valve in open_valves or len(open_valves) == max_openable_valves:
        return skip_move
    release_t = t - 2
    open_valves_if_release = open_valves.union({valve})
    release_valve = max(
        children, 
        key=lambda c: children_val(c, release_t, open_valves_if_release)
    )
    release_value = rates[valve] * (t-1) + children_val(release_valve, release_t, open_valves_if_release)
    if release_value > skip_value:
        return Move(release_valve, release_t, open_valves_if_release, release_value)
    return skip_move

def most_pressure_to_release(
    graph: dict[str, list[str]], 
    rates: dict[str, int], 
    s: str = 'AA', 
    start_time: int = 26
) -> int:
  openable_valves = {
    v for v in rates 
    if (
        rates[v] > 0
        and
        dist(s, v, graph) < start_time - 1
    )
  }
  possible_opens = powerset(openable_valves)
  max_openable_valves = len(openable_valves)
  memo = {}
  memo.update({(m, e, 0, p_o): (0, 0) for m in graph for e in graph for p_o in possible_opens})
  memo.update({(m, e, 1, p_o): (0, 0) for m in graph for e in graph for p_o in possible_opens})
  for t in range(2, start_time+1):
        print(t)
        for m in graph:
            for e in graph:
                for open_valves in possible_opens:
                    m_move = best_next_move(
                        graph=graph,
                        rates=rates,
                        memo=memo,
                        m_or_e=M,
                        open_valves=open_valves,
                        valve=m,
                        other_valve=e,
                        t=t,
                        max_openable_valves=max_openable_valves
                    )
                    # this logic for what e should do probably isn't right
                    # not the case that when e moves, open_valves = m_move.open_valves
                    # with m at m_move.valve *already*
                    e_move = best_next_move(
                        graph=graph,
                        rates=rates,
                        memo=memo,
                        m_or_e=E,
                        open_valves=m_move.open_valves,
                        valve=e,
                        other_valve=m_move.valve,
                        t=t,
                        max_openable_valves=max_openable_valves
                    )
                    memo[(m, e, t, open_valves)] = (m_move.value, e_move.value)
  final_val = memo[(s, s, start_time, frozenset({}))]
  print(f'final_val: {final_val}')
  return final_val[M] + final_val[E]
                    


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
    main(True)
