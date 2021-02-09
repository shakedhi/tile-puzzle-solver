from heapq import heapify, heappop, heappush
from utils import SearchAlgorithm, Astar
import math


class AstarLate(SearchAlgorithm, Astar):
    def _search(self, start):
        openl, closed = [start], []
        heapify(openl)

        self.iters = 0
        while len(openl) > 0:
            self.exp += 1
            best = heappop(openl)
            
            if best.is_goal():
                return best
            
            closed.append(best)
            
            for child in best.get_children():  
                child.f(w=self.weighted)
                self.gen += 1
                if self._check_duplicate(closed, child) or self._check_duplicate(openl, child, True):
                    continue
                heappush(openl, child)

            self.iters += 1

        return None