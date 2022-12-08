'''
Every Elf carries a badge that identifies their group. For efficiency, within each group of three Elves, the badge is the only item type carried by all three Elves. That is, if a group's badge is item type B, then all three Elves will have item type B somewhere in their rucksack, and at most two of the Elves will be carrying any other item type.

The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the badges need to be pulled out of the rucksacks so the new authenticity stickers can be attached.

Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which item type is the right one is by finding the one item type that is common between all three Elves in each group.

Every set of three lines in your list corresponds to a single group, but each group can have a different badge item type. So, in the above example, the first group's rucksacks are the first three lines:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg

And the second group's rucksacks are the next three lines:

wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

In the first group, the only item type that appears in all three rucksacks is lowercase r; this must be their badges. In the second group, their badge item type must be Z.

Priorities for these items must still be found to organize the sticker attachment efforts: here, they are 18 (r) for the first group and 52 (Z) for the second group. The sum of these is 70.

Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?
'''
from part_1_solution import get_rucksacks, priority


def badge(rucksack_1: str, rucksack_2: str, rucksack_3: str) -> str:
    return set(rucksack_1).intersection(rucksack_2, rucksack_3).pop()


ELF_GROUP_SIZE = 3
def sum_badge_priorities(rucksacks):
    total = 0
    for i in range(0, len(rucksacks), ELF_GROUP_SIZE):
        group = rucksacks[i:i+ELF_GROUP_SIZE]
        print(f'group: {group}')
        group_badge = badge(*group)
        print(f'group_badge: {group_badge}, priority({group_badge}) = {priority(group_badge)}')
        total += priority(group_badge)
        print(f'total: {total}')
    return total


if __name__ == '__main__':
    test_rucksack_1 = 'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn'
    test_rucksack_2 = 'ttgJtRGJQctTZtZT'
    test_rucksack_3 = 'CrZsJsPPZsGzwwsLwLmpwMDw'
    assert badge(test_rucksack_1, test_rucksack_2, test_rucksack_3) == 'Z'
    rucksacks = get_rucksacks()
    badge_priorities_total = sum_badge_priorities(rucksacks)
    
    print(f'PART 2: badge_priorities_total = {badge_priorities_total}')
