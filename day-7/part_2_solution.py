from part_1_solution import (
    populate_directory_tree, get_total_size
)
_MIN_UNUSED_SPACE = 30000000
_TOTAL_SPACE = 70000000
if __name__ == '__main__':
    root_dir = populate_directory_tree('input.txt')
    free_space = _TOTAL_SPACE - root_dir.size()
    min_size_to_delete = _MIN_UNUSED_SPACE - free_space
    candidates = set([root_dir.size()]).union(
        [
            descendant_dir.size() 
            for descendant_dir in root_dir.get_descendant_dirs()
            if descendant_dir.size() >= min_size_to_delete 
        ]
    )
    print(min(candidates))

    