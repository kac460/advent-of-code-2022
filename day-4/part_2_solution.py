'''
It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the number of pairs that overlap at all.

In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap, while the remaining four pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:

    5-7,7-9 overlaps in a single section, 7.
    2-8,3-7 overlaps all of the sections 3 through 7.
    6-6,4-6 overlaps in a single section, 6.
    2-6,4-8 overlaps in sections 4, 5, and 6.

So, in this example, the number of overlapping assignment pairs is 4.

In how many assignment pairs do the ranges overlap?
'''

from part_1_solution import (
    get_pairs, 
    min_max,
)


def num_in_range(num: int, lower: int, upper: int):
    return num >= lower and num <= upper



def sections_overlap(sec_1: str, sec_2: str):
    sec_1_range = min_max(sec_1)
    sec_2_range = min_max(sec_2)
    for bound in sec_1_range:
        if num_in_range(bound, *sec_2_range):
            return True
    for bound in sec_2_range:
        if num_in_range(bound, *sec_1_range):
            return True
    return False


def cnt_pairs_with_overlapping_sections(pairs):
    return sum(1 for pair in pairs if sections_overlap(*pair))

if __name__ == '__main__':
    assert num_in_range(1, 0, 5)
    assert not num_in_range(1, 2, 5)
    assert sections_overlap('2-4', '3-5')
    assert sections_overlap('2-4', '4-5')
    assert not sections_overlap('2-4', '5-6')
    pairs = get_pairs()
    print(f'PART 2: cnt_pairs_with_overlapping_sections = {cnt_pairs_with_overlapping_sections(pairs)}')