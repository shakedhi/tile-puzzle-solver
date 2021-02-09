from heapq import heapify
from datetime import datetime
import abc

class SearchAlgorithm(abc.ABC):
    def __init__(self, weighted=False):
        self.gen = 1
        self.exp = 0
        self.iters = 0
        self.time = 0
        self.moves = 0
        self.weighted = weighted
        self.g = 0

    def reset_stats(self):
        self.gen = 1
        self.exp = 0
        self.iters = 0
        self.moves = 0
        self.time = 0

    def get_stats(self):
        return {
            'Iterations': self.iters,
            'Generated': self.gen,
            'Expended': self.exp,
            'Duration': self.time
        }

    @abc.abstractmethod
    def _search(self, start):
        pass
    
    def search(self, start, print=True):
        st = datetime.now()
        self.reset_stats()
        res = self._search(start)
        self.time = (datetime.now() - st).total_seconds()
        if print:
            if res is not None:
                print(f'Best solution requires {res.moves} steps (cost={res.g}).')
            else:
                print(f'There is not solution.')
        return res.moves, res.g



class Astar:
    def _check_duplicate(self, lst, child, is_queue=False):
        if child in lst:
            i = lst.index(child)
            if lst[i].g < child.g:
                return True
            lst.pop(i)
            if is_queue:
                heapify(lst)
        return False
    