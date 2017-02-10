from PuzzleSolver import PuzzleSolver
from functools import reduce
sudoku_len = 9

def digit_rep(x):
    if x:
        return 2**(x-1)
    else:
        return 2**9 - 1

# use bit masking to determine what's up
# can use XOR

# can use ANDing to determine hits / containment


class Puzzle:
    def __init__(self,lines):
        self._solution = []
        self._original = []
        for line in lines:
            l = list(line.strip())
            self._original.append(l)
            self._solution.append([digit_rep(int(d)) for d in l])

    def get_entry(self,row,column):
        return self._solution[column][row]

    def num_possibilities(self,row,column):
        # logarithmic enumeration of digits maybe?
        num = self.get_entry(row,column)
        return sum(not not 2**n & num for n in range(sudoku_len))

    def is_solved(self):
        ##### fill this out

    def is_solved_square(self,row,column):
        return not (self.get_entry(row,column) & self.get_entry(row,column) - 1)

    def pretty_print(self):
        for col in range(sudoku_len):
            for row in range(sudoku_len):
                if self.is_solved_square(row,col):
                    print(self.get_entry(row,col).bit_length(),end=" ")
                else:
                    print(".",end=" ")
            print()
        print()

    def solve(self):
        ps = PuzzleSolver(self)
        pass

    def top_left_digits(self):
        return 0
#        return int("".join(str(s) for s in self._solution[0][0:3]))
