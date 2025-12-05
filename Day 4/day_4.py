import collections, heapq, itertools, re
import numpy as np


def read_file(filename):
    str_parse = lambda line: [char == '@' for char in line]
    
    with open( filename, 'r') as f:
        data = [str_parse(f".{line.strip()}.") for line in f]
    
    # Adding padding to remove edge cases
    empty = [[False,] * len(data[0])]
    data = empty + data + empty
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    total = 0
    
    for r_idx, row in enumerate(data):
        for c_idx, val in enumerate(row):
            # there's a roll here w/ <4 neighbors
            if val and get_num_neighbors(data, r_idx, c_idx) < 4:
                total += 1
    
    return total



def get_num_neighbors(board, r, c):
    rolls = 0
    
    for r_idx in range(r - 1, r + 2):
        for c_idx in range(c - 1, c + 2):
            if board[r_idx][c_idx] and (r_idx, c_idx) != (r, c):
                rolls += 1
    
    return rolls



def part2(data):
    total = 0
    removals = 1
    
    while removals > 0:
        data, removals = run_round(data)
        
        total += removals
    
    return total



def run_round(board):
    removals = 0
    
    new_board = [[False for val in row] for row in board]
    
    for r_idx, row in enumerate(board):
        for c_idx, val in enumerate(row):
            # there's a roll here
            if val:
                if get_num_neighbors(board, r_idx, c_idx) >= 4:
                    # it stays for the next round if it has 4+ neighbors
                    new_board[r_idx][c_idx] = True
                else:
                    # we remove it by leaving it's value <False>
                    removals += 1
    
    return new_board, removals



if __name__ == '__main__':
    puzzles = [['test_case.txt', 13, 43],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))