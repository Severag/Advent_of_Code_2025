


def read_file(filename):
    num_parse = lambda line: list(map(int, line.strip()))
    
    with open(filename, 'r') as f:
        data = list(map(num_parse, f))
    
    return data



def solve(data, do_1=True, do_2=True):
    p1 = part1(data) if do_1 else None
    p2 = part2(data) if do_2 else None
    
    return p1, p2



def part1(data):
    total = 0
    
    for line in data:
        first,idx = get_next_digit(line, 1)
        second,_ = get_next_digit(line[idx+1:], 0)
        
        joltage = 10 * first + second
        total += joltage

    return total



def get_next_digit(array, with_remaining):
    end_idx = -abs(with_remaining) if with_remaining !=0 else None
    
    num = max(array[:end_idx])
    idx = array.index(num)
    
    return num, idx



def part2(data):
    total = 0
    
    for line in data:
        joltage = 0
        idx = 0
        
        for end_buffer in reversed(range(12)):
            new_digit, d_idx = get_next_digit(line[idx:], end_buffer)
            
            joltage = 10 * joltage + new_digit
            idx += d_idx + 1
        
        total += joltage 
    
    return total



if __name__ == '__main__':
    puzzles = [['test_case.txt', 357, 3_121_910_778_619],
               ['puzzle_input.txt', ]]
    
    try:
        import AoC_testing
        AoC_testing.run(puzzles, read_file, solve)
    except ModuleNotFoundError:
        for filename, *_ in puzzles:
            print(solve(read_file(filename)))