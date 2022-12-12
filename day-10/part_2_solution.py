from __future__ import annotations
from math import floor
from part_1_solution import (
    CPU,
    get_instructions
)
_SCREEN_LENGTH = 40
_SCREEN_HEIGHT = 6
class CRT(CPU):
    def __init__(self):
        super().__init__()
        self._screen = [
            ['X' for col in range(_SCREEN_LENGTH)]
            for row in range(_SCREEN_HEIGHT)
        ]


    def _complete_cycle(self) -> None:
        self._draw_pixel()
        super()._complete_cycle()

    def _pixel(self) -> str:
        if abs(self._x - self._col()) > 1:
            return '.'
        return '#'

    def _draw_pixel(self) -> None:
        row = self._row()
        col = self._col()
        if col == 14:
            print('here')
        self._screen[row][col] = self._pixel()
        

    def _row(self) -> int:
        # note: _clock_cycle is the last completed clock cycle
        # so if we're in clock cycle 1, _clock_cycle = 0 -> 0
        # if we're in clock cycle 40, _clock_cycle = 39 -> 0
        # if we're in clock cycle 41, _clock_cycle = 40 -> 1
        return floor((self._clock_cycle) / _SCREEN_LENGTH)

    def _col(self) -> int:
        return self._clock_cycle % _SCREEN_LENGTH

    def print_screen(self) -> None:
        for row in self._screen:
            print(''.join(row))

if __name__ == '__main__':
    crt = CRT()
    instructions = get_instructions()
    crt.execute_instructions(instructions)
    crt.print_screen()