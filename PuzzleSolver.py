import itertools as it
indices = [0,1,2,3,4,5,6,7,8]

class PuzzleSolver:
    def __init__(self,puzzle):
        self._p = puzzle
        self.init_set()

    def init_set(self):
        return
        self._s = set()
        for x,y in it.product(indices,indices):
            if is_solved_square(x,y):
                self._s.add((x,y))

    def get_next(self):
        return self._s.pop()

    def solve(self):
        iterCount = 1
        while True:
            try:
                x,y = self.get_next()
                self.simplify(x,y)
            except KeyError:
                if self._p.is_solved():
                    return
                else:
                    iterCount += 1
                    # smart check
                    self.deep_check()
                    if not iterCount % 5:
                        self._p = self.take_a_chance()

    def deep_check(self):
        pass

    def take_a_chance(self,first=True):
        # conditional solve
        q = set()
        _x,_y = self.find_pair()
        if _x is None or _y is None:
            print("Couldn't find any possibly pairs")
            exit()
        _p = copy.deepcopy(self._p)


        pass

    def find_pair(self):
        for x,y in it.product(indices,indices):
            if self._p.is_solved_square(x,y):
            elif self._p.num_possibilities(x,y) == 2:
                return x,y
        return None,None


    def simplify(self,x,y):
