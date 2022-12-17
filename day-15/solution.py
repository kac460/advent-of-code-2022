from __future__ import annotations
from collections import namedtuple
from copy import copy
import re

Position = namedtuple('Position', 'x y')
def manhattan_distance(pos_1: Position, pos_2: Position) -> int:
    return abs(pos_1.x - pos_2.x) + abs(pos_1.y - pos_2.y)

_S_X = 2
_S_Y = 3
_B_X = 8
_B_Y = 9
def get_sensors(filename: str = 'day-15/input.txt') -> dict[Position, Position]:
    with open(filename) as f:
        lines = [re.split(':\s|\s|,\s', line.strip()) for line in f.readlines()]
    sensors = dict()
    get_coord = lambda s: int(s.split('=')[1])
    for line in lines:
        s_x = get_coord(line[_S_X])
        s_y = get_coord(line[_S_Y])
        sensor = Position(s_x, s_y)
        b_x = get_coord(line[_B_X])
        b_y = get_coord(line[_B_Y])
        beacon = Position(b_x, b_y)
        sensors[sensor] = beacon
    return sensors


def get_sensor_max_distances(sensors: dict[Position, Position]) -> dict[Position, int]:
    return {
        sensor: manhattan_distance(sensor, beacon)
        for sensor, beacon in sensors.items()
    }


def get_max_x(sensor_max_distances: dict[Position, int]):
    max_manhattan_distance = max(dist for dist in sensor_max_distances.values())
    return max(
        sensor.x + max_manhattan_distance 
        for sensor in sensor_max_distances
    )
def get_min_x(sensor_max_distances: dict[Position, int]):
    max_manhattan_distance = max(dist for dist in sensor_max_distances.values())
    return min(
        sensor.x - max_manhattan_distance
        for sensor in sensor_max_distances
    )

# return {(x1, x2) | no beacon can exist between x1 and x2 inclusive}
def get_invalid_ranges(
    sensor_max_distances: dict[Position, int], 
    y: int
) -> set[tuple[int, int]]:
    invalid_positions = set()
    for sensor, md in sensor_max_distances.items():
        y_dist = abs(sensor.y - y)
        md_minus_y_dist = md - y_dist
        if md_minus_y_dist >= 0:
            min_invalid_x = sensor.x - md_minus_y_dist
            max_invalid_x = sensor.x + md_minus_y_dist
            invalid_positions.add((min_invalid_x, max_invalid_x))
    return invalid_positions


def merge_ranges(ranges: set[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges = sorted([[range[_MIN], range[_MAX]] for range in ranges])
    stack = []
    stack.append(ranges[0])
    for range in ranges:
        if stack[-1][_MIN] <= range[_MIN] <= stack[-1][_MAX]:
            stack[-1][_MAX] = max(stack[-1][_MAX], range[_MAX])
        else:
            stack.append(range)
    return stack

_MIN = 0
_MAX = 1
def get_num_invalid_positions(
    invalid_ranges: set[tuple[int, int]],
    y: int,
    beacons: set[Position]
) -> int:
    non_ovelapping = merge_ranges(invalid_ranges)
    num_beacons_in_range = 0
    for beacon in beacons:
        if beacon.y == y:
            for r in non_ovelapping:
                if r[_MIN] <= beacon.x and r[_MAX] >= beacon.x:
                    num_beacons_in_range += 1
    return sum(r[_MAX] - r[_MIN] for r in non_ovelapping) + 1 - num_beacons_in_range
        

def find_beacon(sensor_max_distances: dict[Position, int], max_pos: int) -> Position:
    for y in range(0, max_pos + 1):
        ranges = get_invalid_ranges(sensor_max_distances, y)
        non_overlapping = merge_ranges(ranges)
        if len(non_overlapping) > 1:
            non_overlapping = sorted(non_overlapping)
            x =  non_overlapping[0][_MAX] + 1
            return Position(x, y)
    raise Exception('beacon not located')



'''def get_invalid_beacon_cols_for_row(sensor_max_distances: dict[Position, int], beacons: set[Position], y: int, min_x: int, max_x: int) -> set[int]:
    invalid_positions = set()
    positions_to_check = {x for x in range(min_x, max_x + 1) if Position(x,y) not in beacons}
    for sensor, md in sensor_max_distances.items():
        new_invalid_positions = set()
        for x in positions_to_check:
            if md >= manhattan_distance(sensor, Position(x, y)):
                new_invalid_positions.add(x)
        invalid_positions.update(new_invalid_positions)
        positions_to_check.difference_update(new_invalid_positions)
    return invalid_positions'''

_TEST = False
if __name__ == '__main__':
    if _TEST:
        _y = 11
        _file = 'day-15/test.txt'
        _max_pos = 20
    else:
        _y = 2000000
        _file = 'day-15/input.txt'
        _max_pos = 4000000
    _sensors = get_sensors(_file)
    _beacons = {beacon for beacon in _sensors.values()}
    _sensor_max_distances = get_sensor_max_distances(_sensors)
    _invalid_ranges = get_invalid_ranges(
        _sensor_max_distances,
        _y
    )
    _num_invalid_positions = get_num_invalid_positions(_invalid_ranges, _y, _beacons)
    print('PART 1')
    print(_num_invalid_positions)
    print('---')
    print('PART 2')
    _beacon = find_beacon(_sensor_max_distances, _max_pos)
    print(_beacon)
    print(4000000*_beacon.x + _beacon.y)


# For any x, y
# For each sensor (s_x, s_y) with closest beacon (b_x, b_y):
# If y in between s_y and b_y:
#   if manhattan_distance((x, y), (b_x, b_y) > manhattan_distance((x, y), (s_x, s_y)) ):
#       (x, y) must have no beacon




