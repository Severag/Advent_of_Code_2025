import collections, heapq, itertools, re
import numpy as np


def read_file(filename):
    num_parse = lambda line: list(map(int, line.strip().split()))
    str_parse = lambda line: line.strip().split()
    regex = r""
    regex_parse = lambda line: re.findall(regex, line)[0]
    
    with open( filename, 'r') as f:
        data = list(map(num_parse, f))
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    return



def part2(data):
    return



if __name__ == '__main__':
    puzzles = [['test_case.txt', None, None],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))