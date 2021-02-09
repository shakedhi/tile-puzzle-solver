from heapq import heapify, heappop, heappush
from utils import SearchAlgorithm, Astar
import math


class AstarEarly(SearchAlgorithm, Astar):
    def __init__(self, weighted=False, clear=False):
        super().__init__(weighted)
        self.clear = clear

    def __clear_open(self, openl, best_sol):
        idx = []
        for i, o in enumerate(openl):
            if o.f(w=self.weighted) >= best_sol:
                idx.insert(0, i)
        for i in idx:
            openl.pop(i)
        heapify(openl)

    def _search(self, start):
        openl, closed = [start], []
        heapify(openl)

        best_sol = math.inf
        best_node = None
        self.iters = 0
        while len(openl) > 0:
            self.exp += 1
            best = heappop(openl)

            if best.f(w=self.weighted) >= best_sol:
                return best_node
            
            closed.append(best)
            
            for child in best.get_children():
                self.gen += 1  
                if self._check_duplicate(closed, child) or self._check_duplicate(openl, child, True):
                    continue
                if child.is_goal():
                    if child.g < best_sol:
                        best_sol = child.g
                        best_node = child
                        if self.clear:
                            self.__clear_open(openl, best_sol)
                if child.f(w=self.weighted) <= best_sol:
                    heappush(openl, child)
            
            self.iters += 1

        return None
