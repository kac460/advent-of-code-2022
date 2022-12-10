from __future__ import annotations
class Directory:
    def __init__(self, parent_dir: Directory, name: str):
        self.parent_dir = parent_dir
        self.child_dirs = {}
        self.files = []
        # name is purely for debugging purposes
        self.name = name
        self.cached_size = None
    
    def add_child_dir(self, dir_name: str) -> None:
        self.child_dirs[dir_name] = (Directory(self, dir_name))

    def add_file(self, file_size: int) -> None: 
        self.files.append(file_size)

    def get_child_dirs(self) -> list:
        return list(self.child_dirs.values())

    def get_descendant_dirs(self) -> list:
        # unpacking is not allowed in list comprehensions :(
        # return self.get_child_dirs() + [*dir.get_descendant_dirs() for dir in self.get_child_dirs()]
        child_dirs = self.get_child_dirs()
        descendant_dirs = child_dirs
        for child_dir in child_dirs:
            descendant_dirs += child_dir.get_descendant_dirs()
        # i'm not sure where the duplicates came from...
        return list(set(descendant_dirs))

    def size(self) -> int:
        if self.cached_size is not None:
            return self.cached_size
        self.cached_size = sum(self.files) + sum([child_dir.size() for child_dir in self.get_child_dirs()])
        print(f'{self.name} size is {self.cached_size}')
        return self.cached_size

    # Processes the line, returning the new current Directory (could just be this Directory)
    def process_line(self, line: str) -> Directory:
        line_split = line.split()
        arg_0 = line_split[0]
        arg_1 = line_split[1]
        if arg_0 == '$':
            if arg_1 == 'cd':
                arg_2 = line_split[2]
                dir_to_enter = arg_2
                if dir_to_enter == '..':
                    return self.parent_dir
                return self.child_dirs[dir_to_enter]
            if arg_1 == 'ls':
                # nothing to do in this case
                return self
            raise Exception(f'Expected either cd or ls after $ but got {line}')
        if arg_0 == 'dir':
            dir_name = arg_1
            self.add_child_dir(dir_name)
            return self
        if arg_0.isnumeric():
            file_size = int(arg_0)
            self.add_file(file_size)
            return self
        raise Exception(f'Expected either $, dir, or an int, but got {line}')


def _get_lines(filename: str) -> list:
    with open(filename) as f:
        return f.readlines()


def populate_directory_tree(filename: str = 'input.txt') -> Directory:
    lines = _get_lines(filename)
    root_dir = Directory(None, '/')
    current_dir = root_dir
    # we can ignore the first 'cd /' because that is essentially what current_dir is
    for line in lines[1:]:
        current_dir = current_dir.process_line(line)
    return root_dir


# excludes root_dir
def sum_dir_sizes_matching_condition(root_dir: Directory, condition: callable) -> int:
    for dir in root_dir.get_descendant_dirs():
        print(f'{dir.name} size: {dir.size()}, matches: {condition(dir)}')
    return sum([dir.size() for dir in root_dir.get_descendant_dirs() if condition(dir)])


# this actually isn't what's being asked for...
def get_total_size() -> int:
    root_dir = populate_directory_tree()
    return root_dir.size()


if __name__ == '__main__':
    root_dir = populate_directory_tree()
    _MAX_DIR_SIZE = 100000
    condition = lambda dir: dir.size() <= _MAX_DIR_SIZE
    print(sum_dir_sizes_matching_condition(root_dir, condition))