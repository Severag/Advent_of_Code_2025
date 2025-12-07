import copy


def read_file(filename):
    str_parse = lambda line: list(f".{line.replace('S', '|').strip()}.")
    
    with open(filename, 'r') as f:
        data = list(map(str_parse, f))
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    total = 0
    board = copy.deepcopy(data)
    
    for r_idx, row in enumerate(board[:-1]):
        for c_idx, val in enumerate(row):
            if val == '|':
                # found a splitter
                if board[r_idx + 1][c_idx] == '^':
                    board[r_idx + 1][c_idx - 1] = '|'
                    board[r_idx + 1][c_idx + 1] = '|'
                    total += 1
                else:
                    board[r_idx + 1][c_idx] = '|'
    
    return total



def part2(data):
    decoder = {'.':0,
               '^':'^',
               '|':1,}
    board = [[decoder[val] for val in row] for row in data]
    
    for r_idx, row in enumerate(board[:-1]):
        for c_idx, val in enumerate(row):
            if isinstance(val, int):
                # found a splitter
                if board[r_idx + 1][c_idx] == '^':
                    board[r_idx + 1][c_idx - 1] += val
                    board[r_idx + 1][c_idx + 1] += val
                else:
                    board[r_idx + 1][c_idx] += val
    
    return sum(val for val in board[-1] if isinstance(val, int))



if __name__ == '__main__':
    puzzles = [['test_case.txt', 21, 40],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))