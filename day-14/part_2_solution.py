from __future__ import annotations
from typing import Optional
from part_1_solution import (
    get_map,
    FILENAME,
    SAND_SOURCE_POS,
    SAND_SOURCE,
    SAND,
    ROCK,
    EMPTY
)

def get_correct_map(filename=FILENAME) -> list[list[str]]:
    old_map = get_map(filename)
    width = len(old_map[0])
    return old_map + [
        [EMPTY for _ in range(width)],
        [ROCK for _ in range(width)]
    ]


def add_column_left(cave_map: list[list[str]]) -> list[list[str]]:
    old_width = len(cave_map[0])
    cave_map[:] = [
        [EMPTY] + old_row
        for old_row in cave_map[:len(cave_map)-1]
    ] + [[ROCK for _ in range(old_width + 1)]]

def add_column_right(cave_map: list[list[str]]) -> None:
    old_width = len(cave_map[0])
    cave_map[:] = [
        old_row + [EMPTY]
        for old_row in cave_map[:len(cave_map)-1]
    ] + [[ROCK for _ in range(old_width + 1)]]


# Return False if cannot add anymore after this
def drop_sand(cave_map: list[list[str]]) -> bool:
    x = cave_map[0].index(SAND_SOURCE)
    y = 0
    # if the sand wants to go to an out of bounds spot
    # then it will fall into the abyss
    while True:
        # go down if possible
        if cave_map[y+1][x] == EMPTY:
            y += 1
        # go down left if possible
        elif x - 1 < 0:
            add_column_left(cave_map)
        elif cave_map[y+1][x-1] == EMPTY:
            y += 1
            x -= 1
        # go down right if possible
        elif x + 1 >= len(cave_map[0]):
            add_column_right(cave_map)
        elif cave_map[y+1][x+1] == EMPTY:
            y += 1
            x += 1
        # if we made it here we can't go any farther down
        else:
            # i know this could be more concise but this is more readable to me
            cave_map[y][x] = SAND
            if y == 0:
                # we couldn't even drop 1 down so we're at the source
                return False
            return True
    

def test_map():
    cave_map = get_correct_map('day-14/test.txt')
    def print_map():
        print('---')
        for row in cave_map:
            print(''.join(row[488:]))
        print()
    print_map()
    add_column_left(cave_map)
    print_map()
    add_column_right(cave_map)
    print_map()
    cnt = 0
    while drop_sand(cave_map):
        cnt += 1
        if cnt == 100:
            print('here')
        #print_map()
    cnt += 1
    print(cnt)

if __name__ == '__main__':
    #test_map()
    cave_map = get_correct_map()
    cnt = 0
    while drop_sand(cave_map):
        cnt += 1
    cnt += 1
    print(cnt)
