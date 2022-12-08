from typing import List, Dict
import re
from pprint import pprint
_BOTTOM_OF_STACKS_LINE = 8
'''_STACK_TO_COL = {
    1: 1,  # 1 + 4(1-1)
    2: 5,  # 1 + 4(2-1)
    3: 9,  # 1 + 4(3-1)
}'''
_FIRST_STACK_COL = 1
_FIRST_STACK = 1
_FINAL_STACK = 9
_DISTANCE_BTWN_STACKS = 4
_STACK_TO_COL = {
    i: _FIRST_STACK_COL + _DISTANCE_BTWN_STACKS*(i-_FIRST_STACK)
    for i in range(_FIRST_STACK, _FINAL_STACK+1)
}
def get_stacks() -> Dict[int, list]:
    with open('input.txt') as f:
        lines = f.readlines()
    # interestingly, if we don't convert stack_lines to a list, this breaks
    # we'd return {1: ['P', 'F', 'M', 'Q', 'W', 'G', 'R', 'T'], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    # seems `for line in stack_lines` doesn't work as expected if we keep stack_lines as just the reverse iterator...
    stack_lines = list(reversed(lines[:_BOTTOM_OF_STACKS_LINE]))
    # this isn't the most efficient way given how caches work, but it's kinda neat?
    # the more efficient way would be to go row-by-row rather than col-by-col
    # (since accessing location x in memory will load x through x+y into the cache)
    # we also unnecessarily continue searching past the first ' ' in each line
    stacks = {
        stack_num: [
            line[_STACK_TO_COL[stack_num]] 
            for line in stack_lines 
            if line[_STACK_TO_COL[stack_num]] != ' '
        ]
        for stack_num in range(_FIRST_STACK, _FINAL_STACK+1)
    }
    return stacks


_FIRST_MOVE_LINE = 11
def get_moves() -> List[tuple]:
    with open('input.txt') as f:
        lines = f.readlines()
    move_lines = lines[_FIRST_MOVE_LINE-1:]
    return [tuple(map(lambda num_str: int(num_str), re.findall('\d+', line))) for line in move_lines]

# indices for the tuples returned by get_moves()
_NUM_CRATES_TO_MOVE= 0
_FROM_STACK = 1
_TO_STACK = 2


def _execute_move(stacks: dict, move: tuple) -> None:
    # Not gonna do any fancy list comprehension stuff here
    # because (1) - lazy, (2) - this code more natually follows the story given
    # about an elf literally moving crates from a stack to another stack
    from_stack = stacks[move[_FROM_STACK]]
    to_stack = stacks[move[_TO_STACK]]
    for i in range(move[_NUM_CRATES_TO_MOVE]):
        crate = from_stack.pop()
        to_stack.append(crate)



if __name__ == '__main__':
    stacks = get_stacks()
    assert stacks[1] == ['P', 'F', 'M', 'Q', 'W', 'G', 'R', 'T']
    assert stacks[2] == ['H', 'F', 'R']
    moves = get_moves()
    assert moves[0][_NUM_CRATES_TO_MOVE] == 3
    assert moves[1][_NUM_CRATES_TO_MOVE] == 2
    assert moves[0][_FROM_STACK] == 8
    assert moves[0][_TO_STACK] == 9
    for move in moves:
        if len(move) != 3:
            raise Exception(f'{move} is not of len 3')
    '''_execute_move(stacks, moves[0])
    print(stacks[8])
    assert stacks[8] == ['F']'''
    for move in moves:
        _execute_move(stacks, move)
    print(stacks)
    print(''.join([stacks[i][len(stacks[i])-1] for i in range(1, _FINAL_STACK+1)]))

    
