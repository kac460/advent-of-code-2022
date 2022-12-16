from __future__ import annotations
from collections import namedtuple

_FILENAME = 'day-14/test.txt'

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


_SAND_SOURCE = Position(500,0)

# each str is a single char
# can't just do a list of strs because they're immutable
def get_map() -> list[list[str]]:
    with open(_FILENAME) as f:
        lines = f.readlines()
    rock_positions = get_rock_positions(lines)
    width = max([pos.x for pos in rock_positions])
    height = max([pos.y for pos in rock_positions])
    rock_map = [
        [
            '#' if Position(x, y) in rock_positions
            else '.'
            for x in range(width+1)
        ]
        for y in range(height+1)
    ]
    rock_map[_SAND_SOURCE.y][_SAND_SOURCE.x] = '+'
    return rock_map


# Return the
def pos_of_sand_after_dropped(cave_map: list[list[str]]) -> Position:
    x = _SAND_SOURCE.x
    y = _SAND_SOURCE.y
    while True:
        # TODO - logic to find where sand ends up
        break
    # Return None if sand cannot fall (maybe goes before while loop)
    return None 
