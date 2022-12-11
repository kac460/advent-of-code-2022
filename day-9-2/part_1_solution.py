from __future__ import annotations
from collections import namedtuple

Step = namedtuple('Displacement', 'delta_x delta_y')
Move = namedtuple('Move', 'direction magnitude')

UP = 'U'
RIGHT = 'R'
DOWN = 'D'
LEFT = 'L'

UP_RIGHT = 'UR'
DOWN_RIGHT = 'DR'
DOWN_LEFT = 'DL'
UP_LEFT = 'UL'

STEPS = {
    UP:     Step(delta_x =  0, delta_y =  1),
    RIGHT:  Step(delta_x =  1, delta_y =  0),
    DOWN:   Step(delta_x =  0, delta_y = -1),
    LEFT:   Step(delta_x = -1, delta_y =  0),

    UP_RIGHT:   Step(delta_x =  1, delta_y =  1),
    DOWN_RIGHT: Step(delta_x =  1, delta_y = -1),
    DOWN_LEFT:  Step(delta_x = -1, delta_y = -1),
    UP_LEFT:    Step(delta_x = -1, delta_y =  1)
}

MAX_TAIL_DIST = 1
class Head:
    def __init__(self, tail: Tail):
        self.x = self.y = 0
        self.tail = tail

    def move(self, move: Move) -> None:
        step = STEPS[move.direction]
        for i in range(move.magnitude):
            self.step(step)

    def step(self, step: Step) -> None:
        # step
        self.x += step.delta_x
        self.y += step.delta_y
        tail_step = None
        self.tail.step(tail_step)

    def tail_too_far_right(self) -> bool:
        return self.tail.x - self.x > MAX_TAIL_DIST

    def tail_too_far_left(self) -> bool:
        return self.tail.x - self.x < -1*MAX_TAIL_DIST
    
    def tail_too_far_down(self) -> bool:
        return self.tail.y - self.tail.y < -1*MAX_TAIL_DIST

    def tail_too_far_up(self) -> bool:
        return self.tail.y - self.tail.y > MAX_TAIL_DIST

    def tail_same_hor(self) -> bool:
        return self.tail.x == self.x
    
    def tail_same_ver(self) -> bool:
        return self.tail.y == self.y
    

    def tail_too_far_straight_right(self) -> Step:
        return STEPS[LEFT] if (
            self.tail_too_far_right()
            and 
            self.tail_same_ver()
        ) else None 
    
    def tail_too_far_straight_down(self) -> Step:
        return STEPS[UP] if (
            self.tail_same_hor()
            and
            self.tail_too_far_down()
        ) else None
    
    def tail_too_far_straight_left(self) -> Step:
        return STEPS[RIGHT] if (
            self.tail_too_far_left()
            and
            self.tail_same_ver()
        ) else None

    def tail_too_far_straight_up(self) -> Step:
        return STEPS[DOWN] if (
            self.tail_same_hor()
            and
            self.tail_too_far_up()
        ) else None

    def tail_1_right(self) -> bool:
        return self.tail.x - self.x == 1
    
    def tail_1_up(self) -> bool:
        return self.tail.y - self.y == 1
    
    def tail_1_left(self) -> bool:
        return self.tail.x - self.x == -1

    def tail_1_down(self) -> bool:
        return self.tail.y - self.y == -1
    
    def tail_too_far_up_right(self) -> Step:
        return STEPS[DOWN_LEFT] if (
            (
                self.tail_too_far_up()
                and
                self.tail_1_right()
            )
            or
            (
                self.tail_1_up()
                and
                self.tail_too_far_right()
            )
        ) else None

    def tail_too_far_down_right(self) -> Step:
        return STEPS[UP_LEFT] if (
            (
                self.tail_too_far_down()
                and
                self.tail_1_right()
            )
            or
            (
                self.tail_1_down()
                and
                self.tail_too_far_right()
            )
        ) else None
    
    def tail_too_far_down_left(self) -> Step:
        return STEPS[UP_RIGHT] if (
            (
                self.tail_too_far_down()
                and
                self.tail_1_left()
            )
            or
            (
                self.tail_1_down()
                and
                self.tail_too_far_left()
            )
        ) else None
    
    def tail_too_far_up_left(self) -> Step:
        return STEPS[DOWN_RIGHT] if (
            (
                self.tail_too_far_up()
                and
                self.tail_1_left()
            )
            or
            (
                self.tail_1_up()
                and
                self.tail_too_far_left()
            )
        ) else None


class Tail: 
    def __init__(self):
        self.x = self.y = 0
        self.history = set()
        self.update_history()
    
    def step(self, step: Step) -> None:
        self.x += step.delta_x
        self.y += step.delta_y
        self.update_history()
    
    def update_history(self) -> None:
        self.history.add((self.x, self.y))

    def num_spots_visited(self) -> int:
        return len(self.history)

DIR_INDEX = 0
MAGNITUDE_INDEX = 'OMFG'
def get_moves(filename='day-9-2/input.txt') -> None:
    with open(filename) as f:
        return []