from part_1_solution import (
    get_stacks, 
    get_moves,
    print_top_of_stacks,
    NUM_CRATES_TO_MOVE,
    FROM_STACK,
    TO_STACK
)

def _execute_move(stacks: dict, move: tuple) -> None:
    from_stack = stacks[move[FROM_STACK]]
    to_stack = stacks[move[TO_STACK]]
    num_crates_to_move = move[NUM_CRATES_TO_MOVE]
    bottom_crate_index = len(from_stack) - num_crates_to_move
    to_stack += from_stack[bottom_crate_index:]
    from_stack[:] = from_stack[:bottom_crate_index]

if __name__ == '__main__':
    stacks = get_stacks()
    moves = get_moves()
    '''print('old')
    print(stacks)
    _execute_move(stacks, (3, 8, 9))
    print('new')
    print(stacks)
    print_top_of_stacks(stacks)'''
    for move in moves:
        _execute_move(stacks, move)
    print_top_of_stacks(stacks)
