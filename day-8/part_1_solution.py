from typing import List, Tuple, Set
# n = length--by num of trees--of an edge in the square grid 
# O(n^3) Naive solution:
#   For each i,j in Grid:
#    Traverse every dir (left/right/up/down) from i,j
#    If reach an edge of grid without finding taller tree,
#       visible[i,j] = true, break out of traversal procedure for i,j

# Heuristic optimization (still O(n^3)):
#   A tree is most likely to be visible from the closest edge given there's fewer trees in the way to that edge compared to the other edges
#   Therefore, it is most likely fastest to sort our traversal directions for each i,j by the distance to the relevant edge (e.g., if left edge is closest, traverse left first; then if not visible from left, traverse to the next closest edge; etc.)

# Q - can we traverse the whole grid only once (or at least a constant number of times)?
# Create a new table M
# M[i,j] = (tallest_l, tallest_r, tallest_u, tallest_d), where
#    tallest_l = tallest tree to left of Grid[i,j], 
#    tallest_r = tallest tree to right of Grid[i,j], 
#    etc.
# Calculate like this:
#   tallest_l = max(M[i, j-1][0], Grid[i, j-1])
#   if accessing a non-existent index, consider it to have height negative infinity


'''
30373
25512
65332
33549
35390
'''

def get_height_grid(filename: str ='day-8/input.txt') -> List[List[int]]:
    with open(filename) as f:
        lines = f.readlines()
        # want to remove the trailing \n -> [:len(line)-1]
        return [[int(tree) for tree in line[:len(line)-1]] for line in lines]


TALLEST_L = 0
TALLEST_R = 1
TALLEST_U = 2
TALLEST_D = 3
class TallestPerDirectionTable():
    def __init__(self, height_grid: List[List[int]]):
        self._height_grid = height_grid
        self._initialize_table()

    def _initialize_table(self):
        grid_width = len(self._height_grid[0])
        grid_height = len(self._height_grid)
        # Don't use [foo]*n because this results in the same object in memory
        # being used for every list (but they need to be distinct)
        self._table = [
            [
                [None, None, None, None] for c in range(grid_width)
            ]
            for r in range(grid_height)
        ]
        self._fill_table()

    def __getitem__(self, row: int) -> int:
        return self._table[row]

    def __len__(self) -> int:
        return len(self._table)

    def _fill_table(self) -> None:
        self._fill_tallest_ls()
        self._fill_tallest_rs()
        self._fill_tallest_ds()
        self._fill_tallest_us()

    def _fill_tallest_ls(self) -> None:
        for r in range(len(self)):
            # Fill left edge's tallest_ls with float('-inf')
            # Since there's nothing to their left
            self[r][0][TALLEST_L] = float('-inf')
            # traverse right from left edge + 1
            for c in range(1, len(self[0])):
                left = c - 1
                self[r][c][TALLEST_L] = max(
                    self[r][left][TALLEST_L],
                    self._height_grid[r][left]
                )
    
    def _fill_tallest_rs(self) -> None:
        right_edge_index = len(self[0]) - 1
        for r in range(len(self)):
            # Fill right edge's tallest_rs with float(-inf)
            # Since there's nothing to their right
            self[r][right_edge_index][TALLEST_R] = float('-inf')
            # Traverse left from right edge - 1
            for c in range(right_edge_index-1, -1, -1):
                right = c + 1
                self[r][c][TALLEST_R] = max(
                    self[r][right][TALLEST_R],
                    self._height_grid[r][right]
                )

    def _fill_tallest_us(self) -> None:
        for c in range(len(self[0])):
            # Fill upper edge's tallest_us with float(-inf)
            # Since there's nothing above them
            self[0][c][TALLEST_U] = float('-inf')
            # Traverse down from upper edge + 1
            for r in range(1, len(self)):
                up = r - 1
                self[r][c][TALLEST_U] = max(
                    self[up][c][TALLEST_U],
                    self._height_grid[up][c]
                )

    def _fill_tallest_ds(self) -> None: 
        lower_edge_index = len(self) - 1
        for c in range(len(self[0])):
            # Fill lower edge's tallest_ds with float(-inf)
            # Since there's nothing below them
            self[lower_edge_index][c][TALLEST_D] = float('-inf')
            # Traverse up from lower edge - 1
            for r in range(lower_edge_index-1, -1, -1):
                down = r + 1
                self[r][c][TALLEST_D] = max(
                    self[down][c][TALLEST_D],
                    self._height_grid[down][c]
                )


def get_visible_trees() -> Set[Tuple[int]]:
    height_grid = get_height_grid()
    tallest_per_direction_table = TallestPerDirectionTable(height_grid)
    return {
        (r, c) 
        for r in range(len(tallest_per_direction_table))
        for c in range(len(tallest_per_direction_table[0]))
        for direction in (TALLEST_L, TALLEST_R, TALLEST_D, TALLEST_U)
        if height_grid[r][c] > tallest_per_direction_table[r][c][direction]
    }
            

if __name__ == '__main__':
    visible_trees = get_visible_trees()
    print(visible_trees)
    assert (0,0) in visible_trees
    assert (2,2) not in visible_trees
    print(len(visible_trees))