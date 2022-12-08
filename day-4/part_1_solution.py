'''
Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been assigned the job of cleaning up sections of the camp. Every section has a unique ID number, and each Elf is assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each other, they've noticed that many of the assignments overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8

For the first few pairs, this list means:

    Within the first pair of Elves, the first Elf was assigned sections 2-4 (sections 2, 3, and 4), while the second Elf was assigned sections 6-8 (sections 6, 7, 8).
    The Elves in the second pair were each assigned two sections.
    The Elves in the third pair were each assigned three sections: one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.

This example list uses single-digit section IDs to make it easier to draw; your actual list might contain larger numbers. Visually, these pairs of section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8

Some of the pairs have noticed that one of their assignments fully contains the other. For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6. In pairs where one assignment fully contains the other, one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem like the most in need of reconsideration. In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?
'''

def get_pairs() -> list:
    with open('input.txt') as f:
        return [line.strip().split(',') for line in f.readlines()]


MIN_INDEX = 0
MAX_INDEX = 1
def min_max(section_range: str) -> tuple:
    section_range = section_range.split('-')
    return int(section_range[MIN_INDEX]), int(section_range[MAX_INDEX])


def section_contains_other(sec_1: str, sec_2: str) -> bool:
    sec_1_range = min_max(sec_1)
    sec_2_range = min_max(sec_2)
    if sec_1_range[MIN_INDEX] == sec_2_range[MIN_INDEX] or sec_1_range[MAX_INDEX] == sec_2_range[MAX_INDEX]:
        return True
    
    if sec_1_range[MIN_INDEX] < sec_2_range[MIN_INDEX]:
        range_with_lower_min = sec_1_range
        range_with_higher_min = sec_2_range
    else:
        range_with_lower_min = sec_2_range
        range_with_higher_min = sec_1_range
    # e.g. section_contains_other('35-93', '34-94') == True because 94 >= 93
    if range_with_lower_min[MAX_INDEX] > range_with_higher_min[MAX_INDEX]:
        print(f'{range_with_lower_min} contains {range_with_higher_min}')
        return True
    print(f'{range_with_lower_min} does NOT contain/is NOT contained by {range_with_higher_min}')
    return False

    
def cnt_pairs_where_one_range_contains_other(pairs: list):
    return sum(1 for pair in pairs if section_contains_other(*pair))


if __name__ == '__main__':
    pairs = get_pairs()
    assert pairs[:3] == [
        ['36-92', '35-78'], 
        ['26-31', '25-27'], 
        ['17-72', '16-71']
    ]
    assert min_max('36-92') == (36, 92)
    assert section_contains_other('35-93', '34-94')
    assert section_contains_other('34-94', '35-93')
    assert section_contains_other('35-93', '36-92')
    assert section_contains_other('36-92', '36-92')
    assert section_contains_other('35-93', '35-96')
    assert not section_contains_other('35-93', '36-96')
    total_very_bad_pairs = cnt_pairs_where_one_range_contains_other(pairs)
    print(f'PART 1: total_very_bad_pairs = {total_very_bad_pairs}')
