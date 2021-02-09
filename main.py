from sliding_puzzle import SlidingTilePuzzle
from astar_early import AstarEarly
from astar_late import AstarLate
from idastar import IDAstar


def analyze_algorithm(alg, puzzle, name):
    moves, cost = alg.search(puzzle, print=False)
    stats = alg.get_stats()
    print(f'{name} | {moves} | {cost} | {" | ".join([str(x) for x in stats.values()])}')


if __name__ == '__main__':
    for x in range(20):
        puzzle = SlidingTilePuzzle(n=3, weighted=True)
        print(puzzle)
        print()

        algs = lambda w: {
            'A*-Early': AstarEarly(weighted=w, clear=True),
            'A*-Late': AstarLate(weighted=w),
            'IDA*': IDAstar(weighted=w),
        }

        for name, a in algs(True).items():
            analyze_algorithm(a, puzzle, f'{name:20} | WMD')
        for name, a in algs(False).items():
            analyze_algorithm(a, puzzle, f'{name:20} |  MD')

