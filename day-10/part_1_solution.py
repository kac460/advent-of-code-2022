from __future__ import annotations
from collections import namedtuple

NOOP = 'noop'
ADDX = 'addx'
class CPU:
    def __init__(self):
        self._x = 1
        self._clock_cycle = 0
        self._logs = {}

    def _log(self) -> None:
        self._logs[self._clock_cycle] = self._x

    def _complete_cycle(self) -> None:
        self._clock_cycle +=1
        self._log()
    
    def _noop(self) -> None:
        self._complete_cycle()

    def _addx(self, x: int) -> None:
        self._complete_cycle()
        self._complete_cycle()
        self._x += x

    def get_log(self, clock_cycle: int):
        return self._logs[clock_cycle]
    
    def execute_instruction(self, instruction: str) -> None:
        instruction_split = instruction.split()
        op = instruction_split[0]
        if op == NOOP:
            self._noop()
        elif op == ADDX:
            self._addx(int(instruction_split[1]))
        else:
            raise ValueError(f'invalid instruction "{instruction}"')

    def execute_instructions(self, instructions: list[str]) -> None:
        for instruction in instructions:
            self.execute_instruction(instruction)
        
def get_instructions(filename: str = 'day-10/input.txt') -> list[str]:
    with open(filename) as f:
        return f.readlines()

def sum_interesting_signal_strengths(start: int, end: int, step: int) -> int:
    instructions = get_instructions()
    cpu = CPU()
    cpu.execute_instructions(instructions)
    return sum([
        cycle * cpu.get_log(cycle)
        for cycle in range(start, end+1, step)
    ])

_START = 20
_END = 220
_STEP = 40

if __name__ == '__main__':
    print(sum_interesting_signal_strengths(_START, _END, _STEP))
