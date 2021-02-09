from utils import SearchAlgorithm
from collections import deque
import math


class IDAstar(SearchAlgorithm):
    def __init__(self, weighted=False):
        super().__init__(weighted)

    def __search_iter(self, path, bound):
        self.exp += 1
        c = path[0]
        if c.f(w=self.weighted) > bound:
            return c.f(w=self.weighted), False
        if c.is_goal():
            return bound, True
        best = math.inf
        for child in c.get_children():
            self.gen += 1
            if child not in path:
                path.appendleft(child)
                t, done = self.__search_iter(path, bound)
                if done:
                    return t, True
                if t < best:
                    best = t
                path.popleft()
        return best, False

    def _search(self, start):
        bound = start.h_manh(self.weighted)
        path = deque([start])
        self.iters = 0
        while len(path) > 0:
            t, done = self.__search_iter(path, bound)
            if done:
                return path[0]
            if t == math.inf:
                return None
            bound = t
            self.iters += 1
