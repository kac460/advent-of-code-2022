from __future__ import annotations
from typing import Union
from functools import cmp_to_key

_FILENAME = 'day-13/input.txt'
def get_pairs() -> list[tuple[list, list]]:
    with open(_FILENAME) as f:
        lines = list(map(lambda line: line[:len(line)-1], f.readlines()))
    pairs = []
    final_left_index = len(lines) - 2
    for i in range(0, final_left_index + 1, 3):
        left = eval(lines[i])
        right = eval(lines[i+1])
        pairs.append((left, right))
    return pairs

def pair_in_right_order(left: Union[list, int] , right: Union[list, int]) -> bool:
    #print(f'Compare {left} vs. {right}')
    # reached a base case, cannot go any further deeper
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            #print('Left side is smaller, so inputs are in right order')
            return -1
        if left > right:
            #print('Right side is smaller, so inputs are not in right order')
            return 1
        return 0
    if isinstance(left, list) and isinstance(right, list):
        index = 0
        while True:
            # base case: left ran out of items first
            if index >= len(left) and index < len(right):
                #print('Left side ran out of items, so inputs are in right order')
                return -1
            # base case: right ran out of items first
            if index < len(left) and index >= len(right):
                #print('Right side ran out of items, so inputs are not in right order')
                return 1
            # base case: no more items in either
            if index >= len(left) and index >= len(right):
                return 0
            left_item = left[index]
            right_item = right[index]
            # if left_item and right_item are both ints, this seems right
            # if left_item and right_item are both lists, we start comparison at index 0
            #   seems right
            right_order = pair_in_right_order(left_item, right_item)
            if right_order != 0:
                return right_order
            index += 1

    if isinstance(left, int): # right is a list
        left = [left]
        return pair_in_right_order(left, right)
    if isinstance(right, int): # left is a list
        right = [right]
        return pair_in_right_order(left, right)
    raise Exception("Didn't expect to get here")
    
def get_pair_indices_in_right_order(pairs: list[tuple]) -> list[int]:
    return [
        i+1
        for i in range(len(pairs))
        if pair_in_right_order(*pairs[i]) == -1
    ]

if __name__ == '__main__':
    print('PART 1')
    pairs = get_pairs()
    pair_indices_in_right_order = get_pair_indices_in_right_order(pairs)
    print(sum(pair_indices_in_right_order))
    print('-----')
    print('PART 2')
    div_1 = [[2]]
    div_2 = [[6]]
    all_packets = [div_1, div_2]
    for pair in pairs:
        all_packets.append(pair[0])
        all_packets.append(pair[1])
    # idk why it's the wrong way around but oh well lol
    sorted_packets = sorted(all_packets, key=cmp_to_key(pair_in_right_order))
    div_1_index = sorted_packets.index(div_1) + 1
    div_2_index = sorted_packets.index(div_2) + 1
    print(div_1_index*div_2_index)
