
from __future__ import annotations
from part_1_solution import (
    get_valves,
    powerset,
    dist
)

def most_pressure_to_release(
    graph: dict[str, list[str]], 
    rates: dict[str, int], 
    s: str = 'AA', 
    start_time: int = 26
) -> int:
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
  memo = {}
  memo.update({(m, e, 0, p_o): 0 for m in graph for e in graph for p_o in possible_opens})
  memo.update({(m, e, 1, p_o): 0 for m in graph for e in graph for p_o in possible_opens})
  for t in range(2, start_time+1):
        print(t)
        for m in graph:
            for e in graph:
                for open_valves in possible_opens:
                    # TODO:
                    m_skip = None
                    e_skip = None
                    if rates[m] == 0:
                        m_best = m_skip
                    else:
                        # TODO - not sure if we need to account for e here
                        new_open_valves = open_valves.union({m})
                        m_release = None
                        m_best = max(m_skip, m_release)
                    if rates[e] == 0:
                        e_best = e_skip
                    else:
                        # TODO - not sure if we need to account for m here
                        new_open_valves = open_valves.union({e})
                        e_release = None
                        e_best = max(e_skip, e_release)
                    memo[(m, e, t, open_valves)] = m_best + e_best
                    


def main(test: bool = False) -> None:
    if test:
        filename = 'day-16/test.txt'
    else:
        filename = 'day-16/input.txt'
    graph = {}
    rates = {}
    get_valves(filename, graph, rates)

if __name__ == '__main__':
    main()
