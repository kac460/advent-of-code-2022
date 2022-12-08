'''Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is, a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.

For example, suppose you have the following list of contents from six rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

    The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means its first compartment contains the items vJrwpWtwJgWr, while the second compartment contains the items hcsFMMfFFhFp. The only item type that appears in both compartments is lowercase p.
    The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL. The only item type that appears in both compartments is uppercase L.
    The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
    The fourth rucksack's compartments only share item type v.
    The fifth rucksack's compartments only share item type t.
    The sixth rucksack's compartments only share item type s.

To help prioritize item rearrangement, every item type can be converted to a priority:

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.

In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?'''

LOWER_A_PRIORITY = 1
LOWER_PRIORITY_OFFSET = ord('a') - LOWER_A_PRIORITY
UPPER_A_PRIORITY = 27
UPPER_PRIORITY_OFFSET = ord('A') - UPPER_A_PRIORITY

def priority(item: str) -> int:
    ascii_val = ord(item)
    if item.isupper():
        return ascii_val - UPPER_PRIORITY_OFFSET
    else:
        return ascii_val - LOWER_PRIORITY_OFFSET

def duplicate_item(rucksack: str) -> str:
    compartment_2_start = int(len(rucksack)/2)
    compartment_1 = set(rucksack[:compartment_2_start])
    compartment_2 = set(rucksack[compartment_2_start:])
    return compartment_1.intersection(compartment_2).pop()


def sum_duplicates_priorities(rucksacks: list) -> str:
    return sum([priority(duplicate_item(rucksack)) for rucksack in rucksacks])


def get_rucksacks() -> list:
    with open('input.txt') as f:
        return list(map(lambda line: line.strip(), f.readlines()))


if __name__ == '__main__':
    assert priority('a') == 1
    assert priority('c') == 3
    assert priority('A') == 27
    assert priority('Z') == 52
    assert duplicate_item('vJrwpWtwJgWrhcsFMMfFFhFp') == 'p'

    rucksacks = get_rucksacks()
    total_duplicate_priorities = sum_duplicates_priorities(rucksacks)
    print(f'PART 1 total_duplicate_priorities = {total_duplicate_priorities}')
    print('----')



