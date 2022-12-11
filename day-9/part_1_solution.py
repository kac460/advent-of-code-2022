from __future__ import annotations
from collections import namedtuple

_DIR_INDEX = 0
_DIST_INDEX = 2
Move = namedtuple('Move', 'dir dist')
Position = namedtuple('Position', 'x y')

def get_moves(filename: str = 'day-9/input.txt') -> list[Move]:
    with open(filename) as f:
        return [
            Move(line[_DIR_INDEX], int(line.strip()[_DIST_INDEX:]))
            for line in f.readlines()
        ]

RIGHT = 'R'
DOWN = 'D'
LEFT = 'L'
UP = 'U'
MOVE_THRESHOLD = 2
MOVE_DIST = MOVE_THRESHOLD - 1
class RopeMover:
    def __init__(self):
        self._h = Position(0, 0)
        self._t = Position(0, 0)
        self.t_visited = {self._h}

    def move_h(self, move: Move) -> None:
        for i in range(move.dist):
            self._move_h(Move(move.dir, 1))

    def _move_h(self, move: Move) -> None:
        #print(f'_move_h move: {move}')
        #print(f't={self._t}, h={self._h}')
        if move.dir not in (RIGHT, DOWN, LEFT, UP):
            raise ValueError(f'Received invalid move {move}')
        if move.dist != 1:
            raise ValueError('Private _move_h should be used only with moves of length 1 '
                f'but got {move.dist}'
            )
        displacement = -1 * move.dist if (
            move.dir in (LEFT, DOWN)
        ) else move.dist
        if move.dir in (RIGHT, LEFT):
            self._h = Position(self._h.x+displacement, self._h.y)
            if abs(self._h.x - self._t.x) >= MOVE_THRESHOLD:
                self._t = Position(self._t.x + displacement, self._h.y)
        else:
            self._h = Position(self._h.x, self._h.y+displacement)
            if abs(self._h.y - self._t.y) >= MOVE_THRESHOLD:
                self._t = Position(self._h.x, self._t.y + displacement)
        #print(f'now: t={self._t}, h={self._h}')
        self.t_visited.add(self._t)

    # just match on the closer axis
    # and move within 1 on the less close axis
    
    # we could've tried to be intelligent about which directions actually need to be checked
    # based on how _h moved, but this is easier and still asymptotically the same runtime
    def _move_t_if_needed(self) -> None:
        # need to move 1 closer x-wise, match y-wise
        print(f't={self._t}, h={self._h}')
        if abs(self._t.x - self._h.x) >= MOVE_THRESHOLD:
            # e.g., if t.x=3, h.x=1, add (h.x - h.y)=(1 - 3)= -2
            print('moving hor, matching ver')
            displacement = -1 * MOVE_DIST if self._t.x > self._h.x else MOVE_DIST
            self._t.x += displacement
            self._t.y = self._h.y
        else:
            print('matching hor, moving ver')
            displacement = -1 * MOVE_DIST if self._t.y > self._h.y else MOVE_DIST
            self._t.x = self._h.x
            self._t.y += displacement
        print(f'now: t={self._t}, h={self._h}')
        self.t_visited.add(self._t)

if __name__ == '__main__':
    mover = RopeMover()
    for move in get_moves():
        print(f'move: {move}')
        mover.move_h(move)
    print(len(mover.t_visited))
    '''mover.move_h(Move(UP, 1))
    print('move up 1')
    mover.move_h(Move(UP, 1))
    print('move up 1')
    mover.move_h(Move(DOWN, 1))
    print('move down 1')
    mover.move_h(Move(UP, 1))
    print('move up 1')
    mover.move_h(Move(RIGHT, 1))
    print('move right 1')
    mover.move_h(Move(RIGHT, 1))
    print('move right 1')'''
    
