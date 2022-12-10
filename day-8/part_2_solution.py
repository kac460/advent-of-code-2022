from __future__ import annotations
from collections import namedtuple
from part_1_solution import get_height_grid
from math import prod

# screw it let's just do the obvious solution
# regrets were had
LEFT = 'L'
RIGHT = 'R'
DOWN = 'D'
UP = 'U'
Step = namedtuple('Step', 'vertical_step horizontal_step', defaults=(1, -1))
DIRECTIONS = {
    LEFT: Step(horizontal_step=-1),
    RIGHT: Step(horizontal_step=1),
    DOWN: Step(vertical_step=1),
    UP: Step(vertical_step=-1)
}

def viewing_distance_horizontal(
    height_grid: list[list[int]],
    row: int,
    col: int, 
    step: int
) -> int:
    if step != 1 and step!= -1:
        raise ValueError(f'step must be 1 or -1 but got {step}')
    if step == 1:
        final_col = len(height_grid[row]) -1
    else:
        final_col = 0
    cnt = 0
    for c in range(col+step, final_col+step, step):
        cnt += 1
        if height_grid[row][c] >= height_grid[row][col]:
            break
    if row == 7 and col == 48:
        print('here')
    return cnt


def viewing_distance_vertical(
    height_grid: list[list[int]],
    row: int,
    col: int, 
    step: int
) -> int:
    if step != 1 and step!= -1:
        raise ValueError(f'step must be 1 or -1 but got {step}')
    if step == 1:
        final_row = len(height_grid) -1
    else:
        final_row = 0
    cnt = 0
    for r in range(row+step, final_row+step, step):
        cnt += 1
        if height_grid[r][col] >= height_grid[row][col]:
            break
    if row == 7 and col == 48:
        print('here')
    return cnt


ViewingDistances = namedtuple('ViewingDistances', f'left right up down')
def viewing_distances(
    height_grid: list[list[int]],
    row: int,
    col: int
) -> ViewingDistances:
    viewing_distance_in_dir = lambda direction: viewing_distance_horizontal(
        height_grid=height_grid,
        row=row,
        col=col,
        step=DIRECTIONS[direction].horizontal_step
    ) if direction == LEFT or direction == RIGHT else viewing_distance_vertical(
        height_grid=height_grid,
        row=row,
        col=col,
        step=DIRECTIONS[direction].vertical_step
    )
    return ViewingDistances(
        left=viewing_distance_in_dir(LEFT),
        right=viewing_distance_in_dir(RIGHT),
        down=viewing_distance_in_dir(DOWN),
        up=viewing_distance_in_dir(UP)
    )

def scenic_score(
    height_grid: list[list[int]],
    row: int,
    col: int
) -> int:
    return prod(viewing_distances(height_grid, row, col))

TreeWithScore = namedtuple('TreeWithScore', 'r c score')

if __name__ == '__main__':
    height_grid = get_height_grid()
    trees_with_scores = [
        TreeWithScore(
            r=r, 
            c=c, 
            score=scenic_score(
                height_grid=height_grid,
                row=r,
                col=c
            )
        )
        for r in range(len(height_grid))
        for c in range(len(height_grid[0]))
    ]
    print(max(trees_with_scores, key=lambda tws: tws.score))

