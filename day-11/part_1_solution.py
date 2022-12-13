from __future__ import annotations
import re
from collections import deque
from math import prod

class WhomstToThrowTo:
    def __init__(self, divisor: int, true_friend: int, false_friend: int):
        self.divisor = divisor
        self.true_friend = true_friend
        self.false_friend = false_friend

    def __call__(self, item: int) -> int:
        return self.true_friend if item % self.divisor == 0 else self.false_friend

_OLD = 'old'
class WorryOperation:
    def __init__(self, operator: str, operand: str, worry_reduction: int):
        self.operator = operator
        self.operand = operand
        self.worry_reduction = worry_reduction
    
    def __call__(self, item: int) -> int:
        if self.operand == _OLD:
            operand = item
        else:
            operand = int(self.operand)
        if self.operator == '*':
            new_worry = item * operand
        elif self.operator == '+':
            new_worry = item + operand
        else:
            raise ValueError(f'unsupported operand {self.operand}')
        if self.worry_reduction != 1:
            return new_worry // self.worry_reduction
        return new_worry

class Monkey:
    def __init__(
        self, 
        id: int,
        friends: dict[int, Monkey], 
        starting_items: deque[int],
        worry_operation: WorryOperation,
        whomst_to_throw_to: WhomstToThrowTo,
    ):
        friends[id] = self
        self._id = id
        self._friends = friends
        self._worry_operation = worry_operation
        self._whomst_to_throw_to = whomst_to_throw_to
        self._items = deque()
        for item in starting_items:
            self._items.append(item)
        self.num_inspections = 0

    def catch(self, item: int) -> None:
        self._items.append(item)
    
    def throw(self) -> None:
        while len(self._items) > 0:
            self.num_inspections += 1
            item = self._items.popleft()
            #print('Monkey 0:')
            #print(f'Inspecting {item}. inspection #{self.num_inspections}')
            item = self._worry_operation(item)
            to_monkey = self._friends[self._whomst_to_throw_to(item)]
            #print(f'Monkey {self._id} throwing {item} to {to_monkey._id}')
            to_monkey.catch(item)

    def __str__(self) -> str:
        return (
            f'Monkey {self._id}:\n'
            f'  Items: {", ".join([str(item) for item in self._items])}\n'
            f'  Operation: new = old {self._worry_operation.operator} {self._worry_operation.operand}\n'
            f'  Test: divisble by {self._whomst_to_throw_to.divisor}\n'
            f'  If true: throw to monkey {self._whomst_to_throw_to.true_friend}\n'
            f'  If false: throw to monkey {self._whomst_to_throw_to.false_friend}\n'
        )


def get_monkeys(worry_reduction: int = 3) -> dict[int, Monkey]:
    monkey_buddies = {}
    with open('day-11/input.txt') as f:
        lines = f.readlines()
        for line in lines:
            line_split = re.split('\s|,\s', line.strip())
            if line_split[0] == 'Monkey':
                # for real this time there's no double digit monkey ids
                id = int(line_split[1][0])
            elif line_split[0] == 'Starting':
                starting_items = list(
                    map(
                        lambda item: int(item),
                        line_split[2:]
                    )
                )
            elif line_split[0] == 'Operation:':
                operator = line_split[4]
                operand = line_split[5]
                operation = WorryOperation(operator, operand, worry_reduction)
            elif line_split[0] == 'Test:': 
                divisor = int(line_split[3])
            elif line_split[0] == 'If' and line_split[1] == 'true:':
                true_friend = int(line_split[5])
            elif line_split[0] == 'If':
                false_friend = int(line_split[5])
                whomst_to_throw_to = WhomstToThrowTo(divisor, true_friend, false_friend)
                Monkey(
                    id=id,
                    friends=monkey_buddies,
                    starting_items=starting_items,
                    worry_operation=operation,
                    whomst_to_throw_to=whomst_to_throw_to
                )
    return monkey_buddies

def monkey_business(monkey_buds: dict[int, Monkey]) -> int:
    return prod(
        list(
            sorted(
                [
                    monkey.num_inspections
                    for monkey in monkey_buds.values()
                ],
                reverse=True
            )
        )[:2]
    )

_NUM_ROUNDS = 20
if __name__ == '__main__':
    monkey_pals = get_monkeys()
    '''for monkey in monkey_pals.values():
        print(monkey)'''
    for round in range(_NUM_ROUNDS):
        for i in range(len(monkey_pals)):
            monkey_pals[i].throw()
        print(f'After round {round+1}, the monkeys are holding items with these worry levels: ')
        for i in range(len(monkey_pals)):
            print(f'Monkey {i}: {", ".join([str(item) for item in monkey_pals[i]._items])}')
        print('')
    print(monkey_business(monkey_pals))

    