import numpy as np
import math

ACTIONS = {
    'u': (1, 0),
    'd': (-1, 0),
    'l': (0, 1),
    'r': (0, -1)
}


class SlidingTilePuzzle():
    def __init__(self, n=4, weighted=False, puzzle=None, blank_row=-1, blank_col=-1, g=0, moves=0):
        self.n = n
        self.g = 0
        self.weighted = weighted
        self.moves = moves
        self._f = -1
        if puzzle is None:
            self._generate_random()
            while self.is_goal() or not self._is_solvable():
                self._generate_random()
        else:
            self.puzzle = puzzle
            self.blank_r = blank_row
            self.blank_c = blank_col
            self.g = g

    def _generate_random(self):
        tiles = np.array(range(self.n**2))
        np.random.shuffle(tiles)
        self.puzzle = tiles.reshape((self.n, self.n))
        br, bc = np.where(self.puzzle == 0)
        self.blank_r, self.blank_c = br[0], bc[0]

    def _is_solvable(self):
        pa = self.puzzle.reshape(-1)
        pa = np.delete(pa, self.blank_r * self.n + self.blank_c)

        inv = 0
        for i in range(pa.size - 1):
            for j in range(i + 1, pa.size):
                if pa[i] > pa[j]:
                    inv += 1

        if self.n % 2 == 0:
            if self.blank_r % 2 == 0:
                return inv % 2 == 0
            else:
                return inv % 2 == 1
        return inv % 2 == 0

    def is_goal(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.puzzle[i][j] != (i * self.n + j):
                    return False
        return True

    def copy_and_move(self, dir):
        sp = SlidingTilePuzzle(n=self.n,
                               weighted=self.weighted,
                               puzzle=self.puzzle.copy(),
                               blank_row=self.blank_r,
                               blank_col=self.blank_c,
                               g=self.g,
                               moves=self.moves)
        sp.move(dir)
        return sp

    def move(self, dir):
        self.moves += 1
        x, y = ACTIONS[dir]
        br, bc = self.blank_r, self.blank_c
        self.puzzle[br, bc], self.puzzle[br+x, bc +
                                         y] = self.puzzle[br+x, bc+y], self.puzzle[br, bc]
        self.blank_r += x
        self.blank_c += y
        self.g += 1 if not self.weighted else self.puzzle[br, bc]

    def get_children(self):
        if self.blank_r > 0:
            yield self.copy_and_move('d')
        if self.blank_r < (self.n - 1):
            yield self.copy_and_move('u')
        if self.blank_c > 0:
            yield self.copy_and_move('r')
        if self.blank_c < (self.n - 1):
            yield self.copy_and_move('l')

    def h_manh(self, w=False):
        h = 0
        for i in range(self.n):
            for j in range(self.n):
                v = self.puzzle[i, j]
                m = abs(v//self.n - i) + abs(v % self.n - j)
                h += m if not w else v * m
        return h

    def f(self, g=-1, w=False):
        if g > -1:
            self.g = g
            self._f == -1
        if self._f == -1:
            self._f = self.g + self.h_manh(w=w)
        return self._f

    def __eq__(self, other):
        for i in range(self.n):
            for j in range(self.n):
                if self.puzzle[i][j] != other.puzzle[i][j]:
                    return False
        return True

    def __lt__(self, other):
        return self.f() < other.f()

    def __str__(self):
        return str(self.puzzle)


if __name__ == '__main__':
    sp = SlidingTilePuzzle(n=2)
    print(sp)
    while True:
        if sp.is_goal():
            break
        c = input('Where to move? ')
        sp.move(c)
        print(sp)
