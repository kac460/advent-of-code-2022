from typing import List
class MyTable():
    def __init__(self):
        self._table = [[[None, None, None, None]]*3]*4

    def __getitem__(self, row: int) -> List[List[int]]:
        return self._table[row]

    def __len__(self) -> int:
        return len(self._table)

    def test(self):
        print(self[0])
        print(len(self))
        # self[0] = 'foo' -> need __setitem__ but don't need this for this problem
        print(self._table)

t = MyTable()
print(t[0])
print(t[0][0])
print(t[0][0][1])
t.test()
print(t[1:])