from __future__ import annotations
from collections import namedtuple
from typing import Optional

FILENAME = 'day-14/input.txt'

Position = namedtuple('Position', 'x y')
def get_rock_line(pos_1: Position, pos_2: Position) -> set[Position]:
    if pos_1.x != pos_2.x:
        smaller_x = min(pos_1.x, pos_2.x)
        larger_x = max(pos_1.x, pos_2.x)
        return {Position(x, pos_1.y) for x in range(smaller_x, larger_x+1)}
    smaller_y = min(pos_1.y, pos_2.y)
    larger_y = max(pos_1.y, pos_2.y)
    return {Position(pos_1.x, y) for y in range(smaller_y, larger_y+1)}

def pos_str_to_position(pos_str: str) -> Position:
    coords = pos_str.split(',')
    return Position(int(coords[0]), int(coords[1]))

def get_rock_positions(file_lines: str) -> set[Position]:
    positions = set()
    for line in file_lines:
        line_positions = line.split(' -> ')
        for i in range(len(line_positions) -1):
            pos_1 = pos_str_to_position(line_positions[i])
            pos_2 = pos_str_to_position(line_positions[i+1])
            positions = positions.union(get_rock_line(pos_1, pos_2))
    return positions


SAND_SOURCE_POS = Position(500,0)
SAND_SOURCE = '+'
SAND = 'o'
ROCK = '#'
EMPTY = '.'
#_ABYSS = 'A'
_ABYSS_REACHED = 'A'
# each str is a single char
# can't just do a list of strs because they're immutable
def get_map(filename=FILENAME) -> list[list[str]]:
    with open(filename) as f:
        lines = f.readlines()
    rock_positions = get_rock_positions(lines)
    width = max([pos.x for pos in rock_positions])
    height = max([pos.y for pos in rock_positions])
    rock_map = [
        [
            ROCK if Position(x, y) in rock_positions
            else EMPTY
            for x in range(width+1)
        ]
        for y in range(height+1)
    ]
    rock_map[SAND_SOURCE_POS.y][SAND_SOURCE_POS.x] = SAND_SOURCE
    return rock_map


# returns _ABYSS_REACHED if about to fall into the abyss
# else places the sand in the right position and returns None
def drop_sand(cave_map: list[list[str]]) -> Optional[str]:
    x = SAND_SOURCE_POS.x
    y = SAND_SOURCE_POS.y
    # if the sand wants to go to an out of bounds spot
    # then it will fall into the abyss
    while y + 1 < len(cave_map):
        # go down if possible
        if cave_map[y+1][x] == EMPTY:
            y += 1
        # go down left if possible
        elif x - 1 < 0:
            return _ABYSS_REACHED
        elif cave_map[y+1][x-1] == EMPTY:
            y += 1
            x -= 1
        # go down right if possible
        elif x + 1 >= len(cave_map[0]):
            return _ABYSS_REACHED
        elif cave_map[y+1][x+1] == EMPTY:
            y += 1
            x += 1
        # if we made it here we can't go any farther down
        else:
            cave_map[y][x] = SAND
            return None
    return _ABYSS_REACHED
    
def test_map():
    cave_map = get_map('day-14/test.txt')
    def print_map():
        print([i for i in range(494, 504)])
        for row in cave_map:
            print(row[494:])
        print()
    cnt = 0
    while drop_sand(cave_map) != _ABYSS_REACHED:
        print_map()
        cnt += 1
    print(cnt)

if __name__ == '__main__':
    #test_map()
    cave_map = get_map()
    cnt = 0
    while drop_sand(cave_map) != _ABYSS_REACHED:
        cnt += 1
    print(cnt)
