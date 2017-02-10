class PuzzleReader:
    def __init__(self,fp):
        with open(fp) as f:
            lines = f.readlines()
        self._lines = lines
        self._count = 0

    def get_next_puzzle(self):
        if self._count * 10 < len(self._lines):
            ls = self._lines[self._count*10 + 1 : (self._count + 1) * 10]
            self._count += 1
        else:
            raise Exception()
        return ls
