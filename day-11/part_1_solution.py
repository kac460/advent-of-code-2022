from __future__ import annotations
import re
from queue import Queue
from math import floor, prod

class WhomstToThrowTo:
    def __init__(self, divisor: int, true_friend: int, false_friend: int):
        self._divisor = divisor
        self._true_friend = true_friend
        self._false_friend = false_friend

    def __call__(self, item: int) -> int:
        return self._true_friend if item % self._divisor == 0 else self._false_friend

_OLD = 'old'
class WorryOperation:
    def __init__(self, operator: str, operand: str):
        self._operator = operator
        self._operand = operand
    
    def __call__(self, item: int) -> int:
        if self._operand == _OLD:
            operand = item
        else:
            operand = int(self._operand)
        if self._operator == '*':
            new_worry = item * operand
        elif self._operator == '+':
            new_worry = item + operand
        else:
            raise ValueError(f'unsupported operand {self._operand}')
        return floor(new_worry /3)

class Monkey:
    def __init__(
        self, 
        id: int,
        friends: dict[int, Monkey], 
        starting_items: list[int],
        worry_operation: WorryOperation,
        whomst_to_throw_to: WhomstToThrowTo,
    ):
        friends[id] = self
        self._id = id
        self._friends = friends
        self._worry_operation = worry_operation
        self._whomst_to_throw_to = whomst_to_throw_to
        self._items = Queue()
        for item in starting_items:
            self._items.put(item)
        self.num_inspections = 0

    def catch(self, item: int) -> None:
        self._items.put(item)
    
    def throw(self) -> None:
        while not self._items.empty():
            self.num_inspections += 1
            item = self._items.get_nowait()
            #print(f'Monkey {self._id} inspecting {item}. inspection #{self.num_inspections}')
            to_monkey = self._friends[self._whomst_to_throw_to(item)]
            item = self._worry_operation(item)
            #print(f'Monkey {self._id} throwing {item} to {to_monkey._id}')
            to_monkey.catch(item)


def get_monkeys() -> dict[int, Monkey]:
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
                operation = WorryOperation(operator, operand)
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
    for round in range(_NUM_ROUNDS):
        for i in range(len(monkey_pals)):
            monkey_pals[i].throw()
    print(monkey_business(monkey_pals))

    